---
description: 논문 종류(연구/리뷰/메타/임상/방법/관점)를 자동판별해서 4탭 귀여운 SVG schematic HTML (KR + EN 토글)로 변환. **Figure Tree (수형도)** 로 피규어→패널→실험 비유 드릴다운 + **Method Deep Cards** (초딩 비유 포함) + 결과 Deep Dive 펼침 섹션
argument-hint: <DOI | PMID | URL | "paper title"> [output filename] [--type=research|review|meta|clinical|method|perspective] [--detail=deep|brief]
---

# /paper_easy — Paper to Cute Schematic Webpage (Bilingual, Type-Aware)

You are an interactive paper-to-schematic generator. Take a scientific paper, **automatically detect its type**, and produce a single self-contained HTML file with **4 tabs** tailored to that type, each filled with **cute SVG illustrations** that communicate the paper's core ideas **at a glance**, in **BOTH Korean and English** simultaneously, switchable via a language toggle.

## Input
Paper identifier: **$ARGUMENTS**

This can be a DOI, PMID, paper URL, or a title to search for. Optional flags:
- Second positional arg = output filename
- `--type=<research|review|meta|clinical|method|perspective>` = force paper type, skipping auto-detection
- `--detail=<deep|brief>` = controls how much detail goes into the Results-equivalent tab. **`deep` is the default** — adds an expandable "📔 결과 자세히 / Results in Depth" panel beneath the summary cards, with real numbers, direct paper quotes, and plain-language interpretation per finding. Use `brief` to revert to the old summary-cards-only behavior.

---

## Supported Paper Types & Their Tab Structure

| Type | Tab1 | Tab2 | Tab3 | Tab4 |
|---|---|---|---|---|
| **research** 🧪 | 📖 Intro | 🔬 Methods | 💡 Results | 💭 Discussion |
| **review** 📚 | 📖 Background | 🗂️ Key Themes | 🔀 Synthesis | 🤔 Open Questions |
| **meta** 🌲 | ❓ Question (PICO) | 🔍 Search & Selection | 📊 Pooled Findings | 🏥 Implications |
| **clinical** 🏥 | ❓ Question | 🧪 Trial Design | 📊 Outcomes | 🩺 Clinical Implications |
| **method** ⚙️ | 🚧 Problem | ⚙️ The Method | ✅ Validation | 🌐 Applications |
| **perspective** 📣 | 🎯 Thesis | 📚 Evidence | ⚖️ Counterarguments | 📣 Call to Action |

**Each type has its own signature SVG vocabulary** — the visual style at a glance tells you what kind of paper it is. See "Type-specific schemas" and "SVG illustration library" below.

---

## Workflow

### Step 0 — Handle `--help` / empty args

**Before doing anything else**, check `$ARGUMENTS`. If it is empty, `--help`, `-h`, `help`, or `?`, **do NOT fetch any paper**. Instead, print the help block below verbatim (bilingual, both languages shown together — since this is plain chat output, not the generated HTML, do not use `<span class="lang-...">` wrappers) and stop:

```
📄 /paper_easy — 논문을 귀여운 SVG schematic HTML로 변환 (KR/EN 토글)
📄 /paper_easy — Convert papers into cute SVG schematic HTML (KR/EN toggle)

Usage:
  /paper_easy <DOI | PMID | URL | "title">                       # auto-detect type, deep results
  /paper_easy <id> <output.html>                                  # custom filename
  /paper_easy <id> --type=<research|review|meta|clinical|method|perspective>
  /paper_easy <id> --detail=<deep|brief>                          # default deep

Examples:
  /paper_easy 10.1038/s41586-024-12345-6
  /paper_easy 38712345
  /paper_easy "Niche regulation of HSC quiescence"
  /paper_easy 10.1016/j.cell.2024.01.001 my_review.html --type=review
  /paper_easy 38712345 --detail=brief                             # summary cards only

📔 Detail mode (default = deep) / 자세히 모드:
  --detail=deep   기본값. 다음 세 가지 deep 컴포넌트가 모두 켜집니다:

                  🌳 Figure Tree (Intro 탭 맨 위)
                     ├─ 각 Figure가 무엇을 주장하는지 한 줄
                     ├─ 클릭 펼침 → 패널 a/b/c... 리스트
                     └─ 패널 다시 클릭 → [실험 종류 + 🧒 초딩 비유 +
                                          📊 간단한 결과 + 💡 스토리상 의미]
                     "섹션별 디테일 들어가기 전에 전체 paper map 한 번에"

                  🔬 Method Deep Cards (Methods 탭)
                     각 기법마다 펼침 카드:
                     [📊 무엇인가 + 🧒 초딩 비유 + 🎯 왜 이 방법
                      + 👁️ 무엇을 볼 수 있나 + ⚠️ 한계]

                  📔 Results Deep Dive (Results 탭)
                     각 finding마다 [실제 수치 + 무엇을 측정했나 +
                                     논문 직접 인용 + 일반인 언어 해설]

  --detail=brief  세 가지 deep 컴포넌트 모두 끔. 요약 카드만.

📚 지원하는 논문 종류 / Supported paper types:

  🧪 research     원저 연구 / Original research (mechanism, discovery)
                  → 📖 Intro · 🔬 Methods · 💡 Results · 💭 Discussion
                  signature: cell + mechanism arrow chain

  📚 review       리뷰 / Literature review
                  → 📖 Background · 🗂️ Themes · 🔀 Synthesis · 🤔 Open Questions
                  signature: 분야 진화 timeline + 합의/논쟁 매트릭스

  🌲 meta         메타분석 / Systematic review · meta-analysis
                  → ❓ PICO · 🔍 PRISMA · 📊 Pooled Findings · 🏥 Implications
                  signature: PRISMA flow + forest plot (diamond pooled estimate)

  🏥 clinical     임상시험 / Clinical trial · RCT · cohort
                  → ❓ Question · 🧪 Design · 📊 Outcomes · 🩺 Implications
                  signature: 환자 stick-figure grid + treatment vs control bar

  ⚙️ method       방법 논문 / New tool · protocol · algorithm
                  → 🚧 Problem · ⚙️ Method · ✅ Validation · 🌐 Applications
                  signature: 번호 매긴 protocol-step 파이프라인 + before/after

  📣 perspective  관점 / Opinion · commentary · call-to-action
                  → 🎯 Thesis · 📚 Evidence · ⚖️ Counterarguments · 📣 Call to Action
                  signature: 양팔 저울 (for vs against)

🔍 자동판별 / Auto-detection:
  논문 fetch 후 abstract + section heading으로 type을 자동 추론합니다.
  After fetch, type is inferred from abstract + section headings.
  override 하려면 --type=... 플래그 사용 / use --type=... to force a specific type.

출력 / Output:
  ~/work/papers/ 폴더에 <FirstAuthor><Year>_<type>_cute.html 로 저장 (없으면 자동 생성).
  두 번째 인자로 경로/파일명을 직접 지정할 수도 있음.
  Saves to ~/work/papers/<FirstAuthor><Year>_<type>_cute.html (auto-creates the folder).
  Pass a second positional argument to override the path/filename.
  Single self-contained HTML — embedded CSS + SVG, no external assets,
  language toggle button (top-right) switches between KR and EN.
```

After printing this block, stop and wait for the user to re-run with a real paper identifier. Do not proceed to Step 1.

### Step 1 — Fetch the paper
Use **WebFetch** and/or **WebSearch** to retrieve:
- Title, authors, affiliations, journal, year, DOI
- Full abstract
- Section headings (this is the strongest signal for type detection)
- The body content relevant to the detected type (see Step 2)
- **For deep-detail mode (default):** for each major finding, also pull
  - Specific numbers (n, %, p-values, fold-change, OR/HR, CI, effect size)
  - At least one **direct quote** (or honest paraphrase if full text isn't accessible — say so)
  - Enough context to write a 2-3 sentence plain-language interpretation
  - The figure/table number where the finding lives, for the quote-source tag

If the paper is paywalled, try PubMed Central, bioRxiv, the lab website, or summarize from the abstract + press releases. Always cite the original DOI/PubMed link in the footer. If specific numbers cannot be retrieved, **omit the number chip rather than fabricate** — note in the deep dive that the value wasn't accessible.

### Step 2 — Auto-detect the paper type

Apply this decision tree using **section headings + abstract keywords + structural cues**:

```
1. Has explicit "Methods" + "Results" sections + original data + n / p-values?
   ├── Yes → it's a primary study. Sub-classify:
   │     ├── "ClinicalTrials.gov", "randomized", "primary endpoint",
   │     │    enrolled patients, intention-to-treat   → CLINICAL
   │     ├── "We describe/present a [protocol|tool|algorithm|pipeline]",
   │     │    benchmarking, validation on test datasets, no biological discovery
   │     │    as the main claim                        → METHOD
   │     └── Otherwise (mechanism / discovery study)    → RESEARCH
   │
   └── No / minimal original wet-lab data → it's a synthesis / opinion piece:
         ├── "Systematic review", "PRISMA", search strategy disclosed,
         │    forest plot, inclusion/exclusion criteria   → META
         ├── Comprehensive multi-section literature synthesis,
         │    "we review", "here we discuss", high citation density,
         │    typically >50 refs                          → REVIEW
         └── Short (<5 pages), single argument, opinion-driven,
              "we argue / propose / call for"              → PERSPECTIVE
```

**Tell the user the detected type in one line before generating** (do not stop and ask):

> 🔍 **감지됨:** 이 논문은 **Review**로 보입니다 (synthesis, no original methods). 진행합니다. (다른 type을 강제하려면 `--type=research` 식으로 다시 실행하세요.)
>
> 🔍 **Detected:** This paper appears to be a **Review** (synthesis, no original methods). Proceeding. (To force a different type, re-run with `--type=research` etc.)

If `--type=...` flag is supplied, skip detection and use that type. If detection is borderline (e.g., review-with-some-data), pick the type that matches the paper's **dominant claim style** and note it.

### Step 3 — Pick the filename
Default: `~/work/papers/<FirstAuthor><Year>_<type>_cute.html` (i.e. `/hpc/home/gc237/work/papers/...` on this machine — expand `~` to the user's HOME).
Examples: `~/work/papers/Smith2024_review_cute.html`, `~/work/papers/Jung2023_research_cute.html`.

Before writing, ensure the directory exists (`mkdir -p ~/work/papers`). If the user supplied a second positional argument, use that as the full path/filename instead — it overrides the default location entirely (do **not** prepend `~/work/papers/` if the user gave their own path). Confirm before overwriting an existing file.

### Step 4 — Generate the HTML
Use the **common skeleton** (CSS, header, tab scaffold, language toggle, JS) and the **type-specific tab content schema** for the detected type. **Strictly preserve** across all types:

- 4-tab navigation (the labels/emojis change per type, but the structure does not)
- The 🌐 language toggle button (top-right, fixed)
- The pastel pink/blue/cream gradient background and panel/card aesthetic
- The bubble/banner/card components
- The cute SVG aesthetic: rounded shapes, simple faces, soft colors, emoji accents

**Bilingual content rules — ABSOLUTELY MANDATORY:**
- Every visible text element (heading, paragraph, bullet, label, button text, SVG text, table cell, footer) must exist in **both** Korean and English
- Wrap each language version in `<span class="lang-kr">한국어</span><span class="lang-en">English</span>`
- For SVG `<text>` elements, emit two `<text>` elements at the same coords: one with `class="lang-kr"`, the other `class="lang-en"`
- CSS hides one language at a time based on `body.lang-kr` / `body.lang-en` — defined in the skeleton
- Default state: `<body class="lang-kr">` (Korean visible)
- English translations should be **idiomatic scientific English**, not literal Korean→English. Read like a native English textbook.

**Visual-first principle (가장 중요):**
> 글이 아니라 **그림**이 먼저 말하게 하라. 누가 페이지를 처음 봤을 때 — 글을 읽기 전에 — type별 시그니처 SVG (forest plot? 환자 아이콘? 분야 진화 타임라인?)만 보고도 "아, 이거 메타분석이구나 / 임상시험이구나 / 리뷰구나"를 알 수 있어야 한다.
>
> Each paper type has signature SVG patterns listed below. **Use them.** A reader scrolling through with the language toggle off should still be able to recognize the paper's genre and core findings purely from the visuals.

### Step 5 — Save and confirm
After Write, tell the user:
- Detected paper type + 1-line justification
- File path
- A 2–3 sentence summary of the paper
- A brief note on which schematic got the biggest visual treatment

---

## Common HTML skeleton

The skeleton below is **type-agnostic**: header, tab scaffold, CSS, language toggle, JS. Plug in type-specific tab labels (Step A) and tab content (Step B, see "Type-specific schemas" further down).

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[[FirstAuthor Year]] — [[Short Title]] (cute · [[type]])</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Quicksand', 'Comic Sans MS', system-ui, sans-serif;
    background: linear-gradient(135deg, #ffeef5 0%, #e8f4ff 50%, #fff5e6 100%);
    color: #3a4252; min-height: 100vh; padding: 30px 20px;
  }
  .container { max-width: 1100px; margin: 0 auto; }
  header { background: white; padding: 28px; border-radius: 24px; text-align: center;
    margin-bottom: 20px; box-shadow: 0 8px 24px rgba(255,150,200,0.15);
    border: 3px dashed #ffb3d4; position: relative; }
  header h1 { font-size: 22px; color: #d63384; margin-bottom: 10px; }
  header .subtitle { color: #6c757d; font-size: 14px; }
  header .citation { color: #999; font-size: 12px; margin-top: 4px; font-style: italic; }
  header .emoji { font-size: 32px; margin-bottom: 8px; }
  header .type-badge { display: inline-block; margin-top: 10px; padding: 4px 14px;
    background: linear-gradient(135deg,#ffd6e7,#fff5e6); border: 2px solid #ffb3d4;
    border-radius: 14px; font-size: 12px; font-weight: bold; color: #d63384; }

  .tabs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;
    margin-bottom: 24px; background: white; padding: 10px; border-radius: 18px;
    box-shadow: 0 4px 14px rgba(100,130,200,0.1); }
  .tab-btn { border: 2px solid transparent; background: #fef6f9; padding: 14px 16px;
    border-radius: 12px; cursor: pointer; font-family: inherit; font-size: 14px;
    font-weight: 600; color: #888; transition: all 0.25s; display: flex;
    flex-direction: column; align-items: center; gap: 4px; }
  .tab-btn .tab-emoji { font-size: 22px; }
  .tab-btn:hover { background: #fff0f5; color: #5a4fcf; transform: translateY(-2px); }
  .tab-btn.active { background: linear-gradient(135deg,#ffd6e7 0%,#fff5e6 100%);
    color: #d63384; border-color: #ffb3d4;
    box-shadow: 0 4px 12px rgba(255,150,200,0.3); }

  .tab-content { display: none; animation: fadeIn 0.4s ease-out; }
  .tab-content.active { display: block; }
  @keyframes fadeIn { from{opacity:0;transform:translateY(8px);} to{opacity:1;transform:translateY(0);} }

  .panel { background: white; border-radius: 20px; padding: 28px; margin-bottom: 24px;
    box-shadow: 0 6px 18px rgba(100,130,200,0.1); border: 2px solid #fff; }
  .panel h2 { font-size: 19px; color: #5a4fcf; margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px; }
  .panel h3 { font-size: 15px; color: #5a4fcf; margin: 16px 0 8px; }

  .scene { display: block; margin: 12px auto; max-width: 100%; }
  .bubble { background: #fff5e6; padding: 14px 18px; border-radius: 16px;
    border: 2px solid #ffd591; font-size: 14px; margin: 12px 0; }
  .bubble.pink { background: #ffe6f0; border-color: #ffb3d4; }
  .bubble.blue { background: #e6f0ff; border-color: #91b8e0; }
  .bubble.green { background: #e8f5e9; border-color: #a5d6a7; }
  .bubble.purple { background: #f0e6ff; border-color: #b89ce0; }
  .bubble.orange { background: #fff0e0; border-color: #ffb380; }

  /* Outcome / finding cards */
  .outcomes { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; margin-top: 20px; }
  .outcome-card { border-radius: 18px; padding: 20px; text-align: center;
    border: 3px solid; background: white; transition: transform 0.2s; }
  .outcome-card:hover { transform: translateY(-4px); }
  .outcome-card.pink { border-color: #d63384; background: linear-gradient(180deg,#fff,#ffe6f0); }
  .outcome-card.blue { border-color: #5b9bd5; background: linear-gradient(180deg,#fff,#e9f1fa); }
  .outcome-card.orange { border-color: #ed7d31; background: linear-gradient(180deg,#fff,#fdf0e6); }
  .outcome-card.green { border-color: #2e8b57; background: linear-gradient(180deg,#fff,#e7f3e4); }
  .outcome-card.purple { border-color: #5a4fcf; background: linear-gradient(180deg,#fff,#f0e6ff); }
  .outcome-card.gray { border-color: #888; background: linear-gradient(180deg,#fff,#f5f5f5); }
  .outcome-card .icon { font-size: 42px; margin-bottom: 8px; }
  .outcome-card h3 { font-size: 15px; margin-bottom: 6px; color: #3a4252; }
  .outcome-card .source-tag { display: inline-block; font-size: 11px; padding: 3px 10px;
    border-radius: 10px; margin-bottom: 10px; font-weight: bold; color: white; }
  .outcome-card.pink .source-tag { background: #d63384; }
  .outcome-card.blue .source-tag { background: #5b9bd5; }
  .outcome-card.orange .source-tag { background: #ed7d31; }
  .outcome-card.green .source-tag { background: #2e8b57; }
  .outcome-card.purple .source-tag { background: #5a4fcf; }
  .outcome-card ul { list-style: none; text-align: left; font-size: 13px; }
  .outcome-card li { padding: 3px 0; }

  .summary-banner { background: linear-gradient(135deg,#ffd591 0%,#ffb3d4 50%,#91b8e0 100%);
    padding: 24px; border-radius: 20px; text-align: center; color: white;
    font-size: 16px; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.15); margin-top: 20px; }

  .method-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px; }
  .method-card { border-radius: 16px; padding: 18px; background: #fafbff; border: 2px solid #e0e6f5; }
  .method-card h4 { color: #5a4fcf; font-size: 14px; margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px; }
  .method-card p, .method-card ul { font-size: 13px; color: #555; }
  .method-card ul { padding-left: 18px; margin-top: 6px; }

  .hierarchy { background: linear-gradient(180deg,#fff 0%,#f0f7ff 100%);
    padding: 20px; border-radius: 16px; border: 2px dashed #91b8e0; margin-top: 12px; }

  .discussion-list { list-style: none; padding: 0; }
  .discussion-item { background: #fafbff; border-left: 5px solid #5a4fcf;
    padding: 16px 20px; border-radius: 8px; margin-bottom: 12px; }
  .discussion-item.limitation { border-left-color: #ed7d31; background: #fdf0e6; }
  .discussion-item.future { border-left-color: #6aaa64; background: #e7f3e4; }
  .discussion-item.controversy { border-left-color: #d63384; background: #ffe6f0; }
  .discussion-item h4 { font-size: 14px; margin-bottom: 6px; color: #5a4fcf; }
  .discussion-item.limitation h4 { color: #b85f25; }
  .discussion-item.future h4 { color: #4a7c47; }
  .discussion-item.controversy h4 { color: #a3296c; }
  .discussion-item p { font-size: 13px; color: #555; line-height: 1.6; }

  .qa-flow { background: linear-gradient(135deg,#fff5e6 0%,#ffe6f0 100%);
    padding: 20px; border-radius: 16px; margin-top: 12px; }
  .qa-row { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 14px; }
  .qa-q, .qa-a { padding: 12px 16px; border-radius: 14px; font-size: 13px; flex: 1; }
  .qa-q { background: #ffe6f0; border: 2px solid #ffb3d4; }
  .qa-a { background: #e6f0ff; border: 2px solid #91b8e0; }

  /* === Type-specific component CSS === */
  /* Review: timeline */
  .timeline { position: relative; padding: 30px 0; margin: 20px 0; }
  .timeline::before { content:''; position: absolute; left: 0; right: 0; top: 50%;
    height: 4px; background: linear-gradient(90deg,#ffb3d4,#91b8e0,#a5d6a7); border-radius: 2px; }
  .timeline-row { display: flex; justify-content: space-between; gap: 12px; }
  .timeline-node { flex: 1; text-align: center; background: white;
    border: 2px solid #b89ce0; border-radius: 14px; padding: 10px; font-size: 12px;
    position: relative; z-index: 1; }
  .timeline-node .year { font-weight: bold; color: #5a4fcf; font-size: 13px; }

  /* Meta: forest plot row + PRISMA */
  .forest-row { display: grid; grid-template-columns: 2fr 3fr 1fr; gap: 12px;
    align-items: center; padding: 8px 0; border-bottom: 1px dashed #eee; font-size: 13px; }
  .forest-row .study-name { font-weight: 600; color: #333; }
  .forest-row .estimate { font-family: monospace; text-align: right; color: #555; }
  .prisma-step { background: linear-gradient(135deg,#e6f0ff,#fff); border: 2px solid #91b8e0;
    padding: 12px 16px; border-radius: 12px; text-align: center; font-size: 13px;
    margin: 8px 0; position: relative; }
  .prisma-step .count { font-weight: bold; color: #5b9bd5; font-size: 16px; }
  .prisma-arrow { text-align: center; font-size: 22px; color: #91b8e0; margin: -2px 0; }

  /* Clinical: patient grid */
  .patient-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 14px; }
  .arm { border-radius: 16px; padding: 18px; text-align: center; }
  .arm.treatment { background: linear-gradient(180deg,#ffe6f0,#fff); border: 3px solid #d63384; }
  .arm.control { background: linear-gradient(180deg,#e9f1fa,#fff); border: 3px solid #5b9bd5; }
  .arm h4 { margin-bottom: 10px; font-size: 15px; }
  .stat-badge { display: inline-block; padding: 6px 14px; border-radius: 12px;
    background: #5a4fcf; color: white; font-weight: bold; font-size: 13px; margin: 4px; }
  .stat-badge.warn { background: #ed7d31; }
  .stat-badge.good { background: #2e8b57; }

  /* Method: protocol step */
  .protocol-step { background: white; border: 2px solid #b89ce0; border-radius: 14px;
    padding: 14px 18px; margin: 8px 0; display: flex; gap: 14px; align-items: center; font-size: 13px; }
  .protocol-step .num { background: #5a4fcf; color: white; width: 32px; height: 32px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: bold; flex-shrink: 0; }

  /* Perspective: argument scale */
  .scale { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 14px 0; }
  .scale-pan { padding: 16px; border-radius: 14px; }
  .scale-pan.for { background: #e7f3e4; border: 2px solid #6aaa64; }
  .scale-pan.against { background: #fdf0e6; border: 2px solid #ed7d31; }

  /* === Deep Dive (--detail=deep) === */
  details.deep-dive { margin: 14px 0; background: #fafbff; border: 2px solid #e0e6f5;
    border-radius: 14px; padding: 14px 18px; transition: background 0.2s; }
  details.deep-dive[open] { background: linear-gradient(180deg,#fff,#fafbff);
    border-color: #b89ce0; box-shadow: 0 4px 12px rgba(100,130,200,0.08); }
  details.deep-dive summary { cursor: pointer; font-size: 14px; font-weight: 600;
    color: #5a4fcf; padding: 4px 0; user-select: none; list-style: none;
    display: flex; align-items: center; gap: 8px; }
  details.deep-dive summary::-webkit-details-marker { display: none; }
  details.deep-dive summary::before { content: '▶'; display: inline-block;
    transition: transform 0.2s; color: #d63384; font-size: 11px; }
  details.deep-dive[open] summary::before { transform: rotate(90deg); }
  details.deep-dive .body { margin-top: 14px; padding-top: 12px;
    border-top: 1px dashed #e0e6f5; }
  details.deep-dive .body h4 { color: #5a4fcf; font-size: 13px; margin: 14px 0 8px;
    display: flex; align-items: center; gap: 6px; font-weight: 700; }
  details.deep-dive .body h4:first-child { margin-top: 0; }

  .narrative { font-size: 13.5px; line-height: 1.75; color: #444; margin: 6px 0 12px; }
  .narrative strong { color: #5a4fcf; }

  .numbers-strip { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0 14px; }
  .number-chip { background: linear-gradient(135deg,#ffe6f0,#fff5e6);
    border: 2px solid #ffb3d4; border-radius: 12px; padding: 8px 14px;
    font-size: 12px; min-width: 80px; text-align: center; }
  .number-chip strong { display: block; color: #d63384; font-size: 17px;
    font-weight: bold; line-height: 1.2; }
  .number-chip .unit { color: #888; font-size: 11px; display: block; margin-top: 2px; }
  .number-chip.blue { background: linear-gradient(135deg,#e6f0ff,#fff);
    border-color: #91b8e0; }
  .number-chip.blue strong { color: #5b9bd5; }
  .number-chip.green { background: linear-gradient(135deg,#e8f5e9,#fff);
    border-color: #a5d6a7; }
  .number-chip.green strong { color: #2e8b57; }
  .number-chip.purple { background: linear-gradient(135deg,#f0e6ff,#fff);
    border-color: #b89ce0; }
  .number-chip.purple strong { color: #5a4fcf; }

  .paper-quote { background: #fff5e6; border-left: 4px solid #d63384;
    padding: 12px 16px 12px 20px; margin: 10px 0 14px; font-style: italic;
    font-size: 13px; color: #6c3a52; border-radius: 0 12px 12px 0; line-height: 1.65; }
  .paper-quote .src { display: block; margin-top: 8px; font-size: 11px;
    font-style: normal; color: #999; text-align: right; }

  /* === Figure Tree (paper structure overview, top of Intro tab) === */
  .figure-tree { margin: 16px 0; display: flex; flex-direction: column; gap: 14px; }
  details.fig-node { background: linear-gradient(135deg,#fff,#fff5e6);
    border: 3px solid #ffb3d4; border-radius: 18px; padding: 14px 18px;
    box-shadow: 0 4px 14px rgba(255,150,200,0.14); transition: background 0.2s; }
  details.fig-node[open] { background: linear-gradient(135deg,#fff,#ffeef5);
    box-shadow: 0 6px 18px rgba(255,150,200,0.20); }
  details.fig-node > summary { cursor: pointer; list-style: none;
    display: flex; align-items: center; gap: 12px; padding: 4px 0;
    font-weight: 700; user-select: none; }
  details.fig-node > summary::-webkit-details-marker { display: none; }
  details.fig-node > summary::before { content: '▶'; font-size: 12px; color: #d63384;
    transition: transform 0.2s; flex-shrink: 0; }
  details.fig-node[open] > summary::before { transform: rotate(90deg); }
  details.fig-node .fig-num { background: #d63384; color: white;
    padding: 5px 14px; border-radius: 12px; font-size: 13px;
    font-weight: bold; flex-shrink: 0; letter-spacing: 0.5px; }
  details.fig-node .fig-claim { font-size: 14.5px; flex: 1; color: #5a4fcf;
    line-height: 1.5; }
  details.fig-node .fig-body { margin-top: 14px; padding: 4px 0 4px 18px;
    border-left: 3px dashed #ffb3d4; display: flex; flex-direction: column; gap: 8px; }
  details.fig-node .fig-overview { font-size: 13px; color: #555;
    background: #fff5e6; padding: 10px 14px; border-radius: 12px;
    line-height: 1.65; border: 1px solid #ffd591; margin-bottom: 4px; }

  details.panel-node { background: white; border: 2px solid #91b8e0;
    border-radius: 12px; padding: 10px 14px; transition: background 0.2s; }
  details.panel-node[open] { background: linear-gradient(135deg,#fff,#e6f0ff);
    box-shadow: 0 3px 8px rgba(91,155,213,0.15); }
  details.panel-node > summary { cursor: pointer; list-style: none;
    display: flex; align-items: center; gap: 10px; padding: 2px 0;
    font-size: 13px; user-select: none; flex-wrap: wrap; }
  details.panel-node > summary::-webkit-details-marker { display: none; }
  details.panel-node > summary::before { content: '▸'; font-size: 11px;
    color: #5b9bd5; transition: transform 0.2s; flex-shrink: 0; }
  details.panel-node[open] > summary::before { transform: rotate(90deg); }
  details.panel-node .panel-letter { background: #5b9bd5; color: white;
    width: 26px; height: 26px; border-radius: 7px; display: inline-flex;
    align-items: center; justify-content: center; font-weight: bold;
    font-size: 12px; flex-shrink: 0; }
  details.panel-node .panel-exp-type { color: #5a4fcf; font-weight: 600; }
  details.panel-node .panel-tldr { color: #666; font-size: 12px;
    margin-left: auto; font-style: italic; }
  details.panel-node .panel-body { margin-top: 12px; padding-top: 10px;
    border-top: 1px dashed #e0e6f5; display: flex; flex-direction: column; gap: 10px; }
  .panel-block { padding: 11px 14px; border-radius: 10px;
    font-size: 13px; line-height: 1.65; }
  .panel-block.exptype { background: #f0e6ff; border-left: 4px solid #5a4fcf; }
  .panel-block.analogy { background: #fff5e6; border-left: 4px solid #ffb380; }
  .panel-block.result  { background: #e6f0ff; border-left: 4px solid #5b9bd5; }
  .panel-block.meaning { background: #e8f5e9; border-left: 4px solid #6aaa64; }
  .panel-block strong { display: block; margin-bottom: 5px;
    font-size: 12px; letter-spacing: 0.3px; }
  .panel-block.exptype strong { color: #5a4fcf; }
  .panel-block.analogy strong { color: #b85f25; }
  .panel-block.result  strong { color: #2a6ea3; }
  .panel-block.meaning strong { color: #4a7c47; }

  /* === Method Deep Cards (Methods tab) === */
  details.method-deep { margin: 12px 0; background: white;
    border: 2px solid #b89ce0; border-radius: 16px; padding: 14px 18px;
    box-shadow: 0 4px 12px rgba(100,80,200,0.08); transition: background 0.2s; }
  details.method-deep[open] { background: linear-gradient(135deg,#fff,#f0e6ff);
    border-color: #5a4fcf; box-shadow: 0 6px 18px rgba(100,80,200,0.15); }
  details.method-deep > summary { cursor: pointer; list-style: none;
    display: flex; align-items: center; gap: 12px;
    font-weight: 700; color: #5a4fcf; font-size: 14.5px;
    padding: 4px 0; user-select: none; }
  details.method-deep > summary::-webkit-details-marker { display: none; }
  details.method-deep > summary::before { content: '▶'; font-size: 12px;
    color: #5a4fcf; transition: transform 0.2s; flex-shrink: 0; }
  details.method-deep[open] > summary::before { transform: rotate(90deg); }
  details.method-deep .method-icon { font-size: 22px; flex-shrink: 0; }
  details.method-deep .method-name { flex: 1; }
  details.method-deep .method-shorttag { font-size: 11px; color: #888;
    background: #f5f0ff; padding: 3px 9px; border-radius: 8px;
    font-weight: normal; flex-shrink: 0; }
  details.method-deep .method-body { margin-top: 14px; padding-top: 12px;
    border-top: 1px dashed #e0e6f5;
    display: flex; flex-direction: column; gap: 12px; }
  details.method-deep .method-body h4 { font-size: 13px; color: #5a4fcf;
    margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
    font-weight: 700; }
  details.method-deep .method-body p { font-size: 13px; color: #444;
    line-height: 1.7; }
  .analogy-box { background: linear-gradient(135deg,#fff5e6,#ffe6f0);
    border: 2px dashed #ffb380; border-radius: 12px; padding: 14px 18px; }
  .analogy-box h4 { color: #b85f25 !important; }
  .analogy-box p { color: #6c4a32 !important; font-style: italic;
    line-height: 1.75 !important; }
  .why-box { background: linear-gradient(135deg,#e6f0ff,#fff);
    border-left: 4px solid #5b9bd5; padding: 12px 16px; border-radius: 0 12px 12px 0; }
  .can-see-box { background: linear-gradient(135deg,#e8f5e9,#fff);
    border-left: 4px solid #6aaa64; padding: 12px 16px; border-radius: 0 12px 12px 0; }
  .limit-box { background: linear-gradient(135deg,#fdf0e6,#fff);
    border-left: 4px solid #ed7d31; padding: 12px 16px; border-radius: 0 12px 12px 0; }

  footer { text-align: center; padding: 20px; color: #888; font-size: 12px; }
  footer a { color: #d63384; text-decoration: none; }

  /* Language toggle */
  .lang-toggle {
    position: fixed; top: 20px; right: 20px; z-index: 100;
    background: white; border: 2px solid #ffb3d4; border-radius: 24px;
    padding: 8px 16px; cursor: pointer; font-family: inherit; font-size: 13px;
    font-weight: 600; color: #d63384; box-shadow: 0 4px 12px rgba(255,150,200,0.25);
    transition: all 0.2s; display: flex; align-items: center; gap: 6px;
  }
  .lang-toggle:hover { transform: scale(1.05); background: #fff0f5; }
  .lang-toggle .flag { font-size: 16px; }

  /* Language visibility */
  body.lang-kr .lang-en, body.lang-en .lang-kr { display: none !important; }
  body.lang-kr svg .lang-en, body.lang-en svg .lang-kr { display: none !important; }

  @media (max-width: 800px) {
    .outcomes, .method-grid, .patient-grid, .scale { grid-template-columns: 1fr; }
    .tabs { grid-template-columns: 1fr 1fr; }
    .lang-toggle { top: 10px; right: 10px; padding: 6px 12px; font-size: 12px; }
  }
</style>
</head>
<body class="lang-kr">

<button class="lang-toggle" onclick="toggleLang()">
  <span class="flag lang-kr">🇰🇷</span><span class="lang-kr">한국어</span>
  <span class="flag lang-en">🇺🇸</span><span class="lang-en">English</span>
  <span style="opacity:0.5;">⇄</span>
  <span class="flag lang-kr">🇺🇸</span><span class="lang-kr" style="opacity:0.5;">EN</span>
  <span class="flag lang-en">🇰🇷</span><span class="lang-en" style="opacity:0.5;">KR</span>
</button>

<div class="container">

<header>
  <div class="emoji">[[3-4 thematic emojis — pick from type signature, see below]]</div>
  <h1>
    <span class="lang-kr">[[Korean catchy title]]</span>
    <span class="lang-en">[[English catchy title]]</span>
  </h1>
  <div class="subtitle">
    <span class="lang-kr">[[Authors et al.]] — [[Lab]] ([[Institution]])</span>
    <span class="lang-en">[[Authors et al.]] — [[Lab]] ([[Institution]])</span>
  </div>
  <div class="citation">[[Journal Volume(Issue):pages]], [[Year]] · DOI: [[doi]]</div>
  <div class="type-badge">
    <span class="lang-kr">[[Type 한글, e.g., 📚 리뷰 논문]]</span>
    <span class="lang-en">[[Type EN, e.g., 📚 Review Article]]</span>
  </div>
</header>

<div class="tabs">
  <!-- Tab labels are TYPE-SPECIFIC. Use the table at the top of this command. -->
  <button class="tab-btn active" data-tab="t1">
    <span class="tab-emoji">[[Tab1 emoji]]</span>
    <span class="lang-kr">[[Tab1 KR]]</span><span class="lang-en">[[Tab1 EN]]</span>
  </button>
  <button class="tab-btn" data-tab="t2">
    <span class="tab-emoji">[[Tab2 emoji]]</span>
    <span class="lang-kr">[[Tab2 KR]]</span><span class="lang-en">[[Tab2 EN]]</span>
  </button>
  <button class="tab-btn" data-tab="t3">
    <span class="tab-emoji">[[Tab3 emoji]]</span>
    <span class="lang-kr">[[Tab3 KR]]</span><span class="lang-en">[[Tab3 EN]]</span>
  </button>
  <button class="tab-btn" data-tab="t4">
    <span class="tab-emoji">[[Tab4 emoji]]</span>
    <span class="lang-kr">[[Tab4 KR]]</span><span class="lang-en">[[Tab4 EN]]</span>
  </button>
</div>

<!-- Each <div class="tab-content" id="t1..t4">…</div> is filled per the type-specific schema below. -->
[[TAB 1 CONTENT]]
[[TAB 2 CONTENT]]
[[TAB 3 CONTENT]]
[[TAB 4 CONTENT]]

<footer>
  <span class="lang-kr">Cute schematic of <strong>[[FirstAuthor et al. Year, <em>Journal</em>]]</strong></span>
  <span class="lang-en">Cute schematic of <strong>[[FirstAuthor et al. Year, <em>Journal</em>]]</strong></span>
  <br>
  <a href="[[paper URL]]" target="_blank">📄 <span class="lang-kr">원 논문</span><span class="lang-en">Original article</span></a> ·
  <a href="[[PubMed URL]]" target="_blank">🔬 PubMed</a>
</footer>

</div>

<script>
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(target).classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
  function toggleLang() {
    const body = document.body;
    if (body.classList.contains('lang-kr')) {
      body.classList.remove('lang-kr'); body.classList.add('lang-en');
      localStorage.setItem('paper_easy_lang', 'en');
    } else {
      body.classList.remove('lang-en'); body.classList.add('lang-kr');
      localStorage.setItem('paper_easy_lang', 'kr');
    }
  }
  (function() {
    const saved = localStorage.getItem('paper_easy_lang');
    if (saved === 'en') {
      document.body.classList.remove('lang-kr');
      document.body.classList.add('lang-en');
    }
  })();
</script>

</body>
</html>
```

---

## Type-specific schemas

For each type below: tab labels, the panels each tab should contain, and the **signature SVG / component** that should dominate the visual. The signature is the "한 눈에 알아볼" element — make it prominent, ideally in tab 2 or 3.

---

### A. RESEARCH 🧪 (mechanism / discovery study)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | 📖 | 서론 | Introduction |
| t2 | 🔬 | 방법 | Methods |
| t3 | 💡 | 결과 | Results |
| t4 | 💭 | 고찰 | Discussion |

**Signature visuals:** cute cell with face (the protagonist cell type), mouse/model schematic, mechanism arrow chain (stimulus → cell → response → output).

**Tab 1 — Intro:**
  - **🌳 Figure Tree panel (FIRST, prominent — see "Figure Tree" section below)** — full paper map: Fig 1 → Fig 2 → … each expandable to panels a/b/c with experiment-type + 🧒 kid analogy + 📊 result + 💡 story role. This sets up the entire paper before the reader drills into Methods/Results detail.
  - Then 2–3 panels: background scene SVG + key concept (signaling pathway) + open questions Q&A bubbles.

**Tab 2 — Methods:**
  - **🔬 Method Deep Cards panel (FIRST, prominent — see "Method Deep Cards" section below)** — one expandable card per major technique used (e.g., scRNA-seq, CUT&Tag, BMT, flow cytometry). Each card: what it is + 🧒 kid analogy + why this method + what you can see + limitations.
  - Then standard 2–3 panels: mouse model schematic, experimental design timeline + crosses, hierarchy/gating tree of analyzed populations.

**Tab 3 — Results:** 2–3 panels. **outcomes-grid** (3 cards = 3 findings) + **mechanism schematic** (the signature of this type — large SVG with arrows down through cell drawings) + summary table. Then the Results Deep Dive panel (see "Deep Dive panel" section below).

**Tab 4 — Discussion:** 4 panels. Old vs new paradigm SVG, implications list, limitations list (orange), future directions list (green), take-home banner.

---

### B. REVIEW 📚 (literature synthesis)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | 📖 | 배경 | Background |
| t2 | 🗂️ | 핵심 주제 | Key Themes |
| t3 | 🔀 | 종합 (합의·논쟁) | Synthesis |
| t4 | 🤔 | 미해결 질문 | Open Questions |

**Signature visuals:** **field-evolution timeline** (year-by-year nodes showing landmark studies), **theme cards** (each major theme = a card with cute icon), **consensus vs controversy matrix** (✅ vs ⚡ vs ❓ grid).

**Tab 1 — Background:** Why does this field exist? 1 panel with intro SVG of the biological/clinical problem. 1 panel with **timeline** of how the field evolved (use `.timeline` component — at least 4–6 nodes).
**Tab 2 — Key Themes:** 2–3 panels, each themed around a major sub-topic the review covers. Each panel uses an **outcome-card grid (3 cards)** to summarize that sub-topic's central ideas. Each card needs a cute icon.
**Tab 3 — Synthesis:** This is the heart. Two sections:
  - **합의 (Consensus)** — what does the field agree on? Use `.discussion-list` with green `.future` styling.
  - **논쟁 (Controversies)** — where do experts disagree? Use `.discussion-list` with new `.controversy` styling. Optionally include a "side A vs side B" two-column SVG.
**Tab 4 — Open Questions:** Q&A flow (`.qa-flow`) with 4–5 unanswered questions. End with a take-home banner stating what the next decade of research should target.

**Optional adaptations for review type:**
- 🌳 Figure Tree → adapt to **"Theme Tree"** at top of Tab 2: each major theme = `.fig-node`, key sub-questions or landmark studies = `.panel-node`. Same kid-analogy structure inside each panel block.
- 🔬 Method Deep Cards → if the review covers a methodological landscape (e.g., "techniques for measuring X"), use Method Deep Cards in Tab 1. Otherwise skip.

---

### C. META 🌲 (systematic review / meta-analysis)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | ❓ | 질문 (PICO) | Question (PICO) |
| t2 | 🔍 | 검색 & 선정 | Search & Selection |
| t3 | 📊 | 통합 결과 | Pooled Findings |
| t4 | 🏥 | 시사점 | Implications |

**Signature visuals:** **PRISMA flow** (the giveaway), **forest plot** (each study = row, OR/HR with CI as horizontal bar, diamond at bottom for pooled estimate), tiny **paper icons** for individual studies.

**Tab 1 — Question:** PICO breakdown (Population / Intervention / Comparator / Outcome) as a 4-card grid using `.outcome-card`. 1 SVG showing the patient population cartoon.
**Tab 2 — Search & Selection:** **PRISMA flow** using stacked `.prisma-step` divs — Records identified (n=...) → Screened → Full-text assessed → Included (final n) — with `.prisma-arrow` between each. Then a `.method-grid` with: databases searched, inclusion/exclusion criteria, quality assessment tool.
**Tab 3 — Pooled Findings:** **THIS is the signature panel.** Forest plot using `.forest-row` divs — one per included study, plus a "Pooled" diamond row at the bottom in color. Render the CI as an inline SVG bar (see SVG library). Add a heterogeneity badge (`I²=...%`).
**Tab 4 — Implications:** 3 sections:
  - **임상적 시사점 (Clinical implications)** — `.discussion-list` with green styling.
  - **한계 (Limitations of the evidence)** — orange `.limitation`.
  - **추가 연구 필요 (Research gaps)** — green `.future`. Take-home banner at end.

**Optional adaptations for meta type:**
- 🌳 Figure Tree → typically skipped (PRISMA + forest plot already serve as the paper's structural tree). If the meta-analysis has notable subgroup analyses, add a small Figure Tree at the top of Tab 3 with each subgroup as a `.fig-node`.
- 🔬 Method Deep Cards → use in Tab 2 to explain *the meta-analysis methodology itself* (random vs fixed effects, heterogeneity measures, risk-of-bias tools) with kid analogies — most readers find these terms opaque.

---

### D. CLINICAL 🏥 (clinical trial / RCT / cohort)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | ❓ | 임상 질문 | Question |
| t2 | 🧪 | 시험 디자인 | Trial Design |
| t3 | 📊 | 결과 | Outcomes |
| t4 | 🩺 | 임상적 시사점 | Clinical Implications |

**Signature visuals:** **patient stick-figure grid** (filled = treated, empty = control), **arm-vs-arm comparison** (side-by-side cards using `.patient-grid` with `.arm.treatment` and `.arm.control`), **outcome bar chart** (KM curve simplified, or bar comparing primary endpoint), **stat badges** (HR=0.65, NNT=12, p<0.001).

**Tab 1 — Question:**
  - **🌳 Figure Tree panel (FIRST)** — Fig 1, Fig 2, ... drilldown with panels and experiment-type kid analogies. (Same component as research type.)
  - Then PICO + clinical motivation. 1 panel with patient population SVG. 1 panel with the clinical question framed as a Q&A bubble.

**Tab 2 — Trial Design:**
  - **🔬 Method Deep Cards panel (FIRST)** — randomization scheme, blinding, primary-outcome assay, etc. Each gets a kid analogy.
  - Then **Signature panel.** `.patient-grid` with two arms (Treatment vs Control). Below it: a horizontal SVG timeline of randomization → intervention → follow-up → analysis.

**Tab 3 — Outcomes:** Primary outcome as a giant comparison SVG. `.stat-badge`s for HR, RR, NNT, p-value. Secondary outcomes as `.outcome-card` grid. Adverse events table. Then the Results Deep Dive panel.

**Tab 4 — Clinical Implications:** **임상에 어떻게 적용?** (How does this change practice?) — `.discussion-list`. **한계점** — orange. **남은 질문 / 다음 trial** — green. Take-home banner.

---

### E. METHOD ⚙️ (new tool / protocol / algorithm)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | 🚧 | 문제 | The Problem |
| t2 | ⚙️ | 방법 | The Method |
| t3 | ✅ | 검증 | Validation |
| t4 | 🌐 | 응용 | Applications |

**Signature visuals:** **before/after panel** (😩 old way vs 😊 new way), **protocol step pipeline** (numbered `.protocol-step` divs cascading down), **benchmark comparison** (new method vs existing methods as a bar chart SVG), **input → black box → output** flow diagram.

**Tab 1 — Problem:**
  - **🌳 Figure Tree panel (FIRST)** — for method papers, the figures usually walk through (i) the problem, (ii) the algorithm/protocol diagram, (iii) benchmarks, (iv) applications. Tree those out with kid analogies per panel.
  - Then 1 panel: the old workflow as a sad SVG (cluttered, slow, error-prone). 1 panel: the unmet need stated clearly. Use a `.bubble.orange` highlighting "What was missing".

**Tab 2 — Method:**
  - **🔬 Method Deep Cards panel (FIRST)** — each algorithmic component / pipeline step / benchmark dataset gets a card with kid analogy. (For method papers this is the heart of the paper — give it real estate.)
  - Then **Signature panel.** Stacked `.protocol-step` divs numbered 1, 2, 3, ... Below: a large "input → method → output" SVG.

**Tab 3 — Validation:** Three `.outcome-card`s: (1) accuracy/sensitivity vs gold standard, (2) speed/cost vs existing tools, (3) generalizability across datasets. Each with a tiny bar-chart SVG. Then the Results Deep Dive panel.

**Tab 4 — Applications:** What can people do with this now? 3 use-case cards. Limitations (orange). Future directions (green). Code/data availability link.

---

### F. PERSPECTIVE 📣 (opinion / commentary / call-to-action)

| Tab | Emoji | KR | EN |
|---|---|---|---|
| t1 | 🎯 | 주장 | Thesis |
| t2 | 📚 | 근거 | Evidence |
| t3 | ⚖️ | 반론 | Counterarguments |
| t4 | 📣 | 행동 촉구 | Call to Action |

**Signature visuals:** **balance scale** SVG (`.scale` component — for vs against), **megaphone / spotlight** SVG for the main argument, **before/after the field** vision SVG.

**Tab 1 — Thesis:** A bold banner SVG stating the central claim (use the `.summary-banner` style but at the top). 1 panel explaining why this thesis matters now (timing / urgency).
**Tab 2 — Evidence:** 3–4 `.outcome-card`s, each summarizing an empirical or logical reason supporting the thesis. Cite supporting studies as small footnote text under each card.
**Tab 3 — Counterarguments:** **Signature panel.** Use the `.scale` component — left pan = "주장 (For)", right pan = "반론 (Against)". For each counterargument, show how the authors rebut it. End with a `.bubble.purple` summarizing why the authors' view wins.
**Tab 4 — Call to Action:** 4–5 `.discussion-item.future` (green) listing concrete actions the field/clinicians/funders should take. Take-home banner with the rallying cry.

**Optional adaptations for perspective type:**
- 🌳 Figure Tree → adapt to **"Argument Tree"** at top of Tab 1: thesis = root `.fig-node`; major sub-claims = `.panel-node`s, with the kid analogy explaining each claim concretely.
- 🔬 Method Deep Cards → typically N/A. Skip unless the perspective proposes a new analytical framework worth explaining.

---

## Deep Dive panel (cross-cutting — applies to all types)

**This is the "easy but detailed" companion to the at-a-glance summary cards.** When `--detail=deep` (the default), every Results-equivalent tab MUST include a **"📔 결과 자세히 / Results in Depth"** panel placed *after* the signature visual + summary cards but *before* the take-home banner.

| Type | Where the deep dive goes |
|---|---|
| **research** 🧪 | Tab 3 (Results) — after the outcome cards + mechanism schematic |
| **clinical** 🏥 | Tab 3 (Outcomes) — after primary outcome bar + secondary cards |
| **meta** 🌲 | Tab 3 (Pooled Findings) — after the forest plot |
| **method** ⚙️ | Tab 3 (Validation) — after the three validation cards |
| **review** 📚 | Tab 3 (Synthesis) — after the consensus/controversy lists |
| **perspective** 📣 | Tab 2 (Evidence) — after the evidence cards |

**Design philosophy:** the visual-first principle still rules — the page must be readable at a glance with everything collapsed. The deep dive is *opt-in* depth, not a wall of text. Use the native `<details>`/`<summary>` element so no JavaScript is needed and collapse state survives the language toggle.

### Structure

For each finding (typically 3 — matching the summary cards), emit one `<details class="deep-dive">` block. Set `open` on the **first one only** so the reader sees what's available; the rest start collapsed.

```html
<div class="panel">
  <h2>📔
    <span class="lang-kr">결과 자세히 — 펼쳐서 읽기</span>
    <span class="lang-en">Results in Depth — expand to read</span>
  </h2>

  <details class="deep-dive" open>
    <summary>
      <span class="lang-kr">[[Finding 1 이름]] — 자세히</span>
      <span class="lang-en">[[Finding 1 name]] — read in detail</span>
    </summary>
    <div class="body">

      <h4>📊 <span class="lang-kr">실제 수치</span><span class="lang-en">The numbers</span></h4>
      <div class="numbers-strip">
        <div class="number-chip">
          <strong>[[value]]</strong>
          <span class="unit"><span class="lang-kr">[[KR unit/label]]</span><span class="lang-en">[[EN unit/label]]</span></span>
        </div>
        <div class="number-chip blue">
          <strong>p&lt;0.001</strong>
          <span class="unit"><span class="lang-kr">통계적 유의</span><span class="lang-en">significance</span></span>
        </div>
        <!-- 2–5 chips total. Use color variants (default pink, .blue, .green, .purple) -->
      </div>

      <h4>🔬 <span class="lang-kr">무엇을 측정했고 어떻게 비교했나</span><span class="lang-en">What was measured and how it was compared</span></h4>
      <p class="narrative">
        <span class="lang-kr">[[저자가 한 일을 2-3문장으로. 어떤 샘플, 어떤 조건, 어떤 비교군. 너무 압축하지 말고 한 단계씩 풀어 쓸 것.]]</span>
        <span class="lang-en">[[2-3 sentence narrative: what samples, what conditions, what comparison. Walk one step at a time, don't over-compress.]]</span>
      </p>

      <div class="paper-quote">
        <span class="lang-kr">[[논문 직접 인용 — 한국어 번역]]</span>
        <span class="lang-en">[[Direct quote from the paper, in English]]</span>
        <span class="src">— <span class="lang-kr">[[논문 섹션 / Fig 번호 / 페이지]]</span><span class="lang-en">[[Section / Fig number / page]]</span></span>
      </div>

      <h4>💡 <span class="lang-kr">왜 중요한가 (쉽게)</span><span class="lang-en">Why it matters (in plain language)</span></h4>
      <p class="narrative">
        <span class="lang-kr">[[비전공자가 읽어도 이해할 수 있는 해설. 도메인 용어가 등장하면 한 마디로 풀어 설명. 2-3문장.]]</span>
        <span class="lang-en">[[Plain-language interpretation, accessible to a smart non-specialist. Define domain terms inline. 2-3 sentences.]]</span>
      </p>

    </div>
  </details>

  <details class="deep-dive">
    <summary>
      <span class="lang-kr">[[Finding 2 이름]] — 자세히</span>
      <span class="lang-en">[[Finding 2 name]] — read in detail</span>
    </summary>
    <div class="body">
      <!-- same 4-block structure: numbers, what was measured, paper quote, why it matters -->
    </div>
  </details>

  <!-- third (and optionally fourth) <details> block, same structure -->
</div>
```

### Required content per `<details>` block

Each deep-dive block MUST contain all four:

1. **📊 실제 수치 / The numbers** — a `.numbers-strip` with 2–5 `.number-chip`s. Pull real values from the paper: n, %, p-values, fold-change, OR/HR with CI, effect size, time-to-event. **If you couldn't access a specific number, omit the chip — never invent.**

2. **🔬 무엇을 측정했나 / What was measured** — a `.narrative` paragraph (2-3 sentences) describing the actual experimental comparison. Resist the urge to over-summarize; the point of the deep dive is to give one more level of granularity than the summary card.

3. **`.paper-quote`** — at least one direct quote (or honest paraphrase, marked as such in the `.src` line) from the paper, with the figure/section reference. This grounds the interpretation and gives the reader something to verify against.

4. **💡 왜 중요한가 / Why it matters** — a `.narrative` paragraph in plain language. Imagine explaining to a smart undergrad with no domain background. Define jargon inline.

### `--detail=brief` behavior

When the user passes `--detail=brief`, **omit the entire Deep Dive panel**. The Results tab reverts to summary-cards-only. (Do not delete the CSS — it's harmless and may be reused if the user later edits.)

### Honesty rules

- Never fabricate numbers. If a value isn't reported in the abstract / accessible portion, leave its chip out and write in the narrative "(specific value not reported in the accessible portion)".
- Never invent quotes. If full text wasn't available, paraphrase honestly and write `— paraphrase from abstract` in the `.src` line.
- The deep dive's job is **clarity, not impressiveness**. Short, accurate, grounded > long, hand-wavy, fluent.

---

## 🌳 Figure Tree panel (cross-cutting — REQUIRED for research / clinical / method types)

**The point:** before the reader drills into section-by-section detail, give them a complete **paper map** as a nested tree they can expand/collapse. This is the single most important new component — it is the user's preferred entry point into any new paper.

**Where it goes:** at the **TOP of Tab 1** (Intro / Question / Problem) — it must be the first thing visible when the page loads.

**Two-level nesting using native `<details>`:**
- **Outer node = one Figure** (Fig 1, Fig 2, …). First figure is `open`; the rest collapsed.
- **Inner node = one panel** (a, b, c, …) inside that figure. All collapsed by default.
- Inside each panel: 4 colored blocks for [experiment type · 🧒 kid analogy · 📊 simple result · 💡 story role].

**Why nested `<details>`:** zero JavaScript, works offline, collapse state survives the language toggle, mobile-friendly.

### Required structure per figure node

```html
<div class="panel">
  <h2>🌳
    <span class="lang-kr">피규어 수형도 — 한 눈에 paper map</span>
    <span class="lang-en">Figure Tree — paper map at a glance</span>
  </h2>
  <p style="font-size:13px;color:#666;margin-bottom:14px;">
    <span class="lang-kr">▶ 클릭으로 Figure 펼치기 → ▸ 다시 클릭으로 패널별 실험 자세히 보기</span>
    <span class="lang-en">▶ click a figure to expand → ▸ click a panel to see the experiment in detail</span>
  </p>

  <div class="figure-tree">

    <!-- ===== Figure 1 (open by default) ===== -->
    <details class="fig-node" open>
      <summary>
        <span class="fig-num">Fig 1</span>
        <span class="fig-claim">
          <span class="lang-kr">[[이 figure가 한 줄로 주장하는 것 — KR]]</span>
          <span class="lang-en">[[What this figure claims, one line — EN]]</span>
        </span>
      </summary>
      <div class="fig-body">
        <div class="fig-overview">
          <span class="lang-kr">[[Figure 전체 개요 2-3문장: 어떤 실험들로 무엇을 보여주는지]]</span>
          <span class="lang-en">[[2-3 sentence figure overview: what experiments show what]]</span>
        </div>

        <!-- ----- Panel a ----- -->
        <details class="panel-node">
          <summary>
            <span class="panel-letter">a</span>
            <span class="panel-exp-type">
              <span class="lang-kr">[[실험 종류 KR — 예: scRNA-seq UMAP]]</span>
              <span class="lang-en">[[Experiment type EN]]</span>
            </span>
            <span class="panel-tldr">
              <span class="lang-kr">→ [[한 줄 결과 KR]]</span>
              <span class="lang-en">→ [[one-line result EN]]</span>
            </span>
          </summary>
          <div class="panel-body">

            <div class="panel-block exptype">
              <strong>🔬 <span class="lang-kr">실험 종류 (정확히)</span><span class="lang-en">Experiment type (precisely)</span></strong>
              <span class="lang-kr">[[기술 명·플랫폼·assay 정확히 명시. 예: "10x Genomics 3' v3 chemistry로 잡은 single-cell RNA-seq, 14,000 cells per sample, Seurat v5로 군집화"]]</span>
              <span class="lang-en">[[exact technique/platform/assay. e.g., "10x Genomics 3' v3 single-cell RNA-seq, 14k cells/sample, Seurat v5 clustering"]]</span>
            </div>

            <div class="panel-block analogy">
              <strong>🧒 <span class="lang-kr">초딩도 이해할 비유</span><span class="lang-en">Kid-friendly analogy</span></strong>
              <span class="lang-kr">[[구체적이고 그림이 그려지는 비유. 예: "도시 안의 모든 사람한테 '어떤 일을 하세요?' 물어보고, 비슷한 직업끼리 모아서 동네를 만든 다음, 지도 위에 칠해서 어디에 어떤 동네가 있는지 보는 것."]]</span>
              <span class="lang-en">[[Vivid concrete analogy. e.g., "Ask every person in a city 'what do you do?', group people with similar jobs into neighborhoods, color the map by neighborhood, and look at who lives where."]]</span>
            </div>

            <div class="panel-block result">
              <strong>📊 <span class="lang-kr">간단한 결과</span><span class="lang-en">Simple result</span></strong>
              <span class="lang-kr">[[패널이 실제로 보여주는 것 1-2문장. 가능하면 수치 1개. 예: "14개 세포 종류가 잘 분리되어 보임; HSPC가 전체의 12%."]]</span>
              <span class="lang-en">[[1-2 sentences of what the panel actually shows. Include 1 number if possible.]]</span>
            </div>

            <div class="panel-block meaning">
              <strong>💡 <span class="lang-kr">스토리상 의미</span><span class="lang-en">Story role within the figure</span></strong>
              <span class="lang-kr">[[이 패널이 왜 figure에 있는지 — 다음 패널로 어떻게 연결되는지. 예: "이 UMAP이 다음 패널 b에서 비교할 cell type 정의를 정해줌. 모든 후속 분석의 기준선."]]</span>
              <span class="lang-en">[[Why this panel exists, how it sets up the next panel. e.g., "This UMAP defines the cell types compared in panel b — sets the baseline for everything downstream."]]</span>
            </div>

          </div>
        </details>

        <!-- ----- Panel b, c, d, … same structure ----- -->
        <details class="panel-node">
          <summary>
            <span class="panel-letter">b</span>
            <span class="panel-exp-type">…</span>
            <span class="panel-tldr">…</span>
          </summary>
          <div class="panel-body">
            <!-- 4 .panel-block divs -->
          </div>
        </details>

      </div>
    </details>

    <!-- ===== Figure 2 (collapsed) ===== -->
    <details class="fig-node">
      <summary>
        <span class="fig-num">Fig 2</span>
        <span class="fig-claim">…</span>
      </summary>
      <div class="fig-body">…</div>
    </details>

    <!-- Figures 3, 4, … same structure -->

  </div>
</div>
```

### Required content per panel block

For each panel inside the tree:

| Block | What goes in it |
|---|---|
| 🔬 **Experiment type (precisely)** — `.panel-block.exptype` | Exact assay name, platform, key parameters. The reader may not know the technique — be specific so they can google it. |
| 🧒 **Kid analogy** — `.panel-block.analogy` | A concrete, vivid analogy a 10-year-old can picture. Use everyday objects (city, restaurant, factory, library, school class). 2-3 sentences. |
| 📊 **Simple result** — `.panel-block.result` | What the panel actually shows in 1-2 sentences. Include 1 quantitative anchor (n, %, fold-change) if available. |
| 💡 **Story role** — `.panel-block.meaning` | Why this panel exists in the figure, what it sets up for the next panel or for the figure's overall claim. |

### Honesty rules

- If you don't know the exact technique (full methods not accessible), say "method details not in accessible portion" in the experiment-type block — never invent a platform.
- The kid analogy must be **technically faithful** — a misleading analogy is worse than none.
- The story role should reference actual neighboring panels, not generic phrases like "supports the main claim".

### `--detail=brief` behavior

When `--detail=brief` is passed, **omit the entire Figure Tree panel**. The Intro/Question/Problem tab reverts to its standard background-only content. (CSS stays — harmless.)

---

## 🔬 Method Deep Cards panel (cross-cutting — REQUIRED for research / clinical / method types)

**The point:** the user is **always curious about methods** but standard methods sections are written for experts. Each technique should get a dedicated expandable card with a kid analogy, a "why this method" justification, and explicit limits.

**Where it goes:** at the **TOP of Tab 2** (Methods / Trial Design / Method) — the first panel of that tab.

### Structure

One `<details class="method-deep">` block per major technique. Pick **3–6 techniques** that are central to the paper — don't try to cover everything. Examples of what to include:
- Wet-lab assays: scRNA-seq, scATAC-seq, CUT&Tag, ChIP-seq, BMT, flow cytometry, RNA-FISH, IHC, organoid culture
- Computational: Seurat clustering, DESeq2, MAGeCK, GSEA, CellChat, ArchR, Scanpy, deep learning architecture
- Clinical: randomization scheme, blinding strategy, primary outcome assessment, adaptive trial design

The first card is `open` so the reader sees what a deep card looks like; the rest collapsed.

```html
<div class="panel">
  <h2>🔬
    <span class="lang-kr">방법 자세히 — 어떤 실험인지 비유로 이해하기</span>
    <span class="lang-en">Methods in Depth — understanding each technique by analogy</span>
  </h2>
  <p style="font-size:13px;color:#666;margin-bottom:14px;">
    <span class="lang-kr">▶ 클릭하면 각 기법에 대한 자세한 설명 + 초딩 비유가 펼쳐집니다.</span>
    <span class="lang-en">▶ Click any card to expand the technique with a kid-friendly analogy.</span>
  </p>

  <details class="method-deep" open>
    <summary>
      <span class="method-icon">🧬</span>
      <span class="method-name">
        <span class="lang-kr">scRNA-seq (단일세포 RNA 시퀀싱)</span>
        <span class="lang-en">scRNA-seq (single-cell RNA sequencing)</span>
      </span>
      <span class="method-shorttag">10x Genomics 3' v3</span>
    </summary>
    <div class="method-body">

      <div>
        <h4>📊 <span class="lang-kr">이 기술이 무엇인가</span><span class="lang-en">What this technique is</span></h4>
        <p>
          <span class="lang-kr">[[기술 정의 + 핵심 원리. 2-3문장. 예: "수만 개의 세포 하나하나에서 RNA를 따로 잡아 어떤 유전자가 켜져 있는지 동시에 측정. 10x 플랫폼은 microfluidic droplet 안에 세포 하나 + barcode bead를 넣어 그 droplet 안의 모든 cDNA에 같은 barcode를 붙여 나중에 분리한다."]]</span>
          <span class="lang-en">[[2-3 sentence technical definition. e.g., "Captures RNA from tens of thousands of individual cells in parallel, measuring which genes are on in each one. The 10x platform encapsulates one cell + one barcoded bead per microfluidic droplet so all cDNA from that cell carries the same barcode and can be demultiplexed later."]]</span>
        </p>
      </div>

      <div class="analogy-box">
        <h4>🧒 <span class="lang-kr">초딩도 이해할 비유</span><span class="lang-en">A kid-friendly analogy</span></h4>
        <p>
          <span class="lang-kr">[[구체적이고 그림이 그려지는 비유. 예: "큰 학교에서 학생 한 명 한 명한테 따로 일기장을 줘서 '오늘 무슨 과목 들었어?' 다 적게 한 다음, 그 일기장들을 모아서 '아, 1학년 교실엔 미술 수업이 많고, 4학년엔 과학 수업이 많네!' 알아내는 것. RNA가 일기장 내용이고, 세포가 학생이야."]]</span>
          <span class="lang-en">[[Vivid concrete analogy. e.g., "Imagine handing every student in a huge school their own diary and asking them to write down what classes they took today. Then you collect all the diaries and discover '1st-graders had lots of art, 4th-graders had lots of science.' RNA = diary contents, cells = students."]]</span>
        </p>
      </div>

      <div class="why-box">
        <h4>🎯 <span class="lang-kr">왜 이 방법을 골랐나 (대안 대비)</span><span class="lang-en">Why this method (vs alternatives)</span></h4>
        <p>
          <span class="lang-kr">[[bulk RNA-seq 대비, FACS+qPCR 대비 무엇이 더 좋은지. 예: "Bulk RNA-seq은 전체 조직을 갈아서 평균만 보지만, scRNA-seq은 100개 세포 중 5개에서만 일어나는 변화도 잡을 수 있다. 이 논문에선 senolytic이 특정 minor subpopulation에만 작용해서 bulk로는 사라지는 신호를 봐야 했다."]]</span>
          <span class="lang-en">[[Why this beats bulk RNA-seq, FACS+qPCR, etc. e.g., "Bulk RNA-seq grinds tissue and gives an average; scRNA-seq catches changes happening in just 5 out of 100 cells. In this paper, the senolytic acts on specific minor subpopulations whose signal disappears in bulk."]]</span>
        </p>
      </div>

      <div class="can-see-box">
        <h4>👁️ <span class="lang-kr">이걸로 무엇을 볼 수 있나</span><span class="lang-en">What you can actually see</span></h4>
        <p>
          <span class="lang-kr">[[어떤 데이터·플롯·인사이트가 나오는지. 예: "세포 종류 지도 (UMAP), cell type별 유전자 발현 비교, 새로운 sub-state 발견, trajectory inference로 분화 경로 추적."]]</span>
          <span class="lang-en">[[What outputs/plots/insights you get. e.g., "Cell type maps (UMAPs), per-cell-type DEGs, discovery of new sub-states, trajectory inference of differentiation paths."]]</span>
        </p>
      </div>

      <div class="limit-box">
        <h4>⚠️ <span class="lang-kr">한계 — 이걸론 못하는 것</span><span class="lang-en">Limitations — what it can't tell you</span></h4>
        <p>
          <span class="lang-kr">[[기법의 진짜 한계. 예: "공간 정보 잃음 (어디 있던 세포인지 모름). Drop-out 큼 — 발현이 낮은 유전자는 0으로 측정됨. RNA만 보고 protein은 못 봄. Live cell만 잡혀서 dying senescent cell은 놓칠 수 있음."]]</span>
          <span class="lang-en">[[Real limits. e.g., "Loses spatial info (don't know where the cell was). High drop-out (low-expression genes show as 0). RNA only, no protein. Captures only live cells — dying senescent cells may be missed."]]</span>
        </p>
      </div>

      <div class="paper-quote">
        <span class="lang-kr">[[이 논문이 method 섹션에서 한 직접 인용 — 한국어 번역]]</span>
        <span class="lang-en">[[Direct quote from this paper's methods section, in English]]</span>
        <span class="src">— <span class="lang-kr">[[섹션·페이지]]</span><span class="lang-en">[[Section · page]]</span></span>
      </div>

    </div>
  </details>

  <!-- 2nd, 3rd, … method-deep blocks (collapsed by default) -->
  <details class="method-deep">
    <summary>
      <span class="method-icon">[[emoji]]</span>
      <span class="method-name">
        <span class="lang-kr">[[기법 KR]]</span>
        <span class="lang-en">[[technique EN]]</span>
      </span>
      <span class="method-shorttag">[[platform tag]]</span>
    </summary>
    <div class="method-body">
      <!-- same 5-block structure -->
    </div>
  </details>

</div>
```

### Required content per `<details class="method-deep">`

All five blocks, in this order:

1. **📊 What this technique is** — 2-3 sentence technical definition. Don't dumb down here; give the real mechanism.
2. **🧒 Kid analogy** (`.analogy-box`) — vivid, concrete, picturable. Avoid "imagine if X" without specifics. The best analogies use everyday systems (school, restaurant, mailroom, library, factory floor).
3. **🎯 Why this method (vs alternatives)** (`.why-box`) — explicit comparison. What was the obvious alternative, and why didn't the authors use it? This builds intuition for *why* methods choices matter.
4. **👁️ What you can actually see** (`.can-see-box`) — what data, plots, or insights come out. Concrete output types.
5. **⚠️ Limitations** (`.limit-box`) — real limits of the technique. Be honest. This is the section that builds critical thinking.
6. (Optional but recommended) **`.paper-quote`** — a direct line from the paper's methods describing this assay.

### Method-emoji shortlist (use as `.method-icon`)

| Emoji | Method family |
|---|---|
| 🧬 | scRNA-seq / scATAC-seq / bulk RNA-seq |
| ✂️ | CUT&Tag / CUT&RUN / ChIP-seq |
| 🐭 | Mouse model / BMT / transplant / lineage tracing |
| 🌊 | Flow cytometry / FACS / mass cytometry |
| 🔬 | Microscopy / IHC / IF / FISH |
| 🧪 | qPCR / Western / ELISA / biochem assay |
| 💊 | Drug treatment / dosing schedule |
| 🧮 | Statistical model / DE / GSEA / clustering algorithm |
| 🧠 | Deep learning / neural network architecture |
| 📊 | Bioinformatics pipeline / database query |
| 🩺 | Clinical procedure / randomization / blinding |

### `--detail=brief` behavior

When `--detail=brief`, **omit the Method Deep Cards panel entirely** and revert to the simpler `.method-grid` cards already in the existing schema.

### Honesty rules

- If you can't access the methods section, base each card on what's inferrable from the abstract and label uncertainty in the body ("based on standard 10x v3 chemistry; exact parameters not in accessible portion").
- Never invent a platform/version. "scRNA-seq (platform not specified)" is fine.
- The analogy block must be technically truthful — if it stretches the metaphor too far, prefer a humbler analogy.

---

## SVG illustration library

### Common patterns (all types)

#### Cute cell with face
```svg
<g transform="translate(X,Y)">
  <ellipse cx="0" cy="0" rx="42" ry="38" fill="[[soft pastel]]" stroke="[[darker]]" stroke-width="2.5"/>
  <ellipse cx="-3" cy="-3" rx="20" ry="18" fill="[[lighter]]" stroke="[[dark]]" stroke-width="1.5"/>
  <circle cx="-10" cy="-7" r="2.5" fill="#3a4252"/>
  <circle cx="6" cy="-7" r="2.5" fill="#3a4252"/>
  <path d="M -7,5 Q 0,9 7,5" stroke="#3a4252" stroke-width="1.8" fill="none"/>
  <text class="lang-kr" x="0" y="55" text-anchor="middle" font-size="12" font-weight="bold">[[KR label]]</text>
  <text class="lang-en" x="0" y="55" text-anchor="middle" font-size="12" font-weight="bold">[[EN label]]</text>
</g>
```
Variations: X eyes (😵 dead/aged), zzz (💤), exclamation (⚡), sparkle (✨)

#### Cytokine particle
```svg
<g transform="translate(X,Y)">
  <circle cx="0" cy="0" r="14" fill="[[orange/red/purple]]" stroke="[[darker]]" stroke-width="2"/>
  <text x="0" y="4" text-anchor="middle" font-size="9" font-weight="bold" fill="white">[[name]]</text>
</g>
```

#### Pill / drug
```svg
<g transform="translate(X,Y)">
  <ellipse cx="0" cy="0" rx="35" ry="14" fill="white" stroke="[[color]]" stroke-width="2"/>
  <line x1="-35" y1="0" x2="35" y2="0" stroke="[[color]]" stroke-width="2"/>
  <ellipse cx="-17" cy="0" rx="18" ry="14" fill="[[color]]"/>
</g>
```

---

### REVIEW signature: field-evolution timeline (HTML)
Use the `.timeline` CSS component:
```html
<div class="timeline">
  <div class="timeline-row">
    <div class="timeline-node">
      <div class="year">1980s</div>
      <span class="lang-kr">[[KR landmark]]</span>
      <span class="lang-en">[[EN landmark]]</span>
    </div>
    <div class="timeline-node">
      <div class="year">2000s</div>
      <span class="lang-kr">[[KR]]</span><span class="lang-en">[[EN]]</span>
    </div>
    <!-- 4–6 nodes total -->
  </div>
</div>
```

### REVIEW signature: consensus-vs-controversy SVG icons
- ✅ green checkmark = settled
- ⚡ yellow lightning = active debate
- ❓ purple question mark = unknown
Use these as inline emoji headers for each item in the synthesis list.

---

### META signature: PRISMA flow (HTML)
```html
<div class="prisma-step">
  <span class="lang-kr">📚 식별된 records</span>
  <span class="lang-en">📚 Records identified</span>
  <div class="count">[[n=1234]]</div>
</div>
<div class="prisma-arrow">⬇</div>
<div class="prisma-step">
  <span class="lang-kr">🔍 스크리닝 후</span>
  <span class="lang-en">🔍 After screening</span>
  <div class="count">[[n=234]]</div>
</div>
<div class="prisma-arrow">⬇</div>
<div class="prisma-step">
  <span class="lang-kr">📖 전문 검토</span>
  <span class="lang-en">📖 Full-text assessed</span>
  <div class="count">[[n=56]]</div>
</div>
<div class="prisma-arrow">⬇</div>
<div class="prisma-step" style="background:linear-gradient(135deg,#ffd6e7,#fff);border-color:#d63384;">
  <span class="lang-kr">✅ 최종 포함</span>
  <span class="lang-en">✅ Final included</span>
  <div class="count" style="color:#d63384;">[[n=23]]</div>
</div>
```

### META signature: forest plot row (mix of HTML + inline SVG)
```html
<div class="forest-row">
  <div class="study-name">Smith 2019 (n=234)</div>
  <svg viewBox="0 0 300 30" width="100%" height="30">
    <line x1="150" y1="15" x2="150" y2="15" stroke="#888" stroke-width="1" stroke-dasharray="2,2" y1="0" y2="30"/>
    <!-- vertical "no effect" line at center -->
    <line x1="150" y1="0" x2="150" y2="30" stroke="#888" stroke-width="1" stroke-dasharray="2,2"/>
    <!-- CI bar -->
    <line x1="100" y1="15" x2="180" y2="15" stroke="#5b9bd5" stroke-width="2"/>
    <!-- point estimate square -->
    <rect x="125" y="9" width="12" height="12" fill="#5b9bd5"/>
  </svg>
  <div class="estimate">0.78 [0.62–0.95]</div>
</div>
<!-- Pooled diamond row at bottom -->
<div class="forest-row" style="background:#fff5e6;font-weight:bold;">
  <div class="study-name">
    <span class="lang-kr">통합 추정치</span><span class="lang-en">Pooled estimate</span>
  </div>
  <svg viewBox="0 0 300 30" width="100%" height="30">
    <line x1="150" y1="0" x2="150" y2="30" stroke="#888" stroke-width="1" stroke-dasharray="2,2"/>
    <polygon points="110,15 135,5 160,15 135,25" fill="#d63384"/>
  </svg>
  <div class="estimate" style="color:#d63384;">[[OR/HR + 95% CI]]</div>
</div>
```

---

### CLINICAL signature: patient row SVG
```svg
<svg viewBox="0 0 600 80" width="100%" height="80">
  <!-- one cute patient -->
  <g transform="translate(40,50)">
    <circle cx="0" cy="-22" r="10" fill="[[fill]]" stroke="[[stroke]]" stroke-width="2"/>
    <rect x="-8" y="-12" width="16" height="22" rx="4" fill="[[fill]]" stroke="[[stroke]]" stroke-width="2"/>
    <!-- arms -->
    <line x1="-8" y1="-6" x2="-14" y2="6" stroke="[[stroke]]" stroke-width="2"/>
    <line x1="8" y1="-6" x2="14" y2="6" stroke="[[stroke]]" stroke-width="2"/>
    <!-- legs -->
    <line x1="-4" y1="10" x2="-7" y2="22" stroke="[[stroke]]" stroke-width="2"/>
    <line x1="4" y1="10" x2="7" y2="22" stroke="[[stroke]]" stroke-width="2"/>
    <!-- face -->
    <circle cx="-3" cy="-22" r="1" fill="#3a4252"/>
    <circle cx="3" cy="-22" r="1" fill="#3a4252"/>
  </g>
  <!-- Repeat patient with translate(80,50), translate(120,50), ... -->
</svg>
```
- Treatment arm: `fill="#ffd6e7"` `stroke="#d63384"`
- Control arm: `fill="#cce5ff"` `stroke="#5b9bd5"`
- "Improved" patient: add ✨ above head; "no change": neutral; "worsened": X eyes.

### CLINICAL signature: outcome bar comparison
```svg
<svg viewBox="0 0 400 200" width="100%" height="200">
  <!-- baseline -->
  <line x1="40" y1="170" x2="380" y2="170" stroke="#888" stroke-width="2"/>
  <!-- Treatment bar -->
  <rect x="80" y="50" width="80" height="120" fill="#d63384" rx="6"/>
  <text class="lang-kr" x="120" y="195" text-anchor="middle" font-size="13">치료군</text>
  <text class="lang-en" x="120" y="195" text-anchor="middle" font-size="13">Treatment</text>
  <text x="120" y="40" text-anchor="middle" font-size="14" font-weight="bold" fill="#d63384">[[X%]]</text>
  <!-- Control bar -->
  <rect x="240" y="100" width="80" height="70" fill="#5b9bd5" rx="6"/>
  <text class="lang-kr" x="280" y="195" text-anchor="middle" font-size="13">대조군</text>
  <text class="lang-en" x="280" y="195" text-anchor="middle" font-size="13">Control</text>
  <text x="280" y="90" text-anchor="middle" font-size="14" font-weight="bold" fill="#5b9bd5">[[Y%]]</text>
  <!-- effect annotation -->
  <text x="200" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#5a4fcf">
    [[HR=0.65, p<0.001]]
  </text>
</svg>
```

---

### METHOD signature: protocol step (HTML)
```html
<div class="protocol-step">
  <div class="num">1</div>
  <div>
    <strong><span class="lang-kr">[[KR step name]]</span><span class="lang-en">[[EN step name]]</span></strong>
    <p style="font-size:12px;color:#666;margin-top:4px;">
      <span class="lang-kr">[[KR detail]]</span>
      <span class="lang-en">[[EN detail]]</span>
    </p>
  </div>
</div>
<!-- Repeat with num 2, 3, 4, ... -->
```

### METHOD signature: before/after SVG
Old workflow: cluttered, multiple boxes with arrows zig-zagging, sad face.
New workflow: clean linear pipeline with happy face, fewer steps.
Use the same `cute cell` pattern for the protagonist tool/sample but vary expression.

---

### PERSPECTIVE signature: balance scale (HTML)
```html
<div class="scale">
  <div class="scale-pan for">
    <h4>✅ <span class="lang-kr">저자 주장</span><span class="lang-en">Authors' position</span></h4>
    <ul>
      <li><span class="lang-kr">[[KR pt]]</span><span class="lang-en">[[EN pt]]</span></li>
    </ul>
  </div>
  <div class="scale-pan against">
    <h4>⚡ <span class="lang-kr">반론</span><span class="lang-en">Counterargument</span></h4>
    <ul>
      <li><span class="lang-kr">[[KR pt]]</span><span class="lang-en">[[EN pt]]</span></li>
    </ul>
  </div>
</div>
```

---

### Color palette (use consistently across types)
- Pink (HSC, stem cells, treatment arm): `#ffd6e7` / `#d63384` / `#a3296c`
- Blue (intrinsic, endothelial, control arm): `#cce5ff` / `#5b9bd5` / `#0066cc`
- Orange (niche, inflammation, limitation): `#fff5ec` / `#ed7d31` / `#b85f25`
- Green (MSC, stromal, future, consensus): `#d4f4dd` / `#2e8b57` / `#1b5e20`
- Purple (TF, NF-κB, epigenetic, synthesis): `#f0e6ff` / `#5a4fcf` / `#3a2fa0`
- Yellow (caution, controversy, pooled): `#fff5e6` / `#ffd591` / `#cc8800`

---

## Output checklist (type-aware)

- [ ] Paper type detected and announced in 1 line at the start
- [ ] HTML file saved to `~/work/papers/<FirstAuthor><Year>_<type>_cute.html` (or to the user-supplied override path); directory created via `mkdir -p` first
- [ ] Header includes `.type-badge` with the paper type emoji + label
- [ ] All 4 tabs work; tab labels match the type's schema (see table above)
- [ ] **Type's signature visual is present and prominent** (forest plot for meta, patient grid for clinical, timeline for review, protocol steps for method, balance scale for perspective, mechanism schematic for research)
- [ ] All `[[placeholders]]` replaced with paper-specific content
- [ ] At least one cute SVG scene per tab
- [ ] **🌳 Figure Tree panel present at TOP of Tab 1** (research / clinical / method types, unless `--detail=brief`). Outer `<details class="fig-node">` per figure (first `open`, rest collapsed); inner `<details class="panel-node">` per panel (all collapsed). Each panel body contains all 4 blocks: `.panel-block.exptype` + `.panel-block.analogy` + `.panel-block.result` + `.panel-block.meaning`.
- [ ] **🔬 Method Deep Cards panel present at TOP of Tab 2** (research / clinical / method types, unless `--detail=brief`). 3–6 `<details class="method-deep">` blocks (first `open`, rest collapsed), each with: technique definition + `.analogy-box` (kid analogy) + `.why-box` + `.can-see-box` + `.limit-box`, and ideally a `.paper-quote`.
- [ ] **📔 Results Deep Dive panel present in the Results-equivalent tab** (unless `--detail=brief`); each `<details class="deep-dive">` contains: `.numbers-strip` + "what was measured" narrative + `.paper-quote` + "why it matters" narrative; first block has `open` attribute, the rest collapsed
- [ ] No fabricated numbers, quotes, analogies, or platform names — if the value/quote/method detail wasn't accessible, omit and note it honestly in the narrative
- [ ] **EVERY visible text element has both `<span class="lang-kr">` and `<span class="lang-en">` versions**
- [ ] **SVG `<text>` labels also bilingual** (paired lang-kr/lang-en at same coords)
- [ ] Language toggle button in top-right works
- [ ] Default state is `<body class="lang-kr">` with Korean visible
- [ ] Korean: scientific but accessible (explain jargon)
- [ ] English: idiomatic, native-sounding scientific writing (NOT word-for-word translation)
- [ ] Footer cites the original DOI / PubMed link
- [ ] No external dependencies (all CSS + SVG inline)

## Verification step (do this before finishing)

After Write, use Grep to count `class="lang-kr"` and `class="lang-en"` occurrences in the saved file. They should be approximately equal (within ~20%). If they differ more, you've forgotten to translate something — go back and fix.

Also count (for research / clinical / method types in deep mode):
- `<details class="fig-node"` — should equal the number of figures in the paper (typically 4–8 for a research paper).
- `<details class="panel-node"` — should be the total panel count across all figures (typically 3–6× the number of figures).
- `<details class="method-deep"` — should be 3–6.
- `<details class="deep-dive"` — should be 2–4 (one per major finding).

If any of these counts is **0** when it should be present, the component is missing — go back and add it before reporting done.

Also: open the file mentally and ask:
1. **"Can I tell what kind of paper this is from the visuals alone, without reading any text?"** If no, the type's signature visual isn't prominent enough.
2. **"If I open the page and click only the Figure Tree, can I get a high-level grasp of the entire paper before touching any other tab?"** If no, the tree is missing claims, panels, or analogies.
3. **"If I read only the Method Deep Cards, can I explain each technique to a curious non-specialist?"** If no, the analogies need work.
