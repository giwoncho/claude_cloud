# Daily Paper — Remote Agent Instructions

> You are the remote agent that runs once per day at 9 AM Eastern.
> Your job: pick ONE important paper for the user, generate a cute
> bilingual HTML schematic, and email it to them.

## Step 0 — Setup

You have already cloned this repo (`giwoncho/claude_cloud`). Read these
three files first:

1. `daily_paper/research_context.md` — what the user works on, what to
   prioritize, what to exclude, and the selection rubric.
2. `daily_paper/paper_easy.md` — the FULL spec for the HTML you must
   generate. Follow it exactly. It defines the 4-tab structure, type
   detection, Figure Tree panel, Method Deep Cards, Deep Dive panel,
   bilingual rules, and CSS skeleton.
3. `daily_paper/sent_log.csv` (if it exists) — papers already sent in
   the last 60 days. Skip these.

## Step 1 — Find ~8 candidate papers

Use **WebSearch** (and **WebFetch** to verify open access) to pull
recent (last 12 months preferred) papers matching the top-3 research
themes in `research_context.md`. Good search starting points:

- Google Scholar / PubMed search queries:
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

If no candidate scores well today (e.g., a slow news day), pick a
**high-relevance recent landmark** the user is likely to want
reinforcement on, but flag in the email body that today's pick is a
"refresher / catch-up" choice.

## Step 3 — Generate the HTML

Follow `daily_paper/paper_easy.md` EXACTLY:

- Auto-detect paper type (research / review / meta / clinical / method
  / perspective).
- Use the 4-tab structure for that type.
- **REQUIRED for research/clinical/method types** (deep mode):
  - 🌳 Figure Tree panel at TOP of Tab 1
  - 🔬 Method Deep Cards panel at TOP of Tab 2
  - 📔 Results Deep Dive panel in the Results-equivalent tab
- Bilingual EVERY visible string (Korean default, English toggle).
- Save to a temporary file: `daily_paper/output/<FirstAuthor><Year>_<type>_cute.html`
- File must be self-contained (CSS + SVG inline, no external assets).

## Step 4 — Email both addresses

Use the **Gmail MCP connector** (already attached to this routine) to
send to BOTH:
- giwon.cho@duke.edu
- giwoncho1206@gmail.com

**Subject line format:**
```
[Daily Paper] {Title} — {Journal} {Year}
```

**Email body (plain text or simple HTML):**
```
안녕하세요 Giwon,

오늘 골라드린 논문:

📄 제목: {Full title}
👥 저자: {First author et al.}
📚 저널: {Journal}, Volume(Issue):pages, {Year}
🔗 DOI: {DOI}
📖 OA URL: {public full-text URL}
🏷️ 종류: {detected paper type, e.g., "Research (mechanism)"}

🎯 왜 이 논문을 골랐는지 (1-2 문단):
{선택 이유 — 사용자 연구의 어떤 부분과 직접 연결되는지,
 왜 다른 후보들보다 이게 중요한지, novelty point는 무엇인지}

🌟 핵심 takeaway (한 줄):
{One-sentence summary}

첨부된 HTML 파일에서 자세한 schematic 보세요. Figure Tree로
paper map 펼치고, Method Deep Cards로 각 기법 비유 확인하시면 됩니다.

— 매일 9시 동부시간 자동 발송
```

**Attachment:** the HTML file generated in Step 3.

If the Gmail connector cannot attach files, fall back to:
1. Push the HTML to `~/work/claude_cloud/daily_paper/output/` and commit
   to the repo so the GitHub Pages URL becomes live:
   `https://giwoncho.github.io/claude_cloud/daily_paper/output/<filename>.html`
2. Include the Pages URL in the email body instead.

## Step 5 — Log

Append a row to `daily_paper/sent_log.csv` so future runs don't repeat:
```
date,doi,title,journal,year,paper_type,why_chosen
2026-05-05,10.xxxx/yyyy,"...",Cell,2026,research,"..."
```

Commit the log update + (if attaching via Pages fallback) the new HTML
to the repo:
```
git add daily_paper/sent_log.csv daily_paper/output/*.html
git commit -m "Daily paper YYYY-MM-DD: <short title>"
git push
```

(Repo remote is already `git@github-giwoncho:giwoncho/claude_cloud.git`
with the right SSH alias. If push fails, the routine still succeeded
provided the email was sent.)

## Step 6 — Done

Print a one-line confirmation: `✅ Sent <title> ({DOI}) to both addresses.`

## Honesty rules

- **NEVER fabricate** a DOI, journal, year, author list, or quote. If a
  detail isn't in the abstract you can access, omit it or say
  "(specific value not in accessible portion)" in the HTML.
- If you genuinely cannot find a single qualifying paper, send a short
  email saying "오늘은 적절한 후보를 못 찾았어요. 검색 쿼리를
  알려주시면 다음에 더 잘 찾겠습니다." Do not pick a low-quality
  paper just to fill the slot.
- Drop any paper whose full text you cannot reach — the user wants
  publicly available papers only.

## Failure modes — what to do

- **No Gmail connector available** → push HTML to repo + email cannot
  be sent. Print error in agent log.
- **WebSearch returns nothing relevant** → broaden by 6 months, retry.
  If still nothing, send "no qualifying paper today" email.
- **HTML generation fails** → email a plain-text summary (no
  attachment) so the user still gets something.
- **Push to GitHub fails** → still send the email; log the error.
