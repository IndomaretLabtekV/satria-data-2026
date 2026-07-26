#!/usr/bin/env python3
"""
Kaggle-first exact duplicate detection on the raw DAC FindIT 2026 files.

Kaggle inputs:
  /kaggle/input/datasets/datacommunityhmif/dac-findit-2026/train
  /kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test

Method:
  exact file matches via sha256(raw file bytes)

Outputs:
  /kaggle/working/raw_duplicates/
    raw_train_members_sha256.csv
    raw_train_groups_sha256.csv
    raw_train_duplicates_sha256.csv
    raw_train_pairs_sha256.csv
    raw_train_review_queue_sha256.csv
    raw_train_summary.txt
    raw_with_test_members_sha256.csv
    raw_with_test_groups_sha256.csv
    raw_with_test_duplicates_sha256.csv
    raw_with_test_pairs_sha256.csv
    raw_with_test_review_queue_sha256.csv
    raw_with_test_summary.txt
    raw_train_group_sizes_sha256.png
    raw_train_group_graphs_sha256.png
    raw_train_top_groups_sha256.png
    raw_with_test_overlap_groups_sha256.png
    raw_with_test_overlap_graphs_sha256.png
  /kaggle/working/raw_duplicates.zip

Kaggle install requirements:
  no extra installs required beyond the standard Kaggle Python image
"""

from __future__ import annotations

import hashlib
import itertools
import os
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm

KAGGLE_TRAIN_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026/train")
KAGGLE_TEST_DIR = Path("/kaggle/input/datasets/datacommunityhmif/dac-findit-2026/test")
KAGGLE_OUTPUT_DIR = Path("/kaggle/working/raw_duplicates")
CLASS_NAMES = [
    "realperson",
    "fake_printed",
    "fake_mannequin",
    "fake_mask",
    "fake_screen",
    "fake_unknown",
]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
RUN_SELF_TEST = os.getenv("RAW_DUPLICATES_SELF_TEST", "0") == "1"
HASH_CHUNK_SIZE = 1024 * 1024

TRAIN_MEMBER_COLUMNS = [
    "record_id",
    "filename",
    "label",
    "path",
    "size_bytes",
    "sha256",
    "group_id",
    "group_size",
    "n_group_labels",
    "group_labels",
    "is_mixed_label_group",
]
TRAIN_GROUP_COLUMNS = [
    "group_id",
    "sha256",
    "size",
    "n_labels",
    "labels",
    "majority_label",
    "is_mixed_label",
    "members",
]
TRAIN_PAIR_COLUMNS = [
    "group_id",
    "sha256",
    "record_id_a",
    "filename_a",
    "label_a",
    "record_id_b",
    "filename_b",
    "label_b",
    "same_label",
]
TRAIN_REVIEW_COLUMNS = [
    "review_rank",
    "priority",
    "review_reason",
    "group_id",
    "sha256",
    "size",
    "n_labels",
    "labels",
    "is_mixed_label",
    "members",
]
WITH_TEST_MEMBER_COLUMNS = [
    "node",
    "record_id",
    "source",
    "filename",
    "label",
    "path",
    "size_bytes",
    "sha256",
    "group_id",
    "group_size",
    "n_train",
    "n_test",
    "has_train_test_overlap",
    "n_train_labels",
    "train_labels",
    "is_mixed_train_label",
]
WITH_TEST_GROUP_COLUMNS = [
    "group_id",
    "sha256",
    "size",
    "n_train",
    "n_test",
    "has_train",
    "has_test",
    "has_train_test_overlap",
    "n_train_labels",
    "train_labels",
    "is_mixed_train_label",
    "members",
]
WITH_TEST_PAIR_COLUMNS = [
    "group_id",
    "sha256",
    "node_a",
    "record_id_a",
    "source_a",
    "filename_a",
    "label_a",
    "node_b",
    "record_id_b",
    "source_b",
    "filename_b",
    "label_b",
    "same_source",
    "same_train_label",
    "pair_type",
]
WITH_TEST_REVIEW_COLUMNS = [
    "review_rank",
    "priority",
    "review_reason",
    "group_id",
    "sha256",
    "size",
    "n_train",
    "n_test",
    "has_train_test_overlap",
    "n_train_labels",
    "train_labels",
    "is_mixed_train_label",
    "members",
]


@dataclass(frozen=True)
class RuntimePaths:
    kaggle: bool
    root: Path
    train_dir: Path
    test_dir: Path
    output_dir: Path


@dataclass(frozen=True)
class ImageRecord:
    record_id: str
    filename: str
    label: str
    path: Path
    source: str = "train"


def running_on_kaggle() -> bool:
    return Path("/kaggle/input").exists() or bool(os.getenv("KAGGLE_KERNEL_RUN_TYPE"))


def discover_repo_root() -> Path:
    seen: set[Path] = set()
    candidates: List[Path] = []
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
            candidates.append(candidate)
    return candidates[0] if candidates else Path.cwd().resolve()


def resolve_runtime_paths() -> RuntimePaths:
    if running_on_kaggle():
        return RuntimePaths(True, Path("/kaggle"), KAGGLE_TRAIN_DIR, KAGGLE_TEST_DIR, KAGGLE_OUTPUT_DIR)
    root = discover_repo_root()
    data_root = root / "dataset"
    return RuntimePaths(False, root, data_root / "train", data_root / "test", root / "output" / "raw_duplicates")


RUNTIME = resolve_runtime_paths()
KAGGLE = RUNTIME.kaggle
ROOT = RUNTIME.root
TRAIN_DIR = RUNTIME.train_dir
TEST_DIR = RUNTIME.test_dir
OUTPUT_DIR = RUNTIME.output_dir


def prefixed_node(source: str, record_id: str) -> str:
    return f"{source}::{record_id}"


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


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(HASH_CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_records(records: Sequence[ImageRecord], desc: str) -> tuple[Dict[str, str], Dict[str, int]]:
    hashes: Dict[str, str] = {}
    sizes: Dict[str, int] = {}
    for record in tqdm(records, desc=desc, leave=True):
        hashes[record.record_id] = sha256_file(record.path)
        sizes[record.record_id] = record.path.stat().st_size
    return hashes, sizes


def save_empty_plot(path: Path, title: str, message: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def save_group_size_hist(groups_df: pd.DataFrame, path: Path, title: str) -> None:
    if groups_df.empty:
        save_empty_plot(path, title, "No duplicate groups to visualize")
        return
    sizes = groups_df["size"].astype(int).to_numpy()
    bins = np.arange(0.5, sizes.max() + 1.5, 1.0)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(sizes, bins=bins, color="#2e86de", edgecolor="white")
    ax.set_title(title)
    ax.set_xlabel("Duplicate group size")
    ax.set_ylabel("Count")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def save_top_groups(groups_df: pd.DataFrame, path: Path, title: str, color_col: str) -> None:
    if groups_df.empty:
        save_empty_plot(path, title, "No duplicate groups to visualize")
        return
    plot_df = groups_df.head(20).sort_values("size", ascending=True)
    labels = [f"group_{int(group_id):03d}" for group_id in plot_df["group_id"]]
    colors = ["#c0392b" if int(flag) == 1 else "#2e86de" for flag in plot_df[color_col]]
    fig, ax = plt.subplots(figsize=(11, max(5, 0.4 * len(plot_df) + 1)))
    ax.barh(labels, plot_df["size"], color=colors)
    ax.set_title(title)
    ax.set_xlabel("Group size")
    ax.set_ylabel("Group")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def train_label_color(label: str) -> str:
    palette = {
        "realperson": "#2e86de",
        "fake_printed": "#e67e22",
        "fake_mannequin": "#8e44ad",
        "fake_mask": "#16a085",
        "fake_screen": "#c0392b",
        "fake_unknown": "#7f8c8d",
    }
    return palette.get(label, "#34495e")


def source_color(source: str) -> str:
    return {"train": "#2e86de", "test": "#f39c12"}.get(source, "#7f8c8d")


def group_members(row: pd.Series) -> List[str]:
    members = str(row.get("members", ""))
    return [member for member in members.split("|") if member]


def save_group_graph_grid(
    group_rows: pd.DataFrame,
    record_lookup: Dict[str, ImageRecord],
    path: Path,
    title: str,
    color_mode: str,
    top_n: int = 6,
) -> None:
    if group_rows.empty:
        save_empty_plot(path, title, "No duplicate groups to visualize")
        return

    plot_rows = group_rows[group_rows["size"] > 1].head(top_n).copy()
    if plot_rows.empty:
        save_empty_plot(path, title, "No multi-image duplicate groups to visualize")
        return

    n_panels = len(plot_rows)
    ncols = 2 if n_panels > 1 else 1
    nrows = int(np.ceil(n_panels / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, max(5, nrows * 5)))
    axes_arr = np.atleast_1d(axes).reshape(-1)
    fig.suptitle(title, fontsize=14)

    for ax, (_, row) in zip(axes_arr, plot_rows.iterrows()):
        nodes = group_members(row)
        graph = nx.complete_graph(nodes)
        pos = {nodes[0]: (0.0, 0.0)} if len(nodes) == 1 else nx.circular_layout(graph)

        if color_mode == "label":
            node_colors = [train_label_color(record_lookup[node].label) for node in graph.nodes()]
        else:
            node_colors = [source_color(record_lookup[node].source) for node in graph.nodes()]

        labels = {node: record_lookup[node].filename[:18] for node in graph.nodes()}
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#b2bec3", alpha=0.8, width=1.2)
        nx.draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            node_color=node_colors,
            node_size=700,
            edgecolors="white",
            linewidths=1.0,
        )
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8, ax=ax)

        group_id = int(row["group_id"])
        group_size = int(row["size"])
        if "n_test" in row.index:
            subtitle = f"group_{group_id:03d} | size={group_size} | train={int(row['n_train'])} test={int(row['n_test'])}"
        else:
            subtitle = f"group_{group_id:03d} | size={group_size} | labels={row['labels']}"
        ax.set_title(subtitle, fontsize=10)
        ax.axis("off")

    for ax in axes_arr[n_panels:]:
        ax.axis("off")

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def build_train_reports(
    records: Sequence[ImageRecord],
    hashes: Dict[str, str],
    sizes: Dict[str, int],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    record_by_id = {record.record_id: record for record in records}
    groups: Dict[str, List[str]] = defaultdict(list)
    for record in records:
        groups[hashes[record.record_id]].append(record.record_id)

    group_rows: List[dict] = []
    member_rows: List[dict] = []
    pair_rows: List[dict] = []

    for group_id, (sha256, record_ids) in enumerate(
        sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    ):
        record_ids = sorted(record_ids)
        labels = sorted({record_by_id[record_id].label for record_id in record_ids})
        label_counter = Counter(record_by_id[record_id].label for record_id in record_ids)
        group_rows.append(
            {
                "group_id": group_id,
                "sha256": sha256,
                "size": len(record_ids),
                "n_labels": len(labels),
                "labels": "|".join(labels),
                "majority_label": label_counter.most_common(1)[0][0],
                "is_mixed_label": int(len(labels) > 1),
                "members": "|".join(record_ids),
            }
        )
        for record_id in record_ids:
            record = record_by_id[record_id]
            member_rows.append(
                {
                    "record_id": record.record_id,
                    "filename": record.filename,
                    "label": record.label,
                    "path": str(record.path),
                    "size_bytes": sizes[record.record_id],
                    "sha256": sha256,
                    "group_id": group_id,
                    "group_size": len(record_ids),
                    "n_group_labels": len(labels),
                    "group_labels": "|".join(labels),
                    "is_mixed_label_group": int(len(labels) > 1),
                }
            )
        if len(record_ids) > 1:
            for record_id_a, record_id_b in itertools.combinations(record_ids, 2):
                record_a = record_by_id[record_id_a]
                record_b = record_by_id[record_id_b]
                pair_rows.append(
                    {
                        "group_id": group_id,
                        "sha256": sha256,
                        "record_id_a": record_a.record_id,
                        "filename_a": record_a.filename,
                        "label_a": record_a.label,
                        "record_id_b": record_b.record_id,
                        "filename_b": record_b.filename,
                        "label_b": record_b.label,
                        "same_label": int(record_a.label == record_b.label),
                    }
                )

    members_df = pd.DataFrame(member_rows, columns=TRAIN_MEMBER_COLUMNS)
    groups_df = pd.DataFrame(group_rows, columns=TRAIN_GROUP_COLUMNS)
    pairs_df = pd.DataFrame(pair_rows, columns=TRAIN_PAIR_COLUMNS)
    duplicates_df = members_df[members_df["group_size"] > 1].copy() if not members_df.empty else members_df.copy()

    if not members_df.empty:
        members_df = members_df.sort_values(["group_id", "label", "record_id", "filename"])
    if not groups_df.empty:
        groups_df = groups_df.sort_values(["size", "group_id"], ascending=[False, True])
    if not duplicates_df.empty:
        duplicates_df = duplicates_df.sort_values(["group_size", "group_id", "label", "record_id"], ascending=[False, True, True, True])
    if not pairs_df.empty:
        pairs_df = pairs_df.sort_values(["group_id", "record_id_a", "record_id_b"])
    return members_df, groups_df, duplicates_df, pairs_df


def build_with_test_reports(
    records: Sequence[ImageRecord],
    hashes_by_node: Dict[str, str],
    sizes_by_node: Dict[str, int],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    record_by_node = {prefixed_node(record.source, record.record_id): record for record in records}
    groups: Dict[str, List[str]] = defaultdict(list)
    for node, sha256 in hashes_by_node.items():
        groups[sha256].append(node)

    group_rows: List[dict] = []
    member_rows: List[dict] = []
    pair_rows: List[dict] = []

    for group_id, (sha256, nodes) in enumerate(sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))):
        nodes = sorted(nodes)
        train_labels = sorted({record_by_node[node].label for node in nodes if record_by_node[node].source == "train"})
        n_train = sum(1 for node in nodes if record_by_node[node].source == "train")
        n_test = sum(1 for node in nodes if record_by_node[node].source == "test")
        group_rows.append(
            {
                "group_id": group_id,
                "sha256": sha256,
                "size": len(nodes),
                "n_train": n_train,
                "n_test": n_test,
                "has_train": int(n_train > 0),
                "has_test": int(n_test > 0),
                "has_train_test_overlap": int(n_train > 0 and n_test > 0),
                "n_train_labels": len(train_labels),
                "train_labels": "|".join(train_labels),
                "is_mixed_train_label": int(len(train_labels) > 1),
                "members": "|".join(nodes),
            }
        )
        for node in nodes:
            record = record_by_node[node]
            member_rows.append(
                {
                    "node": node,
                    "record_id": record.record_id,
                    "source": record.source,
                    "filename": record.filename,
                    "label": record.label,
                    "path": str(record.path),
                    "size_bytes": sizes_by_node[node],
                    "sha256": sha256,
                    "group_id": group_id,
                    "group_size": len(nodes),
                    "n_train": n_train,
                    "n_test": n_test,
                    "has_train_test_overlap": int(n_train > 0 and n_test > 0),
                    "n_train_labels": len(train_labels),
                    "train_labels": "|".join(train_labels),
                    "is_mixed_train_label": int(len(train_labels) > 1),
                }
            )
        if len(nodes) > 1:
            for node_a, node_b in itertools.combinations(nodes, 2):
                record_a = record_by_node[node_a]
                record_b = record_by_node[node_b]
                pair_rows.append(
                    {
                        "group_id": group_id,
                        "sha256": sha256,
                        "node_a": node_a,
                        "record_id_a": record_a.record_id,
                        "source_a": record_a.source,
                        "filename_a": record_a.filename,
                        "label_a": record_a.label,
                        "node_b": node_b,
                        "record_id_b": record_b.record_id,
                        "source_b": record_b.source,
                        "filename_b": record_b.filename,
                        "label_b": record_b.label,
                        "same_source": int(record_a.source == record_b.source),
                        "same_train_label": int(
                            record_a.source == "train"
                            and record_b.source == "train"
                            and record_a.label == record_b.label
                        ),
                        "pair_type": f"{record_a.source}-{record_b.source}" if record_a.source <= record_b.source else f"{record_b.source}-{record_a.source}",
                    }
                )

    members_df = pd.DataFrame(member_rows, columns=WITH_TEST_MEMBER_COLUMNS)
    groups_df = pd.DataFrame(group_rows, columns=WITH_TEST_GROUP_COLUMNS)
    pairs_df = pd.DataFrame(pair_rows, columns=WITH_TEST_PAIR_COLUMNS)
    duplicates_df = members_df[members_df["group_size"] > 1].copy() if not members_df.empty else members_df.copy()

    if not members_df.empty:
        members_df = members_df.sort_values(["group_id", "source", "record_id", "filename"])
    if not groups_df.empty:
        groups_df = groups_df.sort_values(["size", "group_id"], ascending=[False, True])
    if not duplicates_df.empty:
        duplicates_df = duplicates_df.sort_values(["group_size", "group_id", "source", "record_id"], ascending=[False, True, True, True])
    if not pairs_df.empty:
        pairs_df = pairs_df.sort_values(["group_id", "node_a", "node_b"])
    return members_df, groups_df, duplicates_df, pairs_df


def summary_text_train(records: Sequence[ImageRecord], groups_df: pd.DataFrame, duplicates_df: pd.DataFrame) -> str:
    duplicate_groups = groups_df[groups_df["size"] > 1] if not groups_df.empty else pd.DataFrame()
    mixed_groups = duplicate_groups[duplicate_groups["is_mixed_label"] == 1] if not duplicate_groups.empty else pd.DataFrame()
    lines = [
        "Raw train exact-duplicate summary",
        f"train_dir={TRAIN_DIR}",
        "method=sha256(raw_file_bytes)",
        "",
        f"total_images={len(records)}",
        f"groups={len(groups_df)}",
        f"duplicate_groups={len(duplicate_groups)}",
        f"duplicate_images={len(duplicates_df)}",
        f"singleton_groups={int((groups_df['size'] == 1).sum()) if not groups_df.empty else len(records)}",
        f"mixed_label_duplicate_groups={len(mixed_groups)}",
        f"images_in_mixed_label_duplicate_groups={int(mixed_groups['size'].sum()) if not mixed_groups.empty else 0}",
        "",
        "top_10_duplicate_groups:",
    ]
    if duplicate_groups.empty:
        lines.append("  none")
    else:
        for _, row in duplicate_groups.head(10).iterrows():
            lines.append(
                f"  group_{int(row['group_id']):03d} size={int(row['size'])} labels={row['labels']} mixed={int(row['is_mixed_label'])}"
            )
    return "\n".join(lines) + "\n"


def summary_text_with_test(records: Sequence[ImageRecord], groups_df: pd.DataFrame, duplicates_df: pd.DataFrame) -> str:
    overlap_groups = groups_df[groups_df["has_train_test_overlap"] == 1] if not groups_df.empty else pd.DataFrame()
    lines = [
        "Raw train+test exact-duplicate summary",
        f"train_dir={TRAIN_DIR}",
        f"test_dir={TEST_DIR}",
        "method=sha256(raw_file_bytes)",
        "",
        f"total_images={len(records)}",
        f"total_train={sum(1 for record in records if record.source == 'train')}",
        f"total_test={sum(1 for record in records if record.source == 'test')}",
        f"groups={len(groups_df)}",
        f"duplicate_groups={int((groups_df['size'] > 1).sum()) if not groups_df.empty else 0}",
        f"duplicate_images={len(duplicates_df)}",
        f"train_test_overlap_groups={len(overlap_groups)}",
        f"test_images_in_overlap_groups={int(overlap_groups['n_test'].sum()) if not overlap_groups.empty else 0}",
        "",
        "top_10_overlap_groups:",
    ]
    if overlap_groups.empty:
        lines.append("  none")
    else:
        overlap_sorted = overlap_groups.sort_values(["n_test", "size", "group_id"], ascending=[False, False, True])
        for _, row in overlap_sorted.head(10).iterrows():
            lines.append(
                f"  group_{int(row['group_id']):03d} size={int(row['size'])} n_train={int(row['n_train'])} n_test={int(row['n_test'])} train_labels={row['train_labels']}"
            )
    return "\n".join(lines) + "\n"


def build_train_review_queue(groups_df: pd.DataFrame) -> pd.DataFrame:
    if groups_df.empty:
        return pd.DataFrame(columns=TRAIN_REVIEW_COLUMNS)

    review_df = groups_df[groups_df["size"] > 1].copy()
    if review_df.empty:
        return pd.DataFrame(columns=TRAIN_REVIEW_COLUMNS)

    priority = []
    review_reason = []
    for _, row in review_df.iterrows():
        if int(row["is_mixed_label"]) == 1 and int(row["size"]) >= 3:
            priority.append("highest")
            review_reason.append("exact duplicate across labels")
        elif int(row["is_mixed_label"]) == 1:
            priority.append("high")
            review_reason.append("cross-label exact duplicate")
        elif int(row["size"]) >= 3:
            priority.append("medium")
            review_reason.append("same-label repeated exact duplicate")
        else:
            priority.append("low")
            review_reason.append("same-label duplicate pair")

    review_df["priority"] = priority
    review_df["review_reason"] = review_reason
    review_df = review_df.sort_values(
        ["is_mixed_label", "size", "group_id"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    review_df["review_rank"] = np.arange(1, len(review_df) + 1)
    return review_df[
        [
            "review_rank",
            "priority",
            "review_reason",
            "group_id",
            "sha256",
            "size",
            "n_labels",
            "labels",
            "is_mixed_label",
            "members",
        ]
    ].copy()


def build_with_test_review_queue(groups_df: pd.DataFrame) -> pd.DataFrame:
    if groups_df.empty:
        return pd.DataFrame(columns=WITH_TEST_REVIEW_COLUMNS)

    review_df = groups_df[groups_df["has_train_test_overlap"] == 1].copy()
    if review_df.empty:
        return pd.DataFrame(columns=WITH_TEST_REVIEW_COLUMNS)

    priority = []
    review_reason = []
    for _, row in review_df.iterrows():
        if int(row["n_test"]) >= 2 and int(row["is_mixed_train_label"]) == 1:
            priority.append("highest")
            review_reason.append("multiple test files overlap mixed-label train duplicates")
        elif int(row["n_test"]) >= 2:
            priority.append("high")
            review_reason.append("multiple test files exactly overlap train")
        elif int(row["is_mixed_train_label"]) == 1:
            priority.append("high")
            review_reason.append("test overlaps mixed-label train duplicate")
        else:
            priority.append("medium")
            review_reason.append("test overlaps train exact duplicate")

    review_df["priority"] = priority
    review_df["review_reason"] = review_reason
    review_df = review_df.sort_values(
        ["n_test", "size", "is_mixed_train_label", "group_id"],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)
    review_df["review_rank"] = np.arange(1, len(review_df) + 1)
    return review_df[
        [
            "review_rank",
            "priority",
            "review_reason",
            "group_id",
            "sha256",
            "size",
            "n_train",
            "n_test",
            "has_train_test_overlap",
            "n_train_labels",
            "train_labels",
            "is_mixed_train_label",
            "members",
        ]
    ].copy()


def zip_output_dir(output_dir: Path) -> Path:
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(output_dir.parent))
    return zip_path


def run_self_tests() -> None:
    records = [
        ImageRecord("realperson/a.jpg", "a.jpg", "realperson", Path("realperson") / "a.jpg", "train"),
        ImageRecord("fake_mask/b.jpg", "b.jpg", "fake_mask", Path("fake_mask") / "b.jpg", "train"),
        ImageRecord("realperson/c.jpg", "c.jpg", "realperson", Path("realperson") / "c.jpg", "train"),
    ]
    hashes = {
        "realperson/a.jpg": "aaa",
        "fake_mask/b.jpg": "aaa",
        "realperson/c.jpg": "ccc",
    }
    sizes = {record.record_id: 123 for record in records}
    members_df, groups_df, duplicates_df, pairs_df = build_train_reports(records, hashes, sizes)
    assert len(groups_df) == 2
    assert len(duplicates_df) == 2
    assert len(pairs_df) == 1
    assert int(groups_df.iloc[0]["is_mixed_label"]) == 1

    combined_records = records + [ImageRecord("a.jpg", "a.jpg", "", Path("test") / "a.jpg", "test")]
    combined_hashes = {
        prefixed_node("train", "realperson/a.jpg"): "aaa",
        prefixed_node("train", "fake_mask/b.jpg"): "aaa",
        prefixed_node("train", "realperson/c.jpg"): "ccc",
        prefixed_node("test", "a.jpg"): "aaa",
    }
    combined_sizes = {node: 123 for node in combined_hashes}
    with_test_members, with_test_groups, with_test_duplicates, with_test_pairs = build_with_test_reports(
        combined_records,
        combined_hashes,
        combined_sizes,
    )
    assert len(with_test_groups) == 2
    assert len(with_test_duplicates) == 3
    assert len(with_test_pairs) == 3
    assert int(with_test_groups.iloc[0]["has_train_test_overlap"]) == 1
    assert int(with_test_groups.iloc[0]["n_test"]) == 1
    print("Self-test passed.")


print(f"KAGGLE      : {KAGGLE}")
print(f"ROOT        : {ROOT}")
print(f"TRAIN_DIR   : {TRAIN_DIR}")
print(f"TEST_DIR    : {TEST_DIR}")
print(f"OUTPUT_DIR  : {OUTPUT_DIR}")

if RUN_SELF_TEST:
    run_self_tests()
else:
    train_records = collect_train_records(TRAIN_DIR)
    test_records = collect_test_records(TEST_DIR)
    if not train_records:
        raise RuntimeError(f"No train images found under {TRAIN_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train_hashes, train_sizes = hash_records(train_records, desc="Hash train files")
    if test_records:
        test_hashes, test_sizes = hash_records(test_records, desc="Hash test files")
    else:
        test_hashes, test_sizes = {}, {}
        print(f"No test images found under {TEST_DIR}; combined report will contain train data only.")

    train_members_df, train_groups_df, train_duplicates_df, train_pairs_df = build_train_reports(
        train_records,
        train_hashes,
        train_sizes,
    )

    train_members_path = OUTPUT_DIR / "raw_train_members_sha256.csv"
    train_groups_path = OUTPUT_DIR / "raw_train_groups_sha256.csv"
    train_duplicates_path = OUTPUT_DIR / "raw_train_duplicates_sha256.csv"
    train_pairs_path = OUTPUT_DIR / "raw_train_pairs_sha256.csv"
    train_review_queue_path = OUTPUT_DIR / "raw_train_review_queue_sha256.csv"
    train_summary_path = OUTPUT_DIR / "raw_train_summary.txt"
    train_group_sizes_path = OUTPUT_DIR / "raw_train_group_sizes_sha256.png"
    train_group_graphs_path = OUTPUT_DIR / "raw_train_group_graphs_sha256.png"
    train_top_groups_path = OUTPUT_DIR / "raw_train_top_groups_sha256.png"
    train_review_queue_df = build_train_review_queue(train_groups_df)

    train_members_df.to_csv(train_members_path, index=False)
    train_groups_df.to_csv(train_groups_path, index=False)
    train_duplicates_df.to_csv(train_duplicates_path, index=False)
    train_pairs_df.to_csv(train_pairs_path, index=False)
    train_review_queue_df.to_csv(train_review_queue_path, index=False)
    train_summary_path.write_text(
        summary_text_train(train_records, train_groups_df, train_duplicates_df),
        encoding="utf-8",
    )
    save_group_size_hist(
        train_groups_df[train_groups_df["size"] > 1],
        train_group_sizes_path,
        "Train exact-duplicate group size distribution",
    )
    save_group_graph_grid(
        train_groups_df,
        {record.record_id: record for record in train_records},
        train_group_graphs_path,
        "Largest train exact-duplicate groups",
        color_mode="label",
    )
    save_top_groups(
        train_groups_df[train_groups_df["size"] > 1],
        train_top_groups_path,
        "Largest train exact-duplicate groups",
        color_col="is_mixed_label",
    )

    combined_records = train_records + test_records
    combined_hashes = {prefixed_node("train", record.record_id): train_hashes[record.record_id] for record in train_records}
    combined_hashes.update({prefixed_node("test", record.record_id): test_hashes[record.record_id] for record in test_records})
    combined_sizes = {prefixed_node("train", record.record_id): train_sizes[record.record_id] for record in train_records}
    combined_sizes.update({prefixed_node("test", record.record_id): test_sizes[record.record_id] for record in test_records})

    with_test_members_df, with_test_groups_df, with_test_duplicates_df, with_test_pairs_df = build_with_test_reports(
        combined_records,
        combined_hashes,
        combined_sizes,
    )

    with_test_members_path = OUTPUT_DIR / "raw_with_test_members_sha256.csv"
    with_test_groups_path = OUTPUT_DIR / "raw_with_test_groups_sha256.csv"
    with_test_duplicates_path = OUTPUT_DIR / "raw_with_test_duplicates_sha256.csv"
    with_test_pairs_path = OUTPUT_DIR / "raw_with_test_pairs_sha256.csv"
    with_test_review_queue_path = OUTPUT_DIR / "raw_with_test_review_queue_sha256.csv"
    with_test_summary_path = OUTPUT_DIR / "raw_with_test_summary.txt"
    with_test_overlap_groups_path = OUTPUT_DIR / "raw_with_test_overlap_groups_sha256.png"
    with_test_overlap_graphs_path = OUTPUT_DIR / "raw_with_test_overlap_graphs_sha256.png"
    with_test_review_queue_df = build_with_test_review_queue(with_test_groups_df)

    with_test_members_df.to_csv(with_test_members_path, index=False)
    with_test_groups_df.to_csv(with_test_groups_path, index=False)
    with_test_duplicates_df.to_csv(with_test_duplicates_path, index=False)
    with_test_pairs_df.to_csv(with_test_pairs_path, index=False)
    with_test_review_queue_df.to_csv(with_test_review_queue_path, index=False)
    with_test_summary_path.write_text(
        summary_text_with_test(combined_records, with_test_groups_df, with_test_duplicates_df),
        encoding="utf-8",
    )
    save_top_groups(
        with_test_groups_df[with_test_groups_df["has_train_test_overlap"] == 1],
        with_test_overlap_groups_path,
        "Largest train-test exact-overlap groups",
        color_col="is_mixed_train_label",
    )
    save_group_graph_grid(
        with_test_groups_df[with_test_groups_df["has_train_test_overlap"] == 1],
        {prefixed_node(record.source, record.record_id): record for record in combined_records},
        with_test_overlap_graphs_path,
        "Largest train-test exact-overlap groups",
        color_mode="source",
    )

    print(f"train images           : {len(train_records)}")
    print(f"test images            : {len(test_records)}")
    print(f"train duplicate groups : {int((train_groups_df['size'] > 1).sum()) if not train_groups_df.empty else 0}")
    print(f"train duplicate images : {len(train_duplicates_df)}")
    print(f"train-test overlaps    : {int(with_test_groups_df['has_train_test_overlap'].sum()) if not with_test_groups_df.empty else 0}")
    print(f"saved                  : {train_members_path}")
    print(f"saved                  : {train_groups_path}")
    print(f"saved                  : {train_duplicates_path}")
    print(f"saved                  : {train_pairs_path}")
    print(f"saved                  : {train_review_queue_path}")
    print(f"saved                  : {train_summary_path}")
    print(f"saved                  : {train_group_sizes_path}")
    print(f"saved                  : {train_group_graphs_path}")
    print(f"saved                  : {train_top_groups_path}")
    print(f"saved                  : {with_test_members_path}")
    print(f"saved                  : {with_test_groups_path}")
    print(f"saved                  : {with_test_duplicates_path}")
    print(f"saved                  : {with_test_pairs_path}")
    print(f"saved                  : {with_test_review_queue_path}")
    print(f"saved                  : {with_test_summary_path}")
    print(f"saved                  : {with_test_overlap_groups_path}")
    print(f"saved                  : {with_test_overlap_graphs_path}")
    zip_path = zip_output_dir(OUTPUT_DIR)
    print(f"saved                  : {zip_path}")
