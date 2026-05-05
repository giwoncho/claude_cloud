# Giwon Cho — Research Context for Daily Paper Selection

> Use this to choose ONE paper per day that is most relevant to the user's
> active research. Updated 2026-05-05.

## The user (recipient)
- **Giwon Cho**, PhD candidate, Varghese Lab, Duke University BME.
- Email: giwon.cho@duke.edu (primary), giwoncho1206@gmail.com (personal).
- Korean speaker, fluent in scientific English.
- Active manuscript in revision (v11) — bone marrow senolytic mechanism.

## Active research themes (PRIORITY for paper selection)

Rank order — pick papers that score high on the top themes.

1. **Bone marrow (BM) senolytic mechanism** — Dasatinib + Quercetin (D+Q) in
   aged BM. How D+Q reshapes the HSC niche, which cells clear, which cells
   reprogram instead of dying, downstream chromatin changes.

2. **Hematopoietic stem and progenitor cell (HSPC) aging & rejuvenation** —
   intrinsic HSC aging (epigenetic drift, polarity loss, lineage bias)
   AND niche-driven aging (extrinsic). Aging reversal interventions.

3. **Mesenchymal stromal cell (MSC) / CAR-cell biology in BM niche** —
   MSC sub-states (CAR / Adipo / Osteo / Perivascular), Bmp2 / Cxcl12 / Kitl
   / Angpt1 secretion, MSC-as-niche regulator. Sorting-bias artifacts in
   MSC literature.

4. **Cell–cell communication in BM (CellChat, NicheNet, LIANA)** —
   ligand–receptor inference, niche topology under perturbation,
   per-cell-type source attribution of cytokines (especially Lgals9, Cxcl12,
   Tgfb1, Il6, Tnf, Mmp8, Igfbp4, Bmp2).

5. **Single-cell multi-omics (scRNA + scATAC, WNN, ArchR, Scanpy, Seurat,
   muon)** — methods for integrating modalities especially across cohorts
   ("different mice" problem), label transfer, peak-to-gene linkage.

6. **Bivalent chromatin & HSC priming** — H3K4me3 + H3K27me3 dual marks at
   stem-cell gene loci, CUT&Tag, chromatin-led aging signatures, the
   2025 Cell paper on bivalency in HSC (already-known reference).

7. **Cellular senescence biology** — SASP composition, p16/p21 markers,
   SenMayo signature, sorting-gate artifacts in senescence flow,
   senolytic specificity, secondary senescence.

8. **Bone marrow transplantation (BMT) — competitive & non-competitive** —
   chimerism kinetics, myeloid bias of aged HSCs, niche-versus-cell-intrinsic
   contribution to engraftment.

## Secondary themes (still good)

- Inflammaging / NLRP3 / IL-1β / TNF in marrow
- Megakaryocyte–HSC niche cross-talk
- Endothelial niche (sinusoidal / arteriolar) role in HSC quiescence
- Adipocyte expansion in aged marrow, Bmp2 sources
- Trained immunity in aged hematopoiesis
- Clonal hematopoiesis of indeterminate potential (CHIP)
- Senolytics (D+Q, fisetin, navitoclax) clinical trials in aging
- ML / deep-learning methods for cell-type annotation, trajectory inference
- First-responder / cascade / temporal-ordering models in scRNA time series

## DEPRIORITIZE (not central; only pick if exceptionally important)

- Cancer-only papers (acute leukemia mechanism without aging/niche angle)
- Pure cardiovascular / metabolic / neuro senolytic papers (other tissues)
- Computational benchmarks of generic algorithms with no biology hook

## EXCLUDE
- Preprints already withdrawn or with major-revision flags on bioRxiv
- Predatory journals
- Non-English papers
- Anything not publicly available (no PubMed/PMC/bioRxiv/OA full-text)

## Selection rubric (when shortlisting)

For each candidate, score 1–5 on each:
1. **Relevance to top-3 themes** (weight 3×)
2. **Novelty / surprise** (does it shift a known model? challenge a
   standard claim? introduce a method the user hasn't seen?)
3. **Methodological transferability** (can the user adopt the technique
   for their own work?)
4. **Recency** (last 12 months > 12-24 months > older landmark only if
   exceptionally relevant)
5. **Open access verified** — must have a public full-text URL.

Pick the single highest-scoring paper. Tie-break by recency.

## Avoid repeats

Before finalizing, check `~/work/claude_cloud/daily_paper/sent_log.csv`
for previously-sent papers (DOI column). Skip if already sent in last
60 days.

## Already known landmark refs (the user has read these — DO NOT pick)

- Itokawa 2022 — aged HSC scATAC GSE190424 (anchor for Stage 33)
- Mansell 2024 — Cell 2024 senolytic BM single-cell
- The user's own work in review (Cho 2026 BM senolytic v11)
- 2025 Cell paper on bivalent chromatin in HSC (already cited)
- Mitchell 2024 (CellChat methods)

(Update this list manually when papers get covered.)
