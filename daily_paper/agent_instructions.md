# Daily Paper — Remote Agent Instructions (Hybrid: Pages + Gmail)

> You are the remote agent that runs once per day at 13:00 UTC (= 9 AM
> EDT through 2026-11-01, then 8 AM EST until next DST). Your job:
> pick ONE important paper, generate a cute bilingual HTML schematic,
> publish it on GitHub Pages, AND email it to the user.

## ⏱️ Time budget — *없음*

**시간 제한 두지 말 것.** 정확하고 잘 만든 결과물이 우선. silent fail 이
가장 큰 문제였음. 천천히, 모든 step 의 결과 (성공/실패) 를 명확히 echo.

소프트 가이드 (자원 낭비 방지용, hard cap 아님):
- WebSearch ~5번
- WebFetch ~4번
- HTML write 한 번에 단일 Write (분할 X, 길어도 OK)

검색이 느려도, HTML 이 길어도, 모든 step 끝까지 완수.

## Step 0 — Read setup files (LEAN)

You have already cloned this repo (`giwoncho/claude_cloud`). Read:

1. `daily_paper/research_context.md` — themes, scoring rubric, exclude list. **Full file.**
2. `daily_paper/sent_log.csv` — papers already sent (skip these by DOI). **Full file.**
3. `daily_paper/paper_easy.md` — HTML spec. **DO NOT read in full (1430 lines).** Read only:
   - Lines 1–200 (input handling, supported types, workflow overview)
   - Lines 204–632 (HTML skeleton — this is the boilerplate you must use verbatim)
   - Lines 640–663 (RESEARCH type schema — most papers are this type)
   - Lines 786–890 (Deep Dive panel spec)
   - Lines 891–1027 (Figure Tree panel spec)
   - Lines 1029–1170 (Method Deep Cards spec)
   - Lines 1383–1430 (color palette + checklist + verification)

   **Skip the SVG illustration library (1172–1382) and other type schemas (665–784) unless your paper is review/meta/clinical/method/perspective.**

   You can use `Read` with `offset` and `limit` parameters to grab just these ranges in 4–5 calls.

For reference, `daily_paper/output/2026-05-05_Doolittle2026_research.html` (the 2026-05-05 example) is a fully-conforming research-type output — if you get stuck on structure, peek at it to copy patterns rather than re-reading the spec.

## Step 1 — Find candidates (HARD CAPS: 3 WebSearch, 2 WebFetch)

Run **3 WebSearch calls maximum**, picked from the top-3 themes in
`research_context.md`. Examples (rotate to avoid repeats with
`sent_log.csv`):

- `"bone marrow" senolytic single-cell 2026`
- `"hematopoietic stem cell" niche aging 2026`
- `"mesenchymal stromal" bone marrow rejuvenation 2026`
- `bivalent chromatin HSC 2026`
- `CellChat NicheNet bone marrow aging 2026`

From the search results pick **3–4 promising candidates**. Run **at
most 2 WebFetch calls** to read the abstracts of the top 1–2.

Drop anything paywalled (no PMC / bioRxiv / OA full-text).

## Step 2 — Score and pick ONE

Apply the rubric in `research_context.md`. Tie-break by recency. Pick
ONE within 2 minutes of finishing fetches. Don't dither — the time
budget is tight.

## Step 3 — Generate HTML (lean target)

Follow `daily_paper/paper_easy.md`. For research/clinical/method types,
REQUIRED:
- 🌳 Figure Tree at top of Tab 1
- 🔬 Method Deep Cards at top of Tab 2
- 📔 Results Deep Dive in Results-equivalent tab

**Lean targets to fit budget:**
- Figure Tree: **3–4 figures** (not all 5–7), each with 2–3 panels
  (not 4–6). Pick the most informative ones.
- Method Deep Cards: **3–4 cards** (not 5–6). Cover the central
  techniques only.
- Deep Dive: **3 findings** (matches summary cards).

Bilingual every visible string (Korean default, English toggle).
Self-contained (CSS + SVG inline, no external assets). One single
`Write` call for the full HTML — don't fragment.

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

## Step 7 — Send email via Resend HTTP API

We use **Resend** (https://resend.com) for delivery. The API key is
provided to you in the prompt as `$RESEND_API_KEY`. Do NOT commit the
key to any file in the repo. Use it only from the env at runtime.

**Recipients:** for now, ONLY `giwoncho1206@gmail.com`. The Resend free
tier blocks non-registered addresses until a domain is verified.
Eventually `giwon.cho@duke.edu` will also be added (after domain
verification or a fallback Gmail-App-Password path).

**From:** `onboarding@resend.dev` (Resend's default until user verifies
their own domain).

**Subject:**
```
[Daily Paper YYYY-MM-DD] {FirstAuthor et al.} — {short-title} — {Journal} {Year}
```

**Body:** HTML — pretty card layout, schematic link prominent, 1-2 paragraph
"why chosen", one-line takeaway, keywords, footer.

**Attachment:** the generated HTML file (base64-encoded in the JSON).

**Critical Cloudflare workaround:** Resend sits behind Cloudflare and
will return HTTP 403 (error code 1010) without a User-Agent header.
ALWAYS send a `User-Agent: Mozilla/5.0 (Linux x86_64) Resend-Client/1.0`
header.

**Implementation (use this Python via Bash heredoc):**

```bash
EMAIL_STATUS="sent"
EMAIL_ERROR=""

if [ -z "$RESEND_API_KEY" ]; then
  EMAIL_STATUS="failed"
  EMAIL_ERROR="RESEND_API_KEY not set in routine env"
else
  python3 <<'PYEOF' || { EMAIL_STATUS="failed"; EMAIL_ERROR="resend send raised"; }
import os, json, base64, urllib.request, urllib.error

HTML_FILE = "daily_paper/output/<TODAY-FILENAME>.html"  # set this
SUBJECT   = "[Daily Paper YYYY-MM-DD] {Author} et al. — {short-title} — {Journal} {Year}"

# Compose body — fill all bracketed slots from the paper you selected
body_html = """<div style="font-family:Helvetica,Arial,sans-serif;max-width:640px;margin:0 auto;line-height:1.6;color:#3a4252;">
<p>안녕하세요 Giwon,</p>
<p>오늘 골라드린 논문 한 편입니다.</p>
<table style="width:100%;background:#fafbff;border-radius:12px;margin:16px 0;border-collapse:collapse;">
  <tr><td style="padding:14px 18px;border-left:4px solid #d63384;">
    <p><strong>📄 제목:</strong> {Full title}</p>
    <p><strong>👥 저자:</strong> {First author et al.} ({Lab}, {Institution})</p>
    <p><strong>📚 저널:</strong> {Journal} {Volume}({Issue}):{pages}, {Year}</p>
    <p><strong>🔗 DOI:</strong> <a href="https://doi.org/{DOI}">{DOI}</a></p>
    <p><strong>📖 OA:</strong> <a href="{OA_URL}">{OA_URL}</a></p>
    <p><strong>🏷️ 종류:</strong> {detected type}</p>
  </td></tr>
</table>
<p style="background:linear-gradient(135deg,#ffd6e7,#fff5e6);padding:14px 18px;border-radius:12px;border:2px dashed #ffb3d4;">
  <strong>🌐 인터랙티브 schematic:</strong><br>
  <a href="{pages_url}" style="color:#d63384;font-weight:bold;">{pages_url}</a><br>
  <span style="color:#888;font-size:12px;">push 2분 후부터 활성. 첨부 HTML 파일도 단독으로 열림.</span>
</p>
<p><strong>🎯 왜 이 논문을 골랐는지</strong></p>
<p>{1-2 specific paragraphs — which top-3 theme it hits, why this beat the other candidates, novelty axis. Avoid generic phrases.}</p>
<p><strong>🌟 핵심 takeaway</strong> (한 줄): {one sentence}</p>
<p><strong>🔑 keywords:</strong> {5-8 comma-separated keywords}</p>
<hr style="margin-top:24px;border:none;border-top:1px solid #eee;">
<p style="color:#888;font-size:12px;line-height:1.5;">
— 매일 아침 9시 (Eastern) 자동 발송<br>
&nbsp;&nbsp;&nbsp;archive: <a href="https://giwoncho.github.io/claude_cloud/daily_paper/" style="color:#888;">https://giwoncho.github.io/claude_cloud/daily_paper/</a><br>
&nbsp;&nbsp;&nbsp;routine: <a href="https://claude.ai/code/routines/trig_0159rp3a4dd1TSqBDeQvdgPQ" style="color:#888;">claude.ai/code/routines/trig_0159rp3a4dd1TSqBDeQvdgPQ</a>
</p>
</div>"""

with open(HTML_FILE, "rb") as f:
    attachment_b64 = base64.b64encode(f.read()).decode("ascii")

payload = {
    "from": "onboarding@resend.dev",
    "to":   ["giwoncho1206@gmail.com"],
    "subject": SUBJECT,
    "html": body_html,
    "attachments": [{
        "filename": HTML_FILE.split("/")[-1],
        "content":  attachment_b64,
    }],
}

req = urllib.request.Request(
    "https://api.resend.com/emails",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {os.environ['RESEND_API_KEY']}",
        "Content-Type":  "application/json",
        "User-Agent":    "Mozilla/5.0 (Linux x86_64) Resend-Client/1.0",
        "Accept":        "application/json",
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as resp:
    print("RESEND HTTP", resp.status, resp.read().decode())
PYEOF
fi
```

**Failure handling:** if Resend send fails → log `EMAIL_ERROR` and
continue. Do not fail the run; the Pages publish (Step 6) remains the
durable copy.

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
