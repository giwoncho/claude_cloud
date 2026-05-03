# Senescence-axis DE-SWAN — Shen 2024 idea adapted for G11BM

**TL;DR.** Shen et al. (Nature Aging 2024) found that human aging molecules
change **non-linearly** — they tip at specific ages. This adaptation
substitutes the *SenePy senescence score per cell* for chronological age,
and applies the same DE-SWAN sliding-window analysis to identify
**senescence thresholds** in your G11BM scRNA-seq data.

## What you get

A **crest plot** of "# of genes with q < 0.05" vs senescence score.
Peaks (crests) mark score values where many genes simultaneously transition.
These are candidate **biological tipping points** for senescence in
each cell type.

For DQ vs Veh: compare crest *location* and *sharpness* between conditions.
DQ might shift the threshold rightward (cells must reach a higher score
to "tip") or flatten it (no tipping at all).

## Files

- `senescence_deswan.py` — the module. Pure Python (numpy + scipy + matplotlib).
  Implements: equal-count binning, bin-pseudobulking, sliding-window
  Welch t-test with BH FDR, anti-circularity gene filtering (drops
  SenMayo + score-correlated genes), and the crest plot.
- `run_demo.py` — wraps the module to read your existing
  `adata_all_drm_anno_fullannot.h5ad` + `percell_senescence_scores.csv`,
  filters to one cell type and condition, and writes outputs.

## Quick start

```bash
cd /hpc/home/gc237/work/claude_cloud/shen_adaptation
# activate the same conda env you use for bm_final_analysis.py
python run_demo.py --celltype Monocytes --condition Veh
python run_demo.py --celltype Monocytes --condition DQ
python run_demo.py --celltype HSPC      --condition both
```

Outputs land in `./output/<celltype>_<condition>/`:
- `crest_<celltype>.png` — the headline plot (crests = senescence thresholds)
- `deswan_<celltype>.csv` — per-window tables (n_significant, top genes)
- `per_gene_peaks_<celltype>.csv` — every gene's "peak" score (rank by `peak_qvalue`)

## Recommended cell types to start with

Based on cell counts in your G11BM data:
1. **Monocytes** (~30k cells) — best statistical power, established senescence biology
2. **Neutrophil / Erythroid** — large populations, useful negative-control comparisons
3. **HSPC** (~5k) — small but biologically interesting; expect noisier crests
4. **MSC** (~few hundred) — likely too few for clean crests; combine V+D and try

## Anti-circularity safeguard (important)

Because the senescence score is itself derived from gene expression,
asking "which genes change with score" is circular for the score-defining
genes. The module drops:
- The canonical **SenMayo** gene set (Saul 2022) — embedded in the module
- Any user-supplied `extra_genes_to_drop` (give it your SenePy hub genes
  for the focal cell type if you want extra protection)
- Genes with `|Spearman(expr, score)| > 0.7` — data-driven leakage check

If you find that the most prominent crests are still being driven by
known senescence markers (look at the `top_genes` column), tighten the
correlation threshold or expand `extra_genes_to_drop`.

## Interpreting a crest

A crest at score = X means "many genes transition between the cells just
below X and the cells just above X." Practical reads:

1. **One sharp crest, late on the score axis** → there's a real "senescent
   commitment point." Look at `top_genes` at that crest — what pathways?
   GSEA them with your existing gseapy pipeline.
2. **Multiple smaller crests** → senescence is staged. Compare gene programs
   per crest.
3. **No crests, just a flat line** → genes change linearly with score
   (unlike Shen's age data, which had two real crests). This itself
   is informative — it would mean SenePy score is a continuous gradient
   without internal thresholds in this cell type.
4. **Veh has a sharp crest, DQ flattens it** → DQ disrupts the senescence
   commitment, candidate mechanism for senolytic effect. (This is the
   biggest "win" scenario for the G11BM paper.)

## Caveats

- DE-SWAN was designed for between-individual variation. Substituting
  per-cell senescence score introduces between-cell variation, which
  conflates senescence with cell-state heterogeneity. The bin-pseudobulk
  step partially mitigates this by treating each bin as a "pseudo-individual."
- Welch's t-test assumes the per-bin pseudobulks are roughly i.i.d.
  within window. If your bins are very unequal in size or your data
  has strong donor effects, consider a permutation null instead.
- Bucket size and bin count are hyperparameters — sweep them and check
  crest robustness.

## Next steps if results look promising

1. Pathway-enrich the genes at each crest using your existing
   `gsea_percelltype_aging.py` — feed the `peak_score` column as the
   ranking metric.
2. Compare crest location across cell types: are there shared thresholds
   (single body-wide commitment) or cell-type-specific thresholds?
3. Compare Veh vs DQ crest locations per cell type — that's the
   senolytic-axis question.
4. (Stretch) Apply the same logic to **maturation pseudotime** in HSPCs
   instead of senescence score — that probes whether myelopoiesis
   itself has tipping points.

## Method credit

- DE-SWAN originally from Lehallier et al. 2019, *Nat Med* (the
  `lehallib/DEswan` R package). We re-implement the core in Python here
  to integrate with your scanpy stack — equivalent results.
- Senescence-axis adaptation: my idea, inspired by Shen 2024.

## Status

Untested on real data — please run on Monocytes first as a sanity check.
Reach out if any of the column-name assumptions in `run_demo.py` don't
match your adata.
