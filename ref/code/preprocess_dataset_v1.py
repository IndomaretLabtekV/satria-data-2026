from __future__ import annotations

import csv
import json
import random
import shutil
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@dataclass
class PreprocessConfig:
    project_root: Path
    raw_root: Path
    processed_root: Path
    output_size: int = 320
    pad_color: tuple[int, int, int] = (114, 114, 114)
    seed: int = 42
    train_augments_per_class: dict[str, int] | None = None


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in VALID_EXTENSIONS


def list_images(root_dir: Path) -> list[Path]:
    return sorted([path for path in root_dir.rglob("*") if is_image_file(path)])


def safe_copy_tree(src: Path, dst: Path) -> None:
    ensure_dir(dst)
    for item in src.rglob("*"):
        rel_path = item.relative_to(src)
        target = dst / rel_path
        if item.is_dir():
            ensure_dir(target)
        else:
            ensure_dir(target.parent)
            if not target.exists():
                shutil.copy2(item, target)


def open_rgb_image(path: Path) -> Image.Image:
    image = Image.open(path)
    return image.convert("RGB")


def resize_with_padding(image: Image.Image, output_size: int, pad_color: tuple[int, int, int]) -> Image.Image:
    resized = image.copy()
    resized.thumbnail((output_size, output_size), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (output_size, output_size), color=pad_color)
    offset_x = (output_size - resized.width) // 2
    offset_y = (output_size - resized.height) // 2
    canvas.paste(resized, (offset_x, offset_y))
    return canvas


def add_light_gaussian_noise(image: Image.Image, sigma_range: tuple[float, float] = (2.0, 6.0)) -> Image.Image:
    sigma = random.uniform(*sigma_range)
    arr = np.array(image).astype(np.float32)
    noise = np.random.normal(0.0, sigma, size=arr.shape)
    noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)


def augment_image(image: Image.Image) -> Image.Image:
    augmented = image.copy()

    if random.random() < 0.5:
        augmented = ImageOps.mirror(augmented)

    if random.random() < 0.8:
        augmented = ImageEnhance.Brightness(augmented).enhance(random.uniform(0.92, 1.10))

    if random.random() < 0.8:
        augmented = ImageEnhance.Contrast(augmented).enhance(random.uniform(0.92, 1.12))

    if random.random() < 0.3:
        augmented = ImageEnhance.Color(augmented).enhance(random.uniform(0.95, 1.05))

    if random.random() < 0.2:
        augmented = augmented.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 0.8)))

    if random.random() < 0.15:
        augmented = ImageEnhance.Sharpness(augmented).enhance(random.uniform(1.05, 1.25))

    if random.random() < 0.2:
        augmented = add_light_gaussian_noise(augmented)

    return augmented


def save_png(image: Image.Image, output_path: Path) -> None:
    ensure_dir(output_path.parent)
    image.save(output_path, format="PNG", optimize=True)


def build_default_augments_per_class() -> dict[str, int]:
    return {
        "realperson": 0,
        "fake_unknown": 0,
        "fake_mask": 1,
        "fake_screen": 1,
        "fake_mannequin": 1,
        "fake_printed": 2,
    }


def process_train_split(
    train_dir: Path,
    output_root: Path,
    config: PreprocessConfig,
) -> list[dict[str, str | int | bool]]:
    manifest_rows: list[dict[str, str | int | bool]] = []
    class_dirs = sorted([path for path in train_dir.iterdir() if path.is_dir()])

    augments_per_class = config.train_augments_per_class or build_default_augments_per_class()

    for class_dir in class_dirs:
        class_name = class_dir.name
        image_paths = list_images(class_dir)
        class_output_dir = output_root / "train" / class_name
        ensure_dir(class_output_dir)

        num_augments = augments_per_class.get(class_name, 1)

        for image_path in image_paths:
            image_id = image_path.stem
            original = open_rgb_image(image_path)
            processed = resize_with_padding(original, config.output_size, config.pad_color)

            original_output_path = class_output_dir / f"{image_id}__orig.png"
            save_png(processed, original_output_path)

            manifest_rows.append(
                {
                    "split": "train",
                    "class_name": class_name,
                    "source_path": str(image_path),
                    "output_path": str(original_output_path),
                    "variant": "orig",
                    "augmented": False,
                }
            )

            for aug_idx in range(1, num_augments + 1):
                augmented = augment_image(original)
                augmented = resize_with_padding(augmented, config.output_size, config.pad_color)
                aug_output_path = class_output_dir / f"{image_id}__aug{aug_idx}.png"
                save_png(augmented, aug_output_path)

                manifest_rows.append(
                    {
                        "split": "train",
                        "class_name": class_name,
                        "source_path": str(image_path),
                        "output_path": str(aug_output_path),
                        "variant": f"aug{aug_idx}",
                        "augmented": True,
                    }
                )

    return manifest_rows


def process_test_split(
    test_dir: Path,
    output_root: Path,
    config: PreprocessConfig,
) -> list[dict[str, str | int | bool]]:
    manifest_rows: list[dict[str, str | int | bool]] = []
    test_output_dir = output_root / "test"
    ensure_dir(test_output_dir)

    for image_path in list_images(test_dir):
        image_id = image_path.stem
        original = open_rgb_image(image_path)
        processed = resize_with_padding(original, config.output_size, config.pad_color)
        output_path = test_output_dir / f"{image_id}.png"
        save_png(processed, output_path)

        manifest_rows.append(
            {
                "split": "test",
                "class_name": "",
                "source_path": str(image_path),
                "output_path": str(output_path),
                "variant": "orig",
                "augmented": False,
            }
        )

    return manifest_rows


def write_manifest(manifest_rows: list[dict[str, str | int | bool]], output_root: Path) -> Path:
    manifest_path = output_root / "manifest.csv"
    fieldnames = ["split", "class_name", "source_path", "output_path", "variant", "augmented"]

    with manifest_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    return manifest_path


def write_config(config: PreprocessConfig, output_root: Path) -> Path:
    config_path = output_root / "preprocessing_config.json"
    serializable = asdict(config)
    serializable["project_root"] = str(config.project_root)
    serializable["raw_root"] = str(config.raw_root)
    serializable["processed_root"] = str(config.processed_root)

    with config_path.open("w", encoding="utf-8") as file_obj:
        json.dump(serializable, file_obj, indent=2)

    return config_path


def summarize_outputs(output_root: Path) -> dict[str, Counter]:
    summary: dict[str, Counter] = {"train": Counter(), "test": Counter()}
    train_root = output_root / "train"
    if train_root.exists():
        for class_dir in sorted([path for path in train_root.iterdir() if path.is_dir()]):
            summary["train"][class_dir.name] = len(list_images(class_dir))

    test_root = output_root / "test"
    if test_root.exists():
        summary["test"]["unlabeled_test"] = len(list_images(test_root))

    return summary


def resolve_input_dirs(project_root: Path, raw_root: Path) -> tuple[Path, Path]:
    raw_train = raw_root / "train"
    raw_test = raw_root / "test"
    if raw_train.exists() and raw_test.exists():
        return raw_train, raw_test

    source_train = project_root / "train"
    source_test = project_root / "test"
    if source_train.exists() and source_test.exists():
        ensure_dir(raw_root)
        safe_copy_tree(source_train, raw_train)
        safe_copy_tree(source_test, raw_test)
        return raw_train, raw_test

    raise FileNotFoundError(
        "Could not find input dataset. Expected either raw/train + raw/test or train + test under the project root."
    )


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config = PreprocessConfig(
        project_root=project_root,
        raw_root=project_root / "raw",
        processed_root=project_root / "processed" / "preprocessing_v1",
        output_size=320,
        pad_color=(114, 114, 114),
        seed=42,
        train_augments_per_class=build_default_augments_per_class(),
    )

    set_seed(config.seed)
    source_train, source_test = resolve_input_dirs(config.project_root, config.raw_root)

    if config.processed_root.exists():
        shutil.rmtree(config.processed_root)
    ensure_dir(config.processed_root)

    manifest_rows = []
    manifest_rows.extend(process_train_split(source_train, config.processed_root, config))
    manifest_rows.extend(process_test_split(source_test, config.processed_root, config))

    manifest_path = write_manifest(manifest_rows, config.processed_root)
    config_path = write_config(config, config.processed_root)
    summary = summarize_outputs(config.processed_root)

    print("Preprocessing V1 complete")
    print(f"Raw dataset root      : {config.raw_root}")
    print(f"Processed dataset root: {config.processed_root}")
    print(f"Manifest              : {manifest_path}")
    print(f"Config                : {config_path}")
    print("Processed train counts:")
    for class_name, count in sorted(summary["train"].items()):
        print(f"  {class_name:<20} {count:>6}")
    print(f"Processed test count  : {summary['test']['unlabeled_test']}")


if __name__ == "__main__":
    main()
