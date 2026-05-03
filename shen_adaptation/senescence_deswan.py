"""
senescence_deswan.py
====================

Adaptation of Shen et al. 2024 (Nature Aging) DE-SWAN sliding-window analysis
to single-cell RNA-seq data, using *per-cell senescence score* as the
"age axis" instead of chronological age.

Why this is useful for the G11BM project
----------------------------------------
Shen et al. discovered that human aging is non-linear: most molecules change
at specific ages (~44 and ~60), not gradually. They used DE-SWAN
(Differential Expression Sliding Window ANalysis, Lehallier et al. 2019)
on individuals ordered by chronological age.

Your G11BM scRNA-seq data has continuous SenePy senescence scores per cell.
Substituting score for age, DE-SWAN can identify *senescence thresholds* —
score values beyond which gene-expression patterns rewire en masse. These
thresholds may mark where a cell becomes "biologically senescent" in
the molecular sense, and DQ vs Veh comparisons of the threshold
location/sharpness are a new mechanistic axis you don't currently use.

Algorithm
---------
1. Filter to one cell type (per-cell-type analysis avoids identity-driven
   variance overwhelming senescence-driven variance).
2. Bin cells along the senescence score axis into N equal-cell-count bins.
3. Pseudobulk: per bin, compute mean log-normalized expression per gene.
   This gives N "pseudo-individuals" with a single score = bin midpoint.
4. DE-SWAN sliding window: for each window center w with bucket size b,
   take bins where midpoint in [w - b/2, w + b/2], split at the within-window
   median, and for each gene run a Welch t-test between low vs high halves.
   FDR-correct (Benjamini-Hochberg) the per-gene p-values within the window.
   Count significant genes (q < alpha).
5. Plot significant-gene count vs window center → crests mark senescence
   thresholds at which many genes simultaneously transition.

Anti-circularity
----------------
The SenePy score is itself derived from gene expression, so testing
"which genes change with score" is tautological for the score-defining
genes. We mitigate this by:
- Excluding the canonical SenMayo gene list (the senescence markers that
  show up most often in senescence-scoring panels).
- Optionally excluding any user-supplied gene list (e.g., your custom
  SenePy hub genes for the focal cell type).
- Reporting the cor(score, expression) per gene so you can post-hoc
  drop highly score-correlated genes if you suspect leakage.

Inputs
------
- A cells × genes log-normalized expression matrix (numpy or scipy.sparse)
- A vector of senescence scores (one per cell)
- A list of gene names matching the matrix columns
- Optional: cell type vector if you want per-cell-type analysis
- Optional: condition vector if you want Veh vs DQ comparison

Outputs
-------
- A DataFrame: window_center, n_significant, top_genes
- A matplotlib crest plot (saved to disk)
- A per-gene table: gene, peak_window_center, peak_qvalue, mean_low, mean_high

Author: Claude (Opus 4.7) for Giwon Cho's G11BM project, May 2026.
Method credit: Lehallier 2019 (DE-SWAN), Shen 2024 (senescence-axis adaptation).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats, sparse
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
from typing import Iterable


# Canonical SenMayo gene set (Saul et al. 2022, Nat Commun).
# Mouse symbols. Users with human data should convert via biomaRt or
# pre-existing ortholog tables in the G11BM repo.
SENMAYO_MOUSE = {
    "Acvr1b", "Ang", "Angpt1", "Angptl4", "Areg", "Axl", "Bex3", "Bmp2", "Bmp6",
    "C3", "Ccl1", "Ccl13", "Ccl16", "Ccl2", "Ccl20", "Ccl24", "Ccl26", "Ccl3",
    "Ccl4", "Ccl5", "Ccl7", "Ccl8", "Cd55", "Cd9", "Csf1", "Csf2", "Csf2rb",
    "Cst10", "Ctnnb1", "Ctsb", "Cxcl1", "Cxcl10", "Cxcl12", "Cxcl16", "Cxcl2",
    "Cxcl3", "Cxcr2", "Dkk1", "Edn1", "Egf", "Egfr", "Ereg", "Esm1", "Ets2",
    "Fas", "Fgf1", "Fgf2", "Fgf7", "Gdf15", "Gem", "Gmfg", "Hgf", "Hmgb1",
    "Icam1", "Icam3", "Igf1", "Igfbp1", "Igfbp2", "Igfbp3", "Igfbp4", "Igfbp5",
    "Igfbp6", "Igfbp7", "Il10", "Il13", "Il15", "Il18", "Il1a", "Il1b", "Il2",
    "Il6", "Il6st", "Il7", "Inha", "Iqgap2", "Itga2", "Itpka", "Jun", "Kitl",
    "Lcp1", "Mif", "Mmp10", "Mmp12", "Mmp13", "Mmp14", "Mmp2", "Mmp3", "Mmp9",
    "Nap1l4", "Nrg1", "Pappa", "Pecam1", "Pgf", "Pigf", "Plat", "Plau", "Plaur",
    "Ppbp", "Ptbp1", "Ptger2", "Ptges", "Rps6ka5", "Scamp4", "Selplg", "Sema3f",
    "Serpinb2", "Serpine1", "Serpine2", "Spp1", "Spx", "Timp2", "Tnf", "Tnfrsf10c",
    "Tnfrsf11b", "Tnfrsf1a", "Tnfrsf1b", "Tubgcp2", "Vegfa", "Vegfc", "Vgf",
    "Wnt16", "Wnt2",
}


def _to_dense_log(X) -> np.ndarray:
    """Densify if sparse. Caller must already have log-normalized data."""
    if sparse.issparse(X):
        return X.toarray()
    return np.asarray(X)


def bin_cells_by_score(
    score: np.ndarray,
    n_bins: int = 30,
    strategy: str = "equal_count",
) -> np.ndarray:
    """
    Assign each cell to a bin based on senescence score.

    Parameters
    ----------
    score : 1D array of senescence scores, one per cell.
    n_bins : number of bins. 20-50 is reasonable for ~10k+ cells.
    strategy : 'equal_count' (default) gives bins with equal cell counts,
               yielding stable per-bin pseudobulks. 'equal_width' gives
               score-uniform bins; useful if the score distribution is
               heavily skewed and you want to preserve tail information.

    Returns
    -------
    bin_idx : 1D int array of bin assignments (0 .. n_bins-1).
    """
    score = np.asarray(score)
    if strategy == "equal_count":
        edges = np.quantile(score, np.linspace(0, 1, n_bins + 1))
        # nudge last edge to include max
        edges[-1] += 1e-9
    elif strategy == "equal_width":
        edges = np.linspace(score.min(), score.max() + 1e-9, n_bins + 1)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    bin_idx = np.digitize(score, edges[1:-1])
    return bin_idx


def pseudobulk_by_bin(
    X: np.ndarray | sparse.spmatrix,
    bin_idx: np.ndarray,
    score: np.ndarray,
    n_bins: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Mean log-normalized expression per bin.

    Returns
    -------
    pb : (n_bins, n_genes) array of per-bin mean expression.
    bin_score : (n_bins,) array of mean senescence score per bin.
    """
    X = _to_dense_log(X)
    pb = np.zeros((n_bins, X.shape[1]), dtype=np.float32)
    bin_score = np.zeros(n_bins, dtype=np.float32)
    for b in range(n_bins):
        mask = bin_idx == b
        if mask.sum() == 0:
            pb[b] = np.nan
            bin_score[b] = np.nan
            continue
        pb[b] = X[mask].mean(axis=0)
        bin_score[b] = score[mask].mean()
    # drop empty bins
    keep = ~np.isnan(bin_score)
    return pb[keep], bin_score[keep]


def deswan_window(
    pb: np.ndarray,
    bin_score: np.ndarray,
    window_center: float,
    bucket_size: float,
    alpha: float = 0.05,
) -> tuple[int, np.ndarray, np.ndarray]:
    """
    DE-SWAN at one window center.

    Within bins whose score lies in [w - bucket/2, w + bucket/2], split at
    the within-window median into low and high halves, then per-gene
    Welch's t-test between halves. FDR (BH) within the window.

    Returns
    -------
    n_sig : count of genes with q < alpha
    qvals : per-gene q-values (length = n_genes)
    direction : per-gene sign of (mean_high - mean_low)
    """
    lo, hi = window_center - bucket_size / 2.0, window_center + bucket_size / 2.0
    in_win = (bin_score >= lo) & (bin_score <= hi)
    n_in = in_win.sum()
    if n_in < 4:
        return 0, np.full(pb.shape[1], np.nan), np.zeros(pb.shape[1])
    sub = pb[in_win]
    sub_score = bin_score[in_win]
    median_score = np.median(sub_score)
    low_mask = sub_score < median_score
    high_mask = ~low_mask
    if low_mask.sum() < 2 or high_mask.sum() < 2:
        return 0, np.full(pb.shape[1], np.nan), np.zeros(pb.shape[1])
    low = sub[low_mask]
    high = sub[high_mask]
    # vectorized Welch's t per gene
    t_stat, p_val = stats.ttest_ind(high, low, axis=0, equal_var=False, nan_policy="omit")
    p_val = np.where(np.isnan(p_val), 1.0, p_val)
    _, q_val, _, _ = multipletests(p_val, method="fdr_bh")
    direction = np.sign(np.nanmean(high, axis=0) - np.nanmean(low, axis=0))
    n_sig = int(np.sum(q_val < alpha))
    return n_sig, q_val, direction


def deswan_scan(
    pb: np.ndarray,
    bin_score: np.ndarray,
    gene_names: list[str],
    window_centers: np.ndarray | None = None,
    bucket_size: float | None = None,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Run DE-SWAN at many window centers along the score axis.

    Parameters
    ----------
    pb : (n_bins, n_genes) bin pseudobulk matrix
    bin_score : (n_bins,) score per bin
    gene_names : list of gene symbols (length n_genes)
    window_centers : axis values to test. If None, use a uniform grid spanning
                     the central 90% of bin_score range, with 30 points.
    bucket_size : window width. If None, use 20% of the score range
                  (Shen used 20 years out of ~50-yr span = 40%; but for
                  our data with bin pseudobulks we want narrower).
    alpha : FDR threshold for significance.

    Returns
    -------
    DataFrame indexed by window_center with columns:
        n_significant : count of genes q<alpha at that window
        top_genes : top-10 most-significant gene symbols (semicolon-joined)
    Plus a wide qvalue matrix accessible via .attrs['qvalues']
    (n_windows × n_genes) for downstream use.
    """
    score_range = bin_score.max() - bin_score.min()
    if window_centers is None:
        window_centers = np.linspace(
            bin_score.min() + 0.05 * score_range,
            bin_score.max() - 0.05 * score_range,
            30,
        )
    if bucket_size is None:
        bucket_size = 0.2 * score_range

    rows = []
    qmat = np.full((len(window_centers), pb.shape[1]), np.nan, dtype=np.float32)
    for i, w in enumerate(window_centers):
        n_sig, q, _ = deswan_window(pb, bin_score, w, bucket_size, alpha=alpha)
        qmat[i] = q
        # top 10 genes by q at this window
        if not np.all(np.isnan(q)):
            order = np.argsort(q)
            top = [gene_names[j] for j in order[:10] if q[j] < alpha]
        else:
            top = []
        rows.append({
            "window_center": float(w),
            "n_significant": n_sig,
            "top_genes": ";".join(top),
        })
    df = pd.DataFrame(rows).set_index("window_center")
    df.attrs["qvalues"] = qmat
    df.attrs["window_centers"] = np.array(window_centers)
    df.attrs["bucket_size"] = float(bucket_size)
    df.attrs["alpha"] = float(alpha)
    df.attrs["gene_names"] = list(gene_names)
    return df


def crest_plot(
    deswan_df: pd.DataFrame,
    title: str = "Senescence-axis DE-SWAN",
    output_path: str | None = None,
    annotate_top_n: int = 2,
) -> plt.Figure:
    """
    Plot significant-gene count vs window center. Crests mark senescence
    thresholds where many genes simultaneously transition.
    """
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    x = deswan_df.index.values
    y = deswan_df["n_significant"].values
    ax.fill_between(x, 0, y, color="#ffd6e7", alpha=0.5)
    ax.plot(x, y, color="#d63384", lw=2.5)
    ax.scatter(x, y, color="#d63384", s=18, zorder=5)
    # annotate top crests
    if annotate_top_n > 0:
        top_idx = np.argsort(y)[::-1][:annotate_top_n]
        for k, idx in enumerate(top_idx):
            color = "#5a4fcf" if k == 0 else "#ed7d31"
            ax.axvline(x[idx], color=color, lw=1.2, ls="--", alpha=0.7)
            ax.annotate(
                f"crest @ score={x[idx]:.2f}\n({int(y[idx])} genes)",
                xy=(x[idx], y[idx]), xytext=(0, 14),
                textcoords="offset points", ha="center",
                fontsize=10, color=color, fontweight="bold",
            )
    ax.set_xlabel("Senescence score (window center)", fontsize=11)
    ax.set_ylabel(f"# genes q<{deswan_df.attrs['alpha']:.2f}", fontsize=11)
    ax.set_title(title, fontsize=13, color="#5a4fcf", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=160, bbox_inches="tight")
    return fig


def per_gene_peak_table(
    deswan_df: pd.DataFrame,
    gene_names: list[str],
    pb: np.ndarray,
    bin_score: np.ndarray,
) -> pd.DataFrame:
    """
    For each gene, the window center where its q-value is minimal (its 'peak'),
    and the mean expression at the bottom vs top decile of score (for direction).

    Useful follow-up to crest_plot: the genes whose peak coincides with a
    crest are the ones driving the senescence threshold.
    """
    qmat = deswan_df.attrs["qvalues"]  # (n_windows, n_genes)
    centers = deswan_df.attrs["window_centers"]
    peak_window_idx = np.nanargmin(qmat, axis=0)
    peak_q = qmat[peak_window_idx, np.arange(qmat.shape[1])]
    peak_score = centers[peak_window_idx]
    # direction: mean of top-decile score bins minus bottom-decile
    decile_low = np.percentile(bin_score, 10)
    decile_high = np.percentile(bin_score, 90)
    low_mean = pb[bin_score <= decile_low].mean(axis=0)
    high_mean = pb[bin_score >= decile_high].mean(axis=0)
    log2fc = high_mean - low_mean  # log-space already
    return pd.DataFrame({
        "gene": gene_names,
        "peak_score": peak_score,
        "peak_qvalue": peak_q,
        "log2fc_high_vs_low_decile": log2fc,
    }).sort_values("peak_qvalue")


def filter_genes_for_circularity(
    gene_names: list[str],
    score: np.ndarray | None = None,
    X: np.ndarray | sparse.spmatrix | None = None,
    extra_drop: Iterable[str] = (),
    cor_threshold: float = 0.7,
) -> np.ndarray:
    """
    Return a boolean mask over genes. True = keep, False = drop.

    Drops:
    - Canonical SenMayo (mouse) — these are the senescence markers most
      likely to define your score panel.
    - Any user-supplied extra_drop list (e.g., your SenePy hub genes for
      the focal cell type — pull from senepy_celltype_thr_stats.csv).
    - If X and score are supplied, also drop genes with |Spearman| > cor_threshold
      with the score across cells (data-driven leakage check).
    """
    keep = np.ones(len(gene_names), dtype=bool)
    senmayo = SENMAYO_MOUSE | set(extra_drop)
    senmayo_lower = {g.lower() for g in senmayo}
    for i, g in enumerate(gene_names):
        if g.lower() in senmayo_lower:
            keep[i] = False
    n_dropped_panel = (~keep).sum()
    print(f"Dropped {n_dropped_panel} senescence-panel genes (SenMayo + extras).")

    if X is not None and score is not None:
        X_dense = _to_dense_log(X)
        # Spearman per gene (rank-based, robust to non-normality)
        # vectorize via stats.spearmanr column-by-column would be slow at scale;
        # use rankdata + Pearson trick
        score_rank = stats.rankdata(score)
        # rank cells per gene (axis=0)
        gene_ranks = stats.rankdata(X_dense, axis=0)
        score_centered = score_rank - score_rank.mean()
        gene_centered = gene_ranks - gene_ranks.mean(axis=0)
        cor = (
            (score_centered[:, None] * gene_centered).sum(axis=0)
            / np.sqrt((score_centered**2).sum() * (gene_centered**2).sum(axis=0) + 1e-12)
        )
        leaky = np.abs(cor) > cor_threshold
        keep &= ~leaky
        print(f"Dropped {leaky.sum()} extra genes with |Spearman(score)| > {cor_threshold}.")
    return keep


# -------------------------------------------------------------------
# High-level convenience: one-call pipeline.
# -------------------------------------------------------------------

def run_senescence_deswan(
    X,                              # cells × genes log-norm matrix (np or sparse)
    gene_names: list[str],          # length n_genes
    score: np.ndarray,              # length n_cells
    cell_type_label: str = "cells",
    n_bins: int = 30,
    alpha: float = 0.05,
    extra_genes_to_drop: Iterable[str] = (),
    output_dir: str | None = None,
) -> dict:
    """
    End-to-end:  X + score → crest plot + DE-SWAN df + per-gene table.
    Returns a dict so you can inspect everything programmatically.
    """
    keep_mask = filter_genes_for_circularity(
        gene_names, score=score, X=X, extra_drop=extra_genes_to_drop, cor_threshold=0.7,
    )
    X_filt = X[:, keep_mask] if not sparse.issparse(X) else X[:, np.where(keep_mask)[0]]
    genes_filt = [g for g, k in zip(gene_names, keep_mask) if k]

    bin_idx = bin_cells_by_score(score, n_bins=n_bins, strategy="equal_count")
    pb, bin_score = pseudobulk_by_bin(X_filt, bin_idx, score, n_bins=n_bins)
    print(f"Pseudobulked into {pb.shape[0]} bins, {pb.shape[1]} genes.")

    deswan_df = deswan_scan(pb, bin_score, genes_filt, alpha=alpha)
    n_total_sig = int((deswan_df["n_significant"] > 0).sum())
    print(f"Windows with ≥1 significant gene: {n_total_sig} / {len(deswan_df)}")

    fig = crest_plot(
        deswan_df,
        title=f"DE-SWAN crests on senescence score · {cell_type_label}",
        output_path=f"{output_dir}/crest_{cell_type_label}.png" if output_dir else None,
    )
    pg_table = per_gene_peak_table(deswan_df, genes_filt, pb, bin_score)
    if output_dir:
        deswan_df.reset_index().to_csv(f"{output_dir}/deswan_{cell_type_label}.csv", index=False)
        pg_table.to_csv(f"{output_dir}/per_gene_peaks_{cell_type_label}.csv", index=False)
    return {
        "deswan": deswan_df,
        "per_gene": pg_table,
        "pseudobulk": pb,
        "bin_score": bin_score,
        "kept_genes": genes_filt,
        "figure": fig,
    }
