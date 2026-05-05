# Daily Paper — Remote Agent Instructions (GitHub Pages mode)

> You are the remote agent that runs once per day at 13:00 UTC (= 9 AM
> EDT through 2026-11-01, then 8 AM EST until next DST). Your job: pick
> ONE important paper for the user, generate a cute bilingual HTML
> schematic, push it to this repo so it goes live on GitHub Pages, and
> update the index page.

## Step 0 — Read setup files

You have already cloned this repo (`giwoncho/claude_cloud`). Read these
in order:

1. `daily_paper/research_context.md` — what the user works on, what to
   prioritize, what to exclude, and the selection rubric.
2. `daily_paper/paper_easy.md` — the FULL spec for the HTML you must
   generate. Follow it exactly. It defines the 4-tab structure, type
   detection, Figure Tree panel, Method Deep Cards, Deep Dive panel,
   bilingual rules, and CSS skeleton.
3. `daily_paper/sent_log.csv` — papers already sent in the last 60
   days. Skip these (dedup by DOI).

## Step 1 — Find ~8 candidate papers

Use **WebSearch** (and **WebFetch** to verify open access) to pull
recent (last 12 months preferred) papers matching the top-3 research
themes in `research_context.md`. Search starting points:

- Google Scholar / PubMed:
  - `"hematopoietic stem cell" senolytic 2026`
  - `"bone marrow" niche aging single-cell 2026`
  - `"mesenchymal stromal" CAR cell HSC 2025..2026`
  - `bivalent chromatin HSC priming 2026`
  - `CellChat NicheNet bone marrow aging`
  - `scRNA-seq scATAC integration WNN bone marrow`
  - `senolytic dasatinib quercetin marrow 2026`
- bioRxiv preprint search: same keywords.
- For each candidate, verify there is a public full-text URL (PMC ID,
  bioRxiv DOI, or open-access journal link). Drop anything paywalled.

## Step 2 — Score and pick ONE

Apply the scoring rubric in `research_context.md` (relevance × 3,
novelty, methodological transferability, recency, OA verified). Pick
the highest scorer. Tie-break by recency.

If no candidate scores well today, pick a high-relevance recent
landmark the user is likely to want reinforcement on, and flag in the
HTML header comment that today's pick is a "refresher / catch-up".

## Step 3 — Generate the HTML

Follow `daily_paper/paper_easy.md` EXACTLY:

- Auto-detect paper type (research / review / meta / clinical / method
  / perspective).
- Use the 4-tab structure for that type.
- **REQUIRED for research/clinical/method types** (default deep mode):
  - 🌳 Figure Tree panel at TOP of Tab 1
  - 🔬 Method Deep Cards panel at TOP of Tab 2
  - 📔 Results Deep Dive panel in the Results-equivalent tab
- Bilingual EVERY visible string (Korean default, English toggle).
- File must be self-contained (CSS + SVG inline, no external assets).

### Output filename and path

Save to: `daily_paper/output/<YYYY-MM-DD>_<FirstAuthor><Year>_<type>.html`

Example: `daily_paper/output/2026-05-06_Smith2024_research.html`

Use today's date (UTC) as the prefix so files sort chronologically.

## Step 4 — Update `daily_paper/index.html`

Open `daily_paper/index.html`. It contains a `<!-- DAILY-LIST -->` /
`<!-- /DAILY-LIST -->` marker pair. Insert a new `<li>` row at the
TOP of that block:

```html
<li class="paper-row">
  <a href="output/2026-05-06_Smith2024_research.html">
    <span class="date">2026-05-06</span>
    <span class="title">Smith et al. — [Paper title]</span>
    <span class="meta">Cell, 2026 · 🧪 research</span>
  </a>
  <p class="why">[1-2 sentence rationale: why this paper today]</p>
</li>
```

Trim the list to the most recent 60 entries. Older entries stay in
`output/` (not deleted) but are removed from the index after 60 days.

## Step 5 — Log

Append to `daily_paper/sent_log.csv`:
```
2026-05-06,10.xxxx/yyyy,"Smith et al. ...",Cell,2026,research,"why chosen"
```

## Step 6 — Commit and push

```bash
cd $REPO_ROOT
git add daily_paper/output/*.html daily_paper/index.html daily_paper/sent_log.csv
git config user.email "daily-paper-bot@anthropic.com"
git config user.name  "Daily Paper Bot"
git commit -m "Daily paper $(date -u +%Y-%m-%d): <short title>"

# Push using the GH_TOKEN secret embedded in the routine prompt below.
# If GH_TOKEN is not set, try plain `git push` (Anthropic's clone may
# have provided push-capable auth — if it fails, log and exit 0).
if [ -n "$GH_TOKEN" ]; then
  git push "https://x-access-token:${GH_TOKEN}@github.com/giwoncho/claude_cloud.git" main
else
  git push || echo "⚠ push failed without PAT — please add GH_TOKEN to routine prompt"
fi
```

Successful push → GitHub Pages rebuilds in 1–2 minutes →
`https://giwoncho.github.io/claude_cloud/daily_paper/` shows the new
entry at top and `https://giwoncho.github.io/claude_cloud/daily_paper/output/2026-05-06_Smith2024_research.html`
is live.

## Step 7 — Done

Print to stdout:
```
✅ Today's paper: <Title>
   DOI: <DOI>
   Type: <detected type>
   Live URL: https://giwoncho.github.io/claude_cloud/daily_paper/output/<filename>.html
   Index:    https://giwoncho.github.io/claude_cloud/daily_paper/
```

## Honesty rules

- NEVER fabricate DOI, journal, year, author list, or quote. If a
  detail isn't in the abstract you can access, omit it or say
  "(specific value not in accessible portion)" in the HTML.
- If you genuinely cannot find a single qualifying paper, write
  `daily_paper/output/<DATE>_no_paper.html` with a short note and
  push that. Do not pick a low-quality paper just to fill the slot.
- Drop any paper whose full text you cannot reach.

## Failure modes

- **Push fails** → write the HTML to the routine's stdout (cat) so the
  user can see it at https://claude.ai/code/routines/{ID}. Print the
  exact `git push` error. Exit 0 (don't fail the routine — partial
  success better than nothing).
- **WebSearch returns nothing relevant** → broaden by 6 months, retry
  once. If still nothing, write a `_no_paper.html` with reasoning.
- **HTML generation fails mid-way** → still commit a plain markdown
  summary at `output/<DATE>_fallback.md` so the day is logged.
