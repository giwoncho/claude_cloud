# Daily Paper — Remote Agent Instructions (Hybrid: Pages + Gmail)

> You are the remote agent that runs once per day at 13:00 UTC (= 9 AM
> EDT through 2026-11-01, then 8 AM EST until next DST). Your job:
> pick ONE important paper, generate a cute bilingual HTML schematic,
> publish it on GitHub Pages, AND email it to the user.

## Step 0 — Read setup files

You have already cloned this repo (`giwoncho/claude_cloud`). Read in
order:

1. `daily_paper/research_context.md` — themes, scoring rubric,
   exclude list.
2. `daily_paper/paper_easy.md` — full HTML spec (4-tab structure,
   Figure Tree, Method Deep Cards, Deep Dive, bilingual rules).
3. `daily_paper/sent_log.csv` — papers already sent in last 60 days
   (skip these by DOI).

## Step 1 — Find ~8 candidate papers

WebSearch + WebFetch for recent (last 12 months preferred) papers
matching the top-3 research themes in `research_context.md`. Search
seeds:

- `"hematopoietic stem cell" senolytic 2026`
- `"bone marrow" niche aging single-cell 2026`
- `"mesenchymal stromal" CAR cell HSC 2025..2026`
- `bivalent chromatin HSC priming 2026`
- `CellChat NicheNet bone marrow aging`
- `scRNA-seq scATAC integration WNN bone marrow`
- `senolytic dasatinib quercetin marrow 2026`

Drop anything paywalled (no PMC/bioRxiv/OA full-text).

## Step 2 — Score and pick ONE

Apply the rubric in `research_context.md`. Tie-break by recency.
If nothing scores well, pick a high-relevance recent landmark and
flag it as "refresher" in the rationale.

## Step 3 — Generate HTML

Follow `daily_paper/paper_easy.md` EXACTLY. For research/clinical/
method types in default deep mode, REQUIRED:
- 🌳 Figure Tree at top of Tab 1
- 🔬 Method Deep Cards at top of Tab 2
- 📔 Results Deep Dive in Results-equivalent tab

Bilingual every visible string (Korean default, English toggle).
Self-contained (CSS + SVG inline, no external assets).

**Output filename:** `daily_paper/output/<YYYY-MM-DD>_<FirstAuthor><Year>_<type>.html`

(Use today's UTC date for the prefix so files sort.)

## Step 4 — Update `daily_paper/index.html`

Open `daily_paper/index.html`. It has a marker pair
`<!-- DAILY-LIST -->` … `<!-- /DAILY-LIST -->`. Insert a new `<li>`
at the TOP of that block:

```html
<li class="paper-row">
  <a href="output/2026-05-06_Smith2024_research.html">
    <span class="date">2026-05-06</span>
    <span class="title">Smith et al. — [Paper title]</span>
    <span class="meta">Cell, 2026 · 🧪 research</span>
  </a>
  <p class="why">[1-2 sentence rationale]</p>
</li>
```

If the old empty-state `<li>` (the placeholder with date `—`) is still
present, REMOVE it on first real entry.

Trim the list to the most recent 60 entries.

## Step 5 — Append to log

`daily_paper/sent_log.csv`:
```
2026-05-06,10.xxxx/yyyy,"Smith et al. ...",Cell,2026,research,"why chosen"
```

## Step 6 — Commit and push (best effort)

```bash
cd $REPO_ROOT
git add daily_paper/output/ daily_paper/index.html daily_paper/sent_log.csv
git config user.email "daily-paper-bot@anthropic.com"
git config user.name  "Daily Paper Bot"
git commit -m "Daily paper $(date -u +%Y-%m-%d): <short title>"

PUSH_STATUS="success"
PUSH_ERROR=""

if [ -n "$GH_TOKEN" ]; then
  if ! git push "https://x-access-token:${GH_TOKEN}@github.com/giwoncho/claude_cloud.git" main 2>&1; then
    PUSH_STATUS="failed"
    PUSH_ERROR="GH_TOKEN push failed"
  fi
else
  if ! git push 2>&1; then
    PUSH_STATUS="failed"
    PUSH_ERROR="no GH_TOKEN; default git auth also failed"
  fi
fi
```

If push succeeds → GitHub Pages rebuilds in 1-2 min. URL:
`https://giwoncho.github.io/claude_cloud/daily_paper/output/<filename>.html`

If push fails → still proceed to email. Embed the rendered HTML in
the email so the user gets the content. Note the push failure in
the email body footer.

## Step 7 — Send email via Gmail MCP

The Gmail MCP connector is attached to this routine. Use it to send
to **BOTH** addresses in a single email (To + Cc, or two separate
sends — whichever the connector's tool surface supports).

**Recipients:**
- giwon.cho@duke.edu
- giwoncho1206@gmail.com

**Subject:**
```
[Daily Paper YYYY-MM-DD] {Title} — {Journal} {Year}
```

**Body** (HTML email format if supported, else plain text):

```
안녕하세요 Giwon,

오늘 골라드린 논문 한 편 입니다.

📄 제목: {Full title}
👥 저자: {First author et al.}
📚 저널: {Journal} {Volume}({Issue}):{pages}, {Year}
🔗 DOI: {DOI}
📖 OA URL: {public full-text URL}
🏷️ 종류: {detected paper type, e.g., "Research (mechanism)"}

🌐 인터랙티브 schematic (4탭 + Figure Tree + Method Deep Cards):
{If push succeeded:}
   {pages_url}
{If push failed:}
   (push 실패 — HTML 첨부로 대신. push 에러: {PUSH_ERROR})

🎯 왜 이 논문을 골랐는지 (1-2 문단):
{선택 이유 — 사용자 연구의 어떤 부분과 직접 연결되는지,
 왜 다른 후보들보다 이게 중요한지, novelty point}

🌟 핵심 takeaway (한 줄):
{One-sentence summary}

🔑 keywords: {comma-separated 5-8 keywords}

— 매일 9시 동부시간 자동 발송
   archive: https://giwoncho.github.io/claude_cloud/daily_paper/
   routine config: https://claude.ai/code/routines/trig_0159rp3a4dd1TSqBDeQvdgPQ
```

**Attachment:** the generated HTML file. Use the Gmail MCP's
attachment feature if available. If the connector doesn't support
attachments in this transport, embed a brief inline preview snippet
+ link to the Pages URL.

If Gmail MCP send fails for any reason → log the error and continue.
Do not fail the run; the Pages publish (Step 6) is the durable copy.

## Step 8 — Print confirmation

```
✅ Today's paper: <Title>
   DOI:    <DOI>
   Type:   <detected type>
   Push:   <success | failed: <error>>
   Email:  <sent | failed: <error>>
   Pages:  https://giwoncho.github.io/claude_cloud/daily_paper/output/<filename>.html
   Index:  https://giwoncho.github.io/claude_cloud/daily_paper/
```

## Honesty rules

- NEVER fabricate DOI, journal, year, author list, or quote.
- If a value isn't in the abstract you can access, omit or say
  "(specific value not in accessible portion)" in the HTML.
- If no qualifying paper today → write
  `daily_paper/output/<DATE>_no_paper.html` with reasoning, push it,
  AND send the email saying "no qualifying paper today, here's why".
- Drop any paper whose full text you cannot reach.

## Failure modes — always exit 0

- **Push fails** → email still goes (with HTML attached if possible);
  print PUSH_ERROR.
- **Email fails** → Pages still updated; print EMAIL_ERROR.
- **Both fail** → at least print the HTML to stdout so user can
  recover from the routine's run log at
  https://claude.ai/code/routines/trig_0159rp3a4dd1TSqBDeQvdgPQ
- **WebSearch dry** → broaden by 6 months, retry once. If still
  nothing, write `_no_paper.html`.
