#!/usr/bin/env python3
"""Highlight live-typed code in exercises_solutions.html.

Marks the code lines that are NOT pre-filled in the student notebook
(exercises.qmd): yellow for walkthrough code the instructor types live,
blue for exercise code students write themselves. Everything unhighlighted
comes pre-filled in the class notebook. Also widens the content column.

Run by .github/workflows/render-solutions.yml right after Quarto renders and
before the HTML is committed, so the published page keeps its highlighting.
Also safe to run by hand after a local render:
    python3 scripts/highlight_typed_code.py

Idempotent: strips any previous highlight pass before applying a new one.

If a RULES entry stops matching (a variable renamed in the solutions qmd,
a cell split), this exits non-zero WITHOUT writing, so CI publishes the plain
render rather than a half-marked page. Fix the rule here, do not hand-edit the
generated HTML.
"""
import html as html_mod
import os
import re
import sys

HTML = os.path.join(os.path.dirname(__file__), "..", "exercises_solutions.html")
WT = "typed-wt"   # instructor types in walkthrough
EX = "typed-ex"   # students write in exercise

# (signature, mode, css_class) applied to code blocks in document order.
# signature: substring that must appear in the block's plain text
#            ("line_exact:" = a line equal to it after stripping).
# mode: "all" (every code line), "first_prefix:<p>" (just the line starting
#       with <p>), "from:<p>" (that line to end of block),
#       "all_except_totalspent" (all but the TotalSpent block).
RULES = [
    ("line_exact:marketing_campaign_raw", "all", EX),
    ("marketing_campaign_raw.info()", "all", EX),
    ("marketing_campaign_raw.isnull().sum()", "all", EX),
    ("marketing_campaign_raw.duplicated().sum()", "all", EX),
    ('marketing_campaign["Kidhome"]', "all_except_totalspent", EX),
    ("marketing_campaign.describe(include='all')", "all", EX),
    ("x='Response', y='Income'", "all", EX),
    ("sns.histplot(data=marketing_campaign, x='TotalSpent')", "all", EX),
    ("x='Income', y='TotalSpent'", "all", EX),
    ("x='Education', hue='Response'", "all", EX),
    ("X = telco_churn[['AvgServiceUsageScore']]", "all", WT),
    ("lr = LinearRegression()", "all", WT),
    ("y_pred = lr.predict(X_val)", "all", WT),
    ("X_m = marketing_campaign[['Income']]", "all", EX),
    ("lr_m = LinearRegression()", "all", EX),
    ("y_m_pred = lr_m.predict(X_m_val)", "all", EX),
    ("clf = RandomForestClassifier", "all", WT),
    ("features_m = ['Income', 'TotalSpent', 'TotalChildren']", "all", EX),
    ("clf_m = RandomForestClassifier", "all", EX),
    ("y_m_pred_class = clf_m.predict", "all", EX),
    ("optimal_k = 3", "all", WT),
    ("features_cluster = ['Income', 'TotalSpent', 'TotalChildren']", "all", EX),
    ("kmeans.fit(X_cluster_scaled)", "all", EX),
    ("labels = kmeans.fit_predict(X_cluster_scaled)", "all", EX),
    ("optimal_k = 5", "all", EX),
    ("x='TotalChildren', y='TotalSpent'", "all", EX),
    ("apriori(telco_churn_basket", "all", WT),
    ("rules = association_rules", "first_prefix:rules = association_rules", WT),
    ("apriori(basket", "all", EX),
    ("rules = association_rules", "all", EX),
    ("cv_results = cross_validate", "all", WT),
    ("X_m = marketing_campaign[['Income', 'TotalSpent', 'TotalChildren']]", "all", EX),
    ("logreg_m = make_pipeline", "all", EX),
    ("cv_results_m = cross_validate", "all", EX),
    ("show_metric(m, cv_results_m)", "all", EX),
    ("grid_search = GridSearchCV", "from:grid_search = GridSearchCV(", WT),
    ("rf_m = RandomForestClassifier", "all", EX),
    ("grid_search_m = GridSearchCV", "from:grid_search_m = GridSearchCV(", EX),
    ("best_rf_m = grid_search_m.best_estimator_", "all", EX),
    ("grid_search_m.best_params_", "all", EX),
]

STYLE = """
<style id="typed-highlight-style">
.typed-wt { background-color: #fff3cd; box-shadow: -4px 0 0 #f0ad4e; }
.typed-ex { background-color: #d9edf7; box-shadow: -4px 0 0 #5bc0de; }
.typed-legend { border: 1px solid #ddd; border-radius: 6px;
  padding: 10px 14px; margin: 14px 0; font-size: 0.95em; }
/* Widen the main content column (Quarto default caps it near 800px).
   Grows with the window, capped at 1450px, leaving room for the right TOC. */
@media (min-width: 992px) {
  body .page-columns {
    grid-template-columns:
      [screen-start] 1.5em
      [screen-start-inset page-start page-start-inset body-start-outset] 5fr
      [body-start] 1.5em
      [body-content-start] minmax(500px, min(1450px, calc(100vw - 310px)))
      [body-content-end] 1.5em
      [body-end] 35px
      [body-end-outset] minmax(75px, 145px)
      [page-end-inset] 35px
      [page-end] 5fr
      [screen-end-inset] 1.5em
      [screen-end];
  }
}
</style>
"""

LEGEND = """
<div class="typed-legend" id="typed-highlight-legend">
<strong>Highlight key:</strong>
<span class="typed-wt">&nbsp;yellow&nbsp;</span> = typed live during the walkthroughs;
<span class="typed-ex">&nbsp;blue&nbsp;</span> = written by students in the exercises.
Unhighlighted code is pre-filled in the class notebook.
</div>
"""


def strip_tags(s):
    return html_mod.unescape(re.sub(r"<[^>]+>", "", s))


def main():
    src = open(HTML, encoding="utf-8").read()

    # Idempotency: remove any earlier pass.
    src = re.sub(r'\n?<style id="typed-highlight-style">.*?</style>\n?', "",
                 src, flags=re.S)
    src = re.sub(r'\n?<div class="typed-legend" id="typed-highlight-legend">'
                 r".*?</div>\n?", "", src, flags=re.S)
    src = re.sub(r'(<span id="cb\d+-\d+") class="typed-(?:wt|ex)">', r"\1>", src)

    open_pat = re.compile(r'<span id="(cb\d+)-(\d+)">')
    matches = list(open_pat.finditer(src))
    blocks, order = {}, []
    for i, m in enumerate(matches):
        bid, ln = m.group(1), int(m.group(2))
        nxt = matches[i + 1].start() if i + 1 < len(matches) else len(src)
        code_end = src.find("</code>", m.end())
        end = min(nxt, code_end) if code_end != -1 else nxt
        text = strip_tags(src[m.end():end]).rstrip("\n")
        if bid not in blocks:
            blocks[bid] = []
            order.append(bid)
        blocks[bid].append((ln, text))

    def is_code(t):
        s = t.strip()
        return bool(s) and not s.startswith("#")

    marked = {}  # (bid, ln) -> class
    ptr = 0
    for sig, mode, cls in RULES:
        found = None
        for j in range(ptr, len(order)):
            bid = order[j]
            lines = blocks[bid]
            joined = "\n".join(t for _, t in lines)
            if sig.startswith("line_exact:"):
                hit = any(t.strip() == sig[len("line_exact:"):] for _, t in lines)
            else:
                hit = sig in joined
            if hit:
                found = j
                break
        if found is None:
            sys.exit(f"RULE NOT MATCHED, nothing written: {sig!r} (mode {mode})")
        ptr = found + 1
        bid = order[found]
        lines = blocks[bid]
        if mode == "all":
            chosen = [ln for ln, t in lines if is_code(t)]
        elif mode == "all_except_totalspent":
            chosen, skipping = [], False
            for ln, t in lines:
                s = t.strip()
                if s.startswith('marketing_campaign["TotalSpent"] = ('):
                    skipping = True
                if not skipping and is_code(t):
                    chosen.append(ln)
                if skipping and s == ")":
                    skipping = False
        elif mode.startswith("first_prefix:"):
            pref = mode[len("first_prefix:"):]
            chosen = [next(ln for ln, t in lines if t.strip().startswith(pref))]
        elif mode.startswith("from:"):
            pref = mode[len("from:"):]
            start = next(ln for ln, t in lines if t.strip().startswith(pref))
            chosen = [ln for ln, t in lines if ln >= start and is_code(t)]
        else:
            sys.exit(f"unknown mode {mode!r}")
        for ln in chosen:
            marked[(bid, ln)] = cls

    def add_class(m):
        cls = marked.get((m.group(1), int(m.group(2))))
        return f'<span id="{m.group(1)}-{m.group(2)}" class="{cls}">' if cls \
            else m.group(0)

    src = open_pat.sub(add_class, src)
    src = src.replace("</head>", STYLE + "</head>", 1)
    hdr = src.find("</header>")
    if hdr == -1:
        sys.exit("no </header> found for legend insertion, nothing written")
    src = src[:hdr + len("</header>")] + LEGEND + src[hdr + len("</header>"):]

    open(HTML, "w", encoding="utf-8").write(src)
    wt = sum(1 for c in marked.values() if c == WT)
    ex = sum(1 for c in marked.values() if c == EX)
    print(f"highlighted {wt} walkthrough-typed lines, {ex} exercise-typed lines "
          f"across {len(set(b for b, _ in marked))} code blocks")


if __name__ == "__main__":
    main()
