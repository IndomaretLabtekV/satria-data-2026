#!/usr/bin/env python3
"""
Kaggle-first train deduplication based on manually curated exact-duplicate review.

Inputs on Kaggle:
  raw train:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026/train
  raw test:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test
  curated duplicate review csv:
    /kaggle/input/datasets/datacommunityhmif/dac-findit-2026-duplicates/true_label_duplicate.csv

Primary goal:
  build a cleaned dataset by:
    - keeping non-duplicate train files as-is
    - keeping one canonical file per reviewed duplicate group
    - placing that canonical file under the curated label
    - writing the cleaned train set to train_deduplicate

Outputs:
  /kaggle/working/train_deduplicate/
    train_deduplicate/
      realperson/
      fake_printed/
      fake_mannequin/
      fake_mask/
      fake_screen/
      fake_unknown/
    test/
    deduplicate_keep_manifest.csv
    deduplicate_drop_manifest.csv
    deduplicate_group_actions.csv
    deduplicate_summary.txt
  /kaggle/working/train_deduplicate.zip

Local paths:
  inputs:
    dataset/train
    dataset/test
    dataset/meta/true_label_duplicate.csv
  generated clean train set:
    dataset/train_deduplicate
  reports:
    output/train_deduplicate
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

KAGGLE_TRAIN_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026/train")
KAGGLE_TEST_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test")
KAGGLE_REVIEW_CSV = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026-duplicates/true_label_duplicate.csv")
KAGGLE_OUTPUT_DIR = Path("/kaggle/working/train_deduplicate")

CLASS_NAMES = [
    "realperson",
    "fake_printed",
    "fake_mannequin",
    "fake_mask",
    "fake_screen",
    "fake_unknown",
]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
RUN_SELF_TEST = os.getenv("DEDUPLICATE_SELF_TEST", "0") == "1"

KEEP_COLUMNS = [
    "source",
    "filename",
    "original_label",
    "final_label",
    "action",
    "group_id",
    "output_relpath",
]
DROP_COLUMNS = [
    "filename",
    "original_label",
    "final_label",
    "group_id",
    "group_size",
    "kept_filename",
    "kept_output_relpath",
    "rationale",
]
GROUP_ACTION_COLUMNS = [
    "group_id",
    "group_size",
    "n_labels",
    "source_labels",
    "final_label",
    "kept_filename",
    "kept_output_relpath",
    "dropped_count",
    "relabeled_count",
    "rationale",
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
class ReviewedGroup:
    group_id: int
    group_size: int
    n_labels: int
    selected_true_label: str
    source_labels: str
    sha256: str
    rationale: str
    members: tuple[str, ...]


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
            if (candidate / "scripts" / "raw_duplicates.py").exists():
                return candidate
            if (candidate / "dataset").exists() and (candidate / "scripts").exists():
                return candidate
    return Path.cwd().resolve()


def resolve_runtime_paths() -> RuntimePaths:
    if running_on_kaggle():
        return RuntimePaths(
            kaggle=True,
            root=Path("/kaggle"),
            train_dir=KAGGLE_TRAIN_DIR,
            test_dir=KAGGLE_TEST_DIR,
            review_csv=KAGGLE_REVIEW_CSV,
            dataset_root_dir=KAGGLE_OUTPUT_DIR,
            generated_train_dir=KAGGLE_OUTPUT_DIR / "train_deduplicate",
            copied_test_dir=KAGGLE_OUTPUT_DIR / "test",
            report_output_dir=KAGGLE_OUTPUT_DIR,
        )
    root = discover_repo_root()
    data_root = root / "dataset"
    return RuntimePaths(
        kaggle=False,
        root=root,
        train_dir=data_root / "train",
        test_dir=data_root / "test",
        review_csv=data_root / "meta" / "true_label_duplicate.csv",
        dataset_root_dir=data_root,
        generated_train_dir=data_root / "train_deduplicate",
        copied_test_dir=None,
        report_output_dir=root / "output" / "train_deduplicate",
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
                records.append(
                    ImageRecord(
                        record_id=path.name,
                        filename=path.name,
                        label=label,
                        path=path,
                        source="train",
                    )
                )
    return records


def collect_test_records(test_dir: Path) -> List[ImageRecord]:
    records: List[ImageRecord] = []
    if not test_dir.exists():
        return records
    for path in sorted(test_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            records.append(
                ImageRecord(
                    record_id=path.name,
                    filename=path.name,
                    label="",
                    path=path,
                    source="test",
                )
            )
    return records


def parse_members(value: str) -> tuple[str, ...]:
    return tuple(member for member in str(value).split("|") if member)


def load_reviewed_groups(review_csv: Path) -> List[ReviewedGroup]:
    if not review_csv.exists():
        raise RuntimeError(f"Curated duplicate review CSV not found: {review_csv}")
    df = pd.read_csv(review_csv)
    required = {
        "group_id",
        "group_size",
        "n_labels",
        "selected_true_label",
        "source_labels",
        "sha256",
        "rationale",
        "members",
    }
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Review CSV is missing required columns: {sorted(missing)}")

    groups: List[ReviewedGroup] = []
    for row in df.itertuples(index=False):
        members = parse_members(row.members)
        if not members:
            raise RuntimeError(f"group_id={row.group_id} has no members")
        if row.selected_true_label not in CLASS_NAMES:
            raise RuntimeError(
                f"group_id={row.group_id} has invalid selected_true_label={row.selected_true_label}"
            )
        groups.append(
            ReviewedGroup(
                group_id=int(row.group_id),
                group_size=int(row.group_size),
                n_labels=int(row.n_labels),
                selected_true_label=str(row.selected_true_label),
                source_labels=str(row.source_labels),
                sha256=str(row.sha256),
                rationale=str(row.rationale),
                members=members,
            )
        )
    return groups


def choose_canonical_member(group: ReviewedGroup, record_by_id: Dict[str, ImageRecord]) -> ImageRecord:
    candidates = [record_by_id[member] for member in group.members]
    return sorted(
        candidates,
        key=lambda record: (
            0 if record.label == group.selected_true_label else 1,
            record.filename.lower(),
            record.record_id.lower(),
        ),
    )[0]


def unique_output_relpath(
    target_label: str,
    preferred_filename: str,
    group_id: int,
    used_paths: set[str],
) -> tuple[str, bool]:
    preferred = f"{target_label}/{preferred_filename}"
    if preferred not in used_paths:
        used_paths.add(preferred)
        return preferred, False

    stem = Path(preferred_filename).stem
    suffix = Path(preferred_filename).suffix
    candidate = f"{target_label}/{stem}__grp{group_id:03d}{suffix}"
    if candidate not in used_paths:
        used_paths.add(candidate)
        return candidate, True

    index = 2
    while True:
        candidate = f"{target_label}/{stem}__grp{group_id:03d}_{index}{suffix}"
        if candidate not in used_paths:
            used_paths.add(candidate)
            return candidate, True
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
    reviewed_groups: Sequence[ReviewedGroup],
    keep_df: pd.DataFrame,
    drop_df: pd.DataFrame,
) -> str:
    kept_train = keep_df[keep_df["source"] == "train"] if not keep_df.empty else pd.DataFrame()
    kept_test = keep_df[keep_df["source"] == "test"] if not keep_df.empty else pd.DataFrame()
    relabeled = (
        kept_train[kept_train["original_label"] != kept_train["final_label"]]
        if not kept_train.empty
        else pd.DataFrame()
    )
    renamed = (
        kept_train[
            kept_train.apply(
                lambda row: Path(str(row["output_relpath"])).name != str(row["filename"]),
                axis=1,
            )
        ]
        if not kept_train.empty
        else pd.DataFrame()
    )

    lines = [
        "Deduplicate summary",
        f"train_dir={TRAIN_DIR}",
        f"test_dir={TEST_DIR}",
        f"review_csv={REVIEW_CSV}",
        "",
        f"raw_train_images={len(train_records)}",
        f"raw_test_images={len(test_records)}",
        f"reviewed_duplicate_groups={len(reviewed_groups)}",
        f"kept_train_images={len(kept_train)}",
        f"dropped_train_images={len(drop_df)}",
        f"kept_test_images={len(kept_test)}",
        f"relabeled_kept_train_images={len(relabeled)}",
        f"renamed_kept_train_images={len(renamed)}",
        "",
        "kept_train_by_label:",
    ]
    if kept_train.empty:
        lines.append("  none")
    else:
        counts = kept_train["final_label"].value_counts().reindex(CLASS_NAMES, fill_value=0)
        for label, count in counts.items():
            lines.append(f"  {label}={int(count)}")
    return "\n".join(lines) + "\n"


def run_self_tests() -> None:
    group = ReviewedGroup(
        group_id=7,
        group_size=3,
        n_labels=2,
        selected_true_label="fake_printed",
        source_labels="fake_mask|fake_printed",
        sha256="abc",
        rationale="printed card",
        members=("fake_mask/x.jpg", "fake_printed/a.jpg", "fake_printed/b.jpg"),
    )
    record_by_id = {
        "fake_mask/x.jpg": ImageRecord("fake_mask/x.jpg", "x.jpg", "fake_mask", Path("fake_mask") / "x.jpg"),
        "fake_printed/a.jpg": ImageRecord("fake_printed/a.jpg", "a.jpg", "fake_printed", Path("fake_printed") / "a.jpg"),
        "fake_printed/b.jpg": ImageRecord("fake_printed/b.jpg", "b.jpg", "fake_printed", Path("fake_printed") / "b.jpg"),
    }
    chosen = choose_canonical_member(group, record_by_id)
    assert chosen.record_id == "fake_printed/a.jpg"

    used_paths: set[str] = set()
    first_path, first_renamed = unique_output_relpath("fake_printed", "same.jpg", 7, used_paths)
    second_path, second_renamed = unique_output_relpath("fake_printed", "same.jpg", 8, used_paths)
    assert first_path == "fake_printed/same.jpg"
    assert first_renamed == 0 or first_renamed is False
    assert second_path == "fake_printed/same__grp008.jpg"
    assert second_renamed == 1 or second_renamed is True
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
    reviewed_groups = load_reviewed_groups(REVIEW_CSV)

    if not train_records:
        raise RuntimeError(f"No train images found under {TRAIN_DIR}")

    record_by_id = {record.record_id: record for record in train_records}
    reviewed_member_ids = set()
    for group in reviewed_groups:
        if group.group_size != len(group.members):
            raise RuntimeError(
                f"group_id={group.group_id} expected group_size={group.group_size} but members={len(group.members)}"
            )
        for member in group.members:
            if member not in record_by_id:
                raise RuntimeError(f"group_id={group.group_id} references missing train record: {member}")
            if member in reviewed_member_ids:
                raise RuntimeError(f"train record appears in multiple reviewed groups: {member}")
            reviewed_member_ids.add(member)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if GENERATED_TRAIN_DIR.exists():
        shutil.rmtree(GENERATED_TRAIN_DIR)
    GENERATED_TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    output_train_dir = GENERATED_TRAIN_DIR
    for label in CLASS_NAMES:
        (output_train_dir / label).mkdir(parents=True, exist_ok=True)
    if COPIED_TEST_DIR is not None:
        if COPIED_TEST_DIR.exists():
            shutil.rmtree(COPIED_TEST_DIR)
        COPIED_TEST_DIR.mkdir(parents=True, exist_ok=True)

    used_output_paths: set[str] = set()
    keep_rows: List[dict] = []
    drop_rows: List[dict] = []
    group_action_rows: List[dict] = []

    reviewed_by_member = {
        member: group
        for group in reviewed_groups
        for member in group.members
    }

    for group in tqdm(reviewed_groups, desc="Materialize dedup train groups", leave=True):
        canonical = choose_canonical_member(group, record_by_id)
        output_relpath, was_renamed = unique_output_relpath(
            f"train_deduplicate/{group.selected_true_label}",
            canonical.filename,
            group.group_id,
            used_output_paths,
        )
        copy_record(canonical, DATASET_ROOT_DIR / output_relpath)
        keep_rows.append(
            {
                "source": "train",
                "filename": canonical.filename,
                "original_label": canonical.label,
                "final_label": group.selected_true_label,
                "action": "keep_canonical",
                "group_id": group.group_id,
                "output_relpath": output_relpath,
            }
        )

        dropped_count = 0
        relabeled_count = 0
        for member in group.members:
            if member == canonical.record_id:
                continue
            record = record_by_id[member]
            dropped_count += 1
            relabeled_count += int(record.label != group.selected_true_label)
            drop_rows.append(
                {
                    "filename": record.filename,
                    "original_label": record.label,
                    "final_label": group.selected_true_label,
                    "group_id": group.group_id,
                    "group_size": group.group_size,
                    "kept_filename": canonical.filename,
                    "kept_output_relpath": output_relpath,
                    "rationale": group.rationale,
                }
            )

        group_action_rows.append(
            {
                "group_id": group.group_id,
                "group_size": group.group_size,
                "n_labels": group.n_labels,
                "source_labels": group.source_labels,
                "final_label": group.selected_true_label,
                "kept_filename": canonical.filename,
                "kept_output_relpath": output_relpath,
                "dropped_count": dropped_count,
                "relabeled_count": relabeled_count + int(canonical.label != group.selected_true_label),
                "rationale": group.rationale,
            }
        )

    singleton_records = [record for record in train_records if record.record_id not in reviewed_by_member]
    for record in tqdm(singleton_records, desc="Copy singleton train files", leave=True):
        output_relpath, was_renamed = unique_output_relpath(
            f"train_deduplicate/{record.label}",
            record.filename,
            -1,
            used_output_paths,
        )
        copy_record(record, DATASET_ROOT_DIR / output_relpath)
        keep_rows.append(
            {
                "source": "train",
                "filename": record.filename,
                "original_label": record.label,
                "final_label": record.label,
                "action": "keep_singleton",
                "group_id": -1,
                "output_relpath": output_relpath,
            }
        )

    if COPIED_TEST_DIR is not None:
        for record in tqdm(test_records, desc="Copy test files", leave=True):
            output_relpath = f"test/{record.filename}"
            copy_record(record, DATASET_ROOT_DIR / output_relpath)
            keep_rows.append(
                {
                    "source": "test",
                    "filename": record.filename,
                    "original_label": "",
                    "final_label": "",
                    "action": "copy_test",
                    "group_id": -1,
                    "output_relpath": output_relpath,
                }
            )

    keep_df = pd.DataFrame(keep_rows, columns=KEEP_COLUMNS)
    drop_df = pd.DataFrame(drop_rows, columns=DROP_COLUMNS)
    group_actions_df = pd.DataFrame(group_action_rows, columns=GROUP_ACTION_COLUMNS)

    if not keep_df.empty:
        keep_df = keep_df.sort_values(["source", "final_label", "output_relpath", "filename"])
    if not drop_df.empty:
        drop_df = drop_df.sort_values(["group_id", "filename"])
    if not group_actions_df.empty:
        group_actions_df = group_actions_df.sort_values(["group_id"])

    keep_manifest_path = OUTPUT_DIR / "deduplicate_keep_manifest.csv"
    drop_manifest_path = OUTPUT_DIR / "deduplicate_drop_manifest.csv"
    group_actions_path = OUTPUT_DIR / "deduplicate_group_actions.csv"
    summary_path = OUTPUT_DIR / "deduplicate_summary.txt"

    keep_df.to_csv(keep_manifest_path, index=False)
    drop_df.to_csv(drop_manifest_path, index=False)
    group_actions_df.to_csv(group_actions_path, index=False)
    summary_path.write_text(
        summary_text(train_records, test_records, reviewed_groups, keep_df, drop_df),
        encoding="utf-8",
    )

    zip_path = zip_output_dir(OUTPUT_DIR)

    print(f"raw train images      : {len(train_records)}")
    print(f"raw test images       : {len(test_records)}")
    print(f"reviewed groups       : {len(reviewed_groups)}")
    print(f"kept train images     : {int((keep_df['source'] == 'train').sum()) if not keep_df.empty else 0}")
    print(f"dropped train images  : {len(drop_df)}")
    print(f"copied test images    : {int((keep_df['source'] == 'test').sum()) if not keep_df.empty else 0}")
    print(f"saved                 : {keep_manifest_path}")
    print(f"saved                 : {drop_manifest_path}")
    print(f"saved                 : {group_actions_path}")
    print(f"saved                 : {summary_path}")
    print(f"saved                 : {zip_path}")
