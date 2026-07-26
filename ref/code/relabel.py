#!/usr/bin/env python3
"""
Kaggle-first train relabeling based on manually reviewed individual labels.

Inputs on Kaggle:
  deduplicated train:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026-deduplicate/train_deduplicate
  raw test:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test
  manual relabel csv:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026-duplicates/true_label_manual.csv

Primary goal:
  build train_clean by:
    - keeping every train file
    - relabeling only filenames listed in true_label_manual.csv
    - writing the cleaned train set to train_clean

Outputs:
  /kaggle/working/train_clean/
    train_clean/
      realperson/
      fake_printed/
      fake_mannequin/
      fake_mask/
      fake_screen/
      fake_unknown/
    test/
    train_clean_manifest.csv
    train_clean_changes.csv
    train_clean_summary.txt
  /kaggle/working/train_clean.zip

Local paths:
  inputs:
    dataset/train_deduplicate
    dataset/test
    dataset/meta/true_label_manual.csv
  generated cleaned train set:
    dataset/train_clean
  reports:
    output/train_clean
"""

from __future__ import annotations

import os
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

import pandas as pd
from tqdm import tqdm

KAGGLE_TRAIN_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026-deduplicate/train_deduplicate")
KAGGLE_TEST_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test")
KAGGLE_REVIEW_CSV = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026-duplicates/true_label_manual.csv")
KAGGLE_OUTPUT_DIR = Path("/kaggle/working/train_clean")

CLASS_NAMES = [
    "realperson",
    "fake_printed",
    "fake_mannequin",
    "fake_mask",
    "fake_screen",
    "fake_unknown",
]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
RUN_SELF_TEST = os.getenv("RELABEL_SELF_TEST", "0") == "1"

MANIFEST_COLUMNS = [
    "source",
    "filename",
    "original_label",
    "final_label",
    "action",
    "output_relpath",
    "note",
]
CHANGE_COLUMNS = [
    "filename",
    "original_label",
    "final_label",
    "output_relpath",
    "note",
]


@dataclass(frozen=True)
class RuntimePaths:
    kaggle: bool
    root: Path
    train_dir: Path
    test_dir: Path
    review_csv: Path
    dataset_root_dir: Path
    generated_train_dir: Path
    copied_test_dir: Path | None
    report_output_dir: Path


@dataclass(frozen=True)
class ImageRecord:
    record_id: str
    filename: str
    label: str
    path: Path
    source: str = "train"


@dataclass(frozen=True)
class ManualRelabel:
    filename: str
    original_label: str
    corrected_label: str
    note: str


def running_on_kaggle() -> bool:
    return Path("/kaggle/input").exists() or bool(os.getenv("KAGGLE_KERNEL_RUN_TYPE"))


def discover_repo_root() -> Path:
    seen: set[Path] = set()
    starts = [Path.cwd()]
    if "__file__" in globals():
        starts.insert(0, Path(__file__).resolve().parent)
    for start in starts:
        for candidate in [start.resolve(), *start.resolve().parents]:
            if candidate in seen:
                continue
            seen.add(candidate)
            if (candidate / "scripts" / "relabel.py").exists():
                return candidate
            if (candidate / "dataset").exists() and (candidate / "scripts").exists():
                return candidate
    return Path.cwd().resolve()


def resolve_runtime_paths() -> RuntimePaths:
    if running_on_kaggle():
        kaggle_train_dir = KAGGLE_TRAIN_DIR
        if not kaggle_train_dir.exists():
            kaggle_train_dir = Path("/kaggle/working/train_deduplicate/train_deduplicate")
        return RuntimePaths(
            kaggle=True,
            root=Path("/kaggle"),
            train_dir=kaggle_train_dir,
            test_dir=KAGGLE_TEST_DIR,
            review_csv=KAGGLE_REVIEW_CSV,
            dataset_root_dir=KAGGLE_OUTPUT_DIR,
            generated_train_dir=KAGGLE_OUTPUT_DIR / "train_clean",
            copied_test_dir=KAGGLE_OUTPUT_DIR / "test",
            report_output_dir=KAGGLE_OUTPUT_DIR,
        )
    root = discover_repo_root()
    data_root = root / "dataset"
    return RuntimePaths(
        kaggle=False,
        root=root,
        train_dir=data_root / "train_deduplicate",
        test_dir=data_root / "test",
        review_csv=data_root / "meta" / "true_label_manual.csv",
        dataset_root_dir=data_root,
        generated_train_dir=data_root / "train_clean",
        copied_test_dir=None,
        report_output_dir=root / "output" / "train_clean",
    )


RUNTIME = resolve_runtime_paths()
KAGGLE = RUNTIME.kaggle
ROOT = RUNTIME.root
TRAIN_DIR = RUNTIME.train_dir
TEST_DIR = RUNTIME.test_dir
REVIEW_CSV = RUNTIME.review_csv
DATASET_ROOT_DIR = RUNTIME.dataset_root_dir
GENERATED_TRAIN_DIR = RUNTIME.generated_train_dir
COPIED_TEST_DIR = RUNTIME.copied_test_dir
OUTPUT_DIR = RUNTIME.report_output_dir


def collect_train_records(train_dir: Path) -> List[ImageRecord]:
    records: List[ImageRecord] = []
    for label in CLASS_NAMES:
        cls_dir = train_dir / label
        if not cls_dir.exists():
            continue
        for path in sorted(cls_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                records.append(ImageRecord(path.name, path.name, label, path, "train"))
    return records


def collect_test_records(test_dir: Path) -> List[ImageRecord]:
    records: List[ImageRecord] = []
    if not test_dir.exists():
        return records
    for path in sorted(test_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            records.append(ImageRecord(path.name, path.name, "", path, "test"))
    return records


def load_manual_relabels(review_csv: Path) -> List[ManualRelabel]:
    if not review_csv.exists():
        raise RuntimeError(f"Manual relabel CSV not found: {review_csv}")
    df = pd.read_csv(review_csv).fillna("")
    required = {"filename", "original_label", "corrected_label", "note"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Manual relabel CSV is missing required columns: {sorted(missing)}")

    relabels: List[ManualRelabel] = []
    for row in df.itertuples(index=False):
        if row.original_label not in CLASS_NAMES:
            raise RuntimeError(f"filename={row.filename} has invalid original_label={row.original_label}")
        if row.corrected_label not in CLASS_NAMES:
            raise RuntimeError(f"filename={row.filename} has invalid corrected_label={row.corrected_label}")
        relabels.append(
            ManualRelabel(
                filename=str(row.filename),
                original_label=str(row.original_label),
                corrected_label=str(row.corrected_label),
                note=str(row.note),
            )
        )
    return relabels


def unique_output_relpath(target_label: str, preferred_filename: str, used_paths: set[str]) -> str:
    preferred = f"{target_label}/{preferred_filename}"
    if preferred not in used_paths:
        used_paths.add(preferred)
        return preferred

    stem = Path(preferred_filename).stem
    suffix = Path(preferred_filename).suffix
    index = 2
    while True:
        candidate = f"{target_label}/{stem}__dup{index}{suffix}"
        if candidate not in used_paths:
            used_paths.add(candidate)
            return candidate
        index += 1


def copy_record(record: ImageRecord, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(record.path, destination)


def zip_output_dir(output_dir: Path) -> Path:
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(output_dir.parent))
    return zip_path


def summary_text(
    train_records: Sequence[ImageRecord],
    test_records: Sequence[ImageRecord],
    manual_relabels: Sequence[ManualRelabel],
    manifest_df: pd.DataFrame,
    changes_df: pd.DataFrame,
) -> str:
    kept_train = manifest_df[manifest_df["source"] == "train"] if not manifest_df.empty else pd.DataFrame()
    kept_test = manifest_df[manifest_df["source"] == "test"] if not manifest_df.empty else pd.DataFrame()
    lines = [
        "Train clean summary",
        f"train_dir={TRAIN_DIR}",
        f"test_dir={TEST_DIR}",
        f"review_csv={REVIEW_CSV}",
        "",
        f"raw_train_images={len(train_records)}",
        f"raw_test_images={len(test_records)}",
        f"manual_relabel_rows={len(manual_relabels)}",
        f"applied_relabels={len(changes_df)}",
        f"kept_train_images={len(kept_train)}",
        f"kept_test_images={len(kept_test)}",
        "",
        "train_by_label:",
    ]
    if kept_train.empty:
        lines.append("  none")
    else:
        counts = kept_train["final_label"].value_counts().reindex(CLASS_NAMES, fill_value=0)
        for label, count in counts.items():
            lines.append(f"  {label}={int(count)}")
    return "\n".join(lines) + "\n"


def run_self_tests() -> None:
    relabels = [
        ManualRelabel("a.jpg", "fake_mask", "fake_printed", "printed card"),
        ManualRelabel("b.jpg", "fake_screen", "realperson", ""),
    ]
    relabel_by_filename = {row.filename: row for row in relabels}
    assert relabel_by_filename["a.jpg"].corrected_label == "fake_printed"

    used_paths: set[str] = set()
    first_path = unique_output_relpath("fake_printed", "same.jpg", used_paths)
    second_path = unique_output_relpath("fake_printed", "same.jpg", used_paths)
    assert first_path == "fake_printed/same.jpg"
    assert second_path == "fake_printed/same__dup2.jpg"
    print("Self-test passed.")


print(f"KAGGLE      : {KAGGLE}")
print(f"ROOT        : {ROOT}")
print(f"TRAIN_DIR   : {TRAIN_DIR}")
print(f"TEST_DIR    : {TEST_DIR}")
print(f"REVIEW_CSV  : {REVIEW_CSV}")
print(f"DATASET_DIR : {DATASET_ROOT_DIR}")
print(f"TRAIN_OUT   : {GENERATED_TRAIN_DIR}")
print(f"OUTPUT_DIR  : {OUTPUT_DIR}")

if RUN_SELF_TEST:
    run_self_tests()
else:
    train_records = collect_train_records(TRAIN_DIR)
    test_records = collect_test_records(TEST_DIR)
    manual_relabels = load_manual_relabels(REVIEW_CSV)

    if not train_records:
        raise RuntimeError(f"No train images found under {TRAIN_DIR}")

    record_by_id = {record.record_id: record for record in train_records}
    relabel_by_filename: Dict[str, ManualRelabel] = {}
    for row in manual_relabels:
        if row.filename not in record_by_id:
            raise RuntimeError(f"Manual relabel references missing train record: {row.filename}")
        if row.filename in relabel_by_filename:
            raise RuntimeError(f"Manual relabel contains duplicate filename entry: {row.filename}")
        actual_label = record_by_id[row.filename].label
        if actual_label != row.original_label:
            raise RuntimeError(
                f"filename={row.filename} expected original_label={row.original_label} but found {actual_label}"
            )
        relabel_by_filename[row.filename] = row

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if GENERATED_TRAIN_DIR.exists():
        shutil.rmtree(GENERATED_TRAIN_DIR)
    GENERATED_TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    for label in CLASS_NAMES:
        (GENERATED_TRAIN_DIR / label).mkdir(parents=True, exist_ok=True)
    if COPIED_TEST_DIR is not None:
        if COPIED_TEST_DIR.exists():
            shutil.rmtree(COPIED_TEST_DIR)
        COPIED_TEST_DIR.mkdir(parents=True, exist_ok=True)

    used_output_paths: set[str] = set()
    manifest_rows: List[dict] = []
    change_rows: List[dict] = []

    for record in tqdm(train_records, desc="Materialize train_clean", leave=True):
        manual_row = relabel_by_filename.get(record.filename)
        final_label = manual_row.corrected_label if manual_row is not None else record.label
        output_relpath = unique_output_relpath(f"train_clean/{final_label}", record.filename, used_output_paths)
        copy_record(record, DATASET_ROOT_DIR / output_relpath)
        action = "relabel" if manual_row is not None else "keep_label"
        note = manual_row.note if manual_row is not None else ""
        manifest_rows.append(
            {
                "source": "train",
                "filename": record.filename,
                "original_label": record.label,
                "final_label": final_label,
                "action": action,
                "output_relpath": output_relpath,
                "note": note,
            }
        )
        if manual_row is not None:
            change_rows.append(
                {
                    "filename": record.filename,
                    "original_label": record.label,
                    "final_label": final_label,
                    "output_relpath": output_relpath,
                    "note": note,
                }
            )

    if COPIED_TEST_DIR is not None:
        for record in tqdm(test_records, desc="Copy test files", leave=True):
            output_relpath = f"test/{record.filename}"
            copy_record(record, DATASET_ROOT_DIR / output_relpath)
            manifest_rows.append(
                {
                    "source": "test",
                    "filename": record.filename,
                    "original_label": "",
                    "final_label": "",
                    "action": "copy_test",
                    "output_relpath": output_relpath,
                    "note": "",
                }
            )

    manifest_df = pd.DataFrame(manifest_rows, columns=MANIFEST_COLUMNS)
    changes_df = pd.DataFrame(change_rows, columns=CHANGE_COLUMNS)

    if not manifest_df.empty:
        manifest_df = manifest_df.sort_values(["source", "final_label", "output_relpath", "filename"])
    if not changes_df.empty:
        changes_df = changes_df.sort_values(["final_label", "filename"])

    manifest_path = OUTPUT_DIR / "train_clean_manifest.csv"
    changes_path = OUTPUT_DIR / "train_clean_changes.csv"
    summary_path = OUTPUT_DIR / "train_clean_summary.txt"

    manifest_df.to_csv(manifest_path, index=False)
    changes_df.to_csv(changes_path, index=False)
    summary_path.write_text(
        summary_text(train_records, test_records, manual_relabels, manifest_df, changes_df),
        encoding="utf-8",
    )

    zip_path = zip_output_dir(OUTPUT_DIR)

    print(f"raw train images      : {len(train_records)}")
    print(f"raw test images       : {len(test_records)}")
    print(f"manual relabel rows   : {len(manual_relabels)}")
    print(f"applied relabels      : {len(changes_df)}")
    print(f"kept train images     : {int((manifest_df['source'] == 'train').sum()) if not manifest_df.empty else 0}")
    print(f"copied test images    : {int((manifest_df['source'] == 'test').sum()) if not manifest_df.empty else 0}")
    print(f"saved                 : {manifest_path}")
    print(f"saved                 : {changes_path}")
    print(f"saved                 : {summary_path}")
    print(f"saved                 : {zip_path}")
