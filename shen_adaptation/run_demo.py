"""
run_demo.py — example wrapper that runs senescence_deswan on the G11BM data.

This script shows EXACTLY how to plug your existing pipeline outputs into
the DE-SWAN module. Read it once, then adapt the file paths / cell type as you wish.

Usage:
    cd /hpc/home/gc237/work/claude_cloud/shen_adaptation
    # activate your scanpy env first (the one your bm_final_analysis.py uses)
    python run_demo.py --celltype Monocytes --condition Veh
    python run_demo.py --celltype HSPC --condition DQ
    python run_demo.py --celltype Monocytes --condition both    # combines V+DQ

Outputs go to ./output/<celltype>_<condition>/ :
    - crest_<celltype>.png  ← the headline figure
    - deswan_<celltype>.csv ← per-window n_significant + top genes
    - per_gene_peaks_<celltype>.csv ← per-gene peak score (for ranking)

Compute notes:
- Memory: loads the focal cell-type subset of the full adata into RAM.
  Monocytes (~30k cells × ~25k genes) ≈ 3 GB dense. Should fit on any
  HPC interactive node. For HSPC (~5k cells) it's trivial.
- Wall time: ~1-5 min per cell type on a single core.
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc

# Allow running from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent))
from senescence_deswan import run_senescence_deswan  # noqa: E402


G11BM_ROOT = Path("/hpc/group/vargheselab/gc237/storage/Python/Scanpy/code_for_G11BM")
ADATA_PATH = G11BM_ROOT / "output_final/adata/adata_all_drm_anno_fullannot.h5ad"
SCORES_PATH = G11BM_ROOT / "output_final/tables/senepy/percell_senescence_scores.csv"
SCORE_COLUMN = "sp_best"           # the SenePy "best hub" continuous score
CELLTYPE_COLUMN = "cell_type_coarse"  # in both adata.obs and the score CSV


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--celltype", required=True,
                    help="One of: Monocytes / HSPC / MSC / B-cell / T-cell / "
                         "Neutrophil / Erythroid / Plasma / Macrophage / NK / "
                         "Mast / cDC / pDC / Platelet / etc. (must match "
                         "cell_type_coarse in the adata)")
    ap.add_argument("--condition", default="both",
                    choices=["Veh", "DQ", "both"],
                    help="Subset to one condition or use both")
    ap.add_argument("--n-bins", type=int, default=30,
                    help="Number of senescence-score bins (default 30)")
    ap.add_argument("--out", default="./output", help="Output directory")
    ap.add_argument("--score-column", default=SCORE_COLUMN,
                    help=f"Column in {SCORES_PATH.name} (default {SCORE_COLUMN})")
    args = ap.parse_args()

    out_dir = Path(args.out) / f"{args.celltype}_{args.condition}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/5] Loading {ADATA_PATH}")
    adata = sc.read_h5ad(ADATA_PATH)
    print(f"   adata: {adata.shape[0]:,} cells × {adata.shape[1]:,} genes")
    print(f"   obs columns: {list(adata.obs.columns)[:10]}…")

    print(f"\n[2/5] Loading {SCORES_PATH}")
    scores = pd.read_csv(SCORES_PATH)
    if "cell_barcode" not in scores.columns:
        raise SystemExit(f"Expected 'cell_barcode' column, got {list(scores.columns)}")
    scores = scores.set_index("cell_barcode")
    if args.score_column not in scores.columns:
        raise SystemExit(f"Score column '{args.score_column}' not in CSV. "
                         f"Available: {list(scores.columns)}")

    print(f"\n[3/5] Subsetting to celltype={args.celltype} · condition={args.condition}")
    if CELLTYPE_COLUMN not in adata.obs:
        # try alternative annotation columns
        for c in ("cell_type", "celltype", "ct", "annotation"):
            if c in adata.obs.columns:
                print(f"   '{CELLTYPE_COLUMN}' missing; using '{c}'")
                celltype_col = c
                break
        else:
            raise SystemExit(f"No celltype column found in adata.obs.")
    else:
        celltype_col = CELLTYPE_COLUMN
    mask_ct = adata.obs[celltype_col].astype(str) == args.celltype
    if args.condition != "both":
        mask_cond = adata.obs["Condition"].astype(str) == args.condition
        mask_ct = mask_ct & mask_cond
    n_ct = mask_ct.sum()
    print(f"   {n_ct:,} cells in {args.celltype}/{args.condition}")
    if n_ct < 500:
        print("   ⚠️  fewer than 500 cells — DE-SWAN crests will be noisy. Proceeding anyway.")
    adata_sub = adata[mask_ct].copy()

    # match cells with scores
    cells = adata_sub.obs.index.intersection(scores.index)
    adata_sub = adata_sub[cells].copy()
    score_vec = scores.loc[adata_sub.obs.index, args.score_column].values.astype(float)
    print(f"   {len(cells):,} cells matched between adata and senepy score table")

    # log-normalize if not already
    print(f"\n[4/5] Ensuring log-normalized expression matrix")
    if "log1p" not in adata_sub.uns and adata_sub.X.max() > 50:
        print("   running sc.pp.normalize_total + sc.pp.log1p")
        sc.pp.normalize_total(adata_sub, target_sum=1e4)
        sc.pp.log1p(adata_sub)
    else:
        print("   appears already log-normalized")

    # Optional: drop genes specific to this cell type's senepy hub (if you want
    # extra protection against circularity beyond SenMayo). The hub-gene lists
    # for each celltype live in your senepy_celltype_thr_stats.csv if you
    # parse the 'hub_name' column. We skip that for the demo.
    extra_drop: list[str] = []

    print(f"\n[5/5] Running DE-SWAN scan with {args.n_bins} bins")
    label = f"{args.celltype}_{args.condition}"
    result = run_senescence_deswan(
        X=adata_sub.X,
        gene_names=list(adata_sub.var_names),
        score=score_vec,
        cell_type_label=label,
        n_bins=args.n_bins,
        alpha=0.05,
        extra_genes_to_drop=extra_drop,
        output_dir=str(out_dir),
    )

    print("\n=== Summary ===")
    print(f"Output dir: {out_dir.resolve()}")
    print(f"Top 5 windows by significant-gene count:")
    print(result["deswan"].sort_values("n_significant", ascending=False).head(5)[["n_significant", "top_genes"]])
    print(f"\nTop 10 'tipping' genes by smallest peak q-value:")
    print(result["per_gene"].head(10).to_string(index=False))
    print(f"\nCrest plot: {out_dir / f'crest_{label}.png'}")


if __name__ == "__main__":
    main()
