"""
/contribute Plugin - Comprehensive Documentation PDF Generator
Generates a professional dark-themed PDF covering all 11 phases,
6 core rules, operating modes, test gate, agents, and architecture.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem,
    Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable

# ─── Colors ───
BG_DARK = HexColor("#0d1117")
BG_CARD = HexColor("#161b22")
BG_CARD_ALT = HexColor("#1c2129")
BORDER = HexColor("#30363d")
TEXT_PRIMARY = HexColor("#e6edf3")
TEXT_SECONDARY = HexColor("#8b949e")
TEXT_MUTED = HexColor("#6e7681")
ACCENT_BLUE = HexColor("#58a6ff")
ACCENT_PURPLE = HexColor("#8b5cf6")
ACCENT_GREEN = HexColor("#3fb950")
ACCENT_YELLOW = HexColor("#d29922")
ACCENT_RED = HexColor("#f85149")
ACCENT_ORANGE = HexColor("#d18616")
ACCENT_CYAN = HexColor("#39d2c0")
WHITE = HexColor("#ffffff")
HEADER_BG = HexColor("#0d1117")
TABLE_HEADER_BG = HexColor("#21262d")
TABLE_ROW_BG = HexColor("#161b22")
TABLE_ROW_ALT = HexColor("#1c2129")
CODE_BG = HexColor("#1a1f26")


# ─── Styles ───
def make_styles():
    s = {}
    s["title"] = ParagraphStyle(
        "Title", fontName="Helvetica-Bold", fontSize=28,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=6,
        leading=34
    )
    s["subtitle"] = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=13,
        textColor=TEXT_SECONDARY, alignment=TA_CENTER,
        spaceAfter=20, leading=18
    )
    s["h1"] = ParagraphStyle(
        "H1", fontName="Helvetica-Bold", fontSize=22,
        textColor=ACCENT_BLUE, spaceBefore=24, spaceAfter=10,
        leading=28, borderPadding=(0, 0, 4, 0)
    )
    s["h2"] = ParagraphStyle(
        "H2", fontName="Helvetica-Bold", fontSize=16,
        textColor=ACCENT_PURPLE, spaceBefore=18, spaceAfter=8,
        leading=22
    )
    s["h3"] = ParagraphStyle(
        "H3", fontName="Helvetica-Bold", fontSize=13,
        textColor=ACCENT_GREEN, spaceBefore=12, spaceAfter=6,
        leading=18
    )
    s["h4"] = ParagraphStyle(
        "H4", fontName="Helvetica-Bold", fontSize=11,
        textColor=ACCENT_CYAN, spaceBefore=8, spaceAfter=4,
        leading=15
    )
    s["body"] = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10,
        textColor=TEXT_PRIMARY, spaceAfter=6,
        leading=15, alignment=TA_JUSTIFY
    )
    s["body_indent"] = ParagraphStyle(
        "BodyIndent", fontName="Helvetica", fontSize=10,
        textColor=TEXT_PRIMARY, spaceAfter=6,
        leading=15, leftIndent=20, alignment=TA_JUSTIFY
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=10,
        textColor=TEXT_PRIMARY, spaceAfter=4,
        leading=14, leftIndent=20, bulletIndent=8,
        bulletFontName="Helvetica", bulletFontSize=10,
        bulletColor=ACCENT_BLUE
    )
    s["code"] = ParagraphStyle(
        "Code", fontName="Courier", fontSize=8.5,
        textColor=ACCENT_GREEN, spaceAfter=6,
        leading=12, leftIndent=12, backColor=CODE_BG,
        borderPadding=(6, 6, 6, 6), borderColor=BORDER,
        borderWidth=0.5, borderRadius=3
    )
    s["code_block"] = ParagraphStyle(
        "CodeBlock", fontName="Courier", fontSize=8,
        textColor=HexColor("#c9d1d9"), spaceAfter=8,
        leading=11, leftIndent=12, backColor=CODE_BG,
        borderPadding=(8, 8, 8, 8), borderColor=BORDER,
        borderWidth=0.5
    )
    s["note"] = ParagraphStyle(
        "Note", fontName="Helvetica-Oblique", fontSize=9.5,
        textColor=ACCENT_YELLOW, spaceAfter=8,
        leading=14, leftIndent=12, borderPadding=(4, 4, 4, 4)
    )
    s["warning"] = ParagraphStyle(
        "Warning", fontName="Helvetica-Bold", fontSize=10,
        textColor=ACCENT_RED, spaceAfter=8,
        leading=14, leftIndent=12
    )
    s["toc_entry"] = ParagraphStyle(
        "TOC", fontName="Helvetica", fontSize=11,
        textColor=ACCENT_BLUE, spaceAfter=4,
        leading=16, leftIndent=12
    )
    s["toc_sub"] = ParagraphStyle(
        "TOCSub", fontName="Helvetica", fontSize=10,
        textColor=TEXT_SECONDARY, spaceAfter=3,
        leading=14, leftIndent=30
    )
    s["footer"] = ParagraphStyle(
        "Footer", fontName="Helvetica", fontSize=8,
        textColor=TEXT_MUTED, alignment=TA_CENTER
    )
    s["table_header"] = ParagraphStyle(
        "TableHeader", fontName="Helvetica-Bold", fontSize=9,
        textColor=WHITE, leading=13, alignment=TA_LEFT
    )
    s["table_cell"] = ParagraphStyle(
        "TableCell", fontName="Helvetica", fontSize=9,
        textColor=TEXT_PRIMARY, leading=13, alignment=TA_LEFT
    )
    s["table_cell_code"] = ParagraphStyle(
        "TableCellCode", fontName="Courier", fontSize=8,
        textColor=ACCENT_GREEN, leading=12, alignment=TA_LEFT
    )
    s["phase_num"] = ParagraphStyle(
        "PhaseNum", fontName="Helvetica-Bold", fontSize=36,
        textColor=ACCENT_PURPLE, alignment=TA_CENTER, leading=42
    )
    return s


class AccentLine(Flowable):
    """A gradient-like accent line."""
    def __init__(self, width, color=ACCENT_BLUE, thickness=2):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def page_bg(canvas, doc):
    """Draw dark background on every page."""
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Footer
    canvas.setFillColor(TEXT_MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 20,
                              f"/contribute Documentation  |  v1.0.0  |  Page {doc.page}")
    # Top accent line
    canvas.setStrokeColor(ACCENT_PURPLE)
    canvas.setLineWidth(1.5)
    canvas.line(40, A4[1] - 35, A4[0] - 40, A4[1] - 35)
    canvas.restoreState()


def title_page_bg(canvas, doc):
    """Special background for the title page."""
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Gradient-like top bar
    canvas.setFillColor(ACCENT_PURPLE)
    canvas.rect(0, A4[1] - 6, A4[0], 6, fill=1, stroke=0)
    canvas.setFillColor(ACCENT_BLUE)
    canvas.rect(0, A4[1] - 10, A4[0], 4, fill=1, stroke=0)
    canvas.restoreState()


def make_table(headers, rows, col_widths=None, style_extra=None):
    """Create a styled table."""
    S = make_styles()
    data = [[Paragraph(h, S["table_header"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S["table_cell"]) for c in row])

    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
    ]
    # Alternate row backgrounds
    for i in range(1, len(data)):
        bg = TABLE_ROW_BG if i % 2 == 1 else TABLE_ROW_ALT
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    if style_extra:
        style_cmds.extend(style_extra)
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf():
    S = make_styles()
    story = []
    W = A4[0] - 80  # usable width

    # ═══════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════
    story.append(Spacer(1, 120))

    # Try to include banner
    banner_path = os.path.join(os.path.dirname(__file__), "banner.png")
    if os.path.exists(banner_path):
        try:
            img = Image(banner_path, width=W, height=W * 0.3)
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception:
            pass

    story.append(Paragraph("/contribute", S["title"]))
    story.append(Spacer(1, 8))
    story.append(AccentLine(W, ACCENT_PURPLE, 2))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Full-Lifecycle Open-Source Contribution Workflow",
        S["subtitle"]
    ))
    story.append(Paragraph(
        "Find issues. Analyze repos. Write code. Validate with industrial-grade testing. Submit PRs. Respond to reviews.",
        ParagraphStyle("SubDesc", fontName="Helvetica", fontSize=10,
                       textColor=TEXT_SECONDARY, alignment=TA_CENTER,
                       leading=15, spaceAfter=30)
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "One command. Every phase.",
        ParagraphStyle("Tagline", fontName="Helvetica-Bold", fontSize=14,
                       textColor=ACCENT_GREEN, alignment=TA_CENTER,
                       spaceAfter=40, leading=20)
    ))

    # Version info
    info_data = [
        ["Version", "1.0.0"],
        ["License", "MIT"],
        ["Author", "LuciferDono"],
        ["Repository", "github.com/LuciferDono/contribute"],
        ["Platform", "Claude Code (primary) + Cursor, Antigravity"],
    ]
    info_table = Table(
        [[Paragraph(r[0], ParagraphStyle("IK", fontName="Helvetica-Bold",
                                          fontSize=9, textColor=ACCENT_BLUE)),
          Paragraph(r[1], ParagraphStyle("IV", fontName="Helvetica",
                                          fontSize=9, textColor=TEXT_PRIMARY))]
         for r in info_data],
        colWidths=[120, 300]
    )
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════
    story.append(Paragraph("Table of Contents", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 12))

    toc_items = [
        ("1.", "Overview", []),
        ("2.", "Core Rules", [
            "Rule 1: Read Is Free, Write Requires Permission",
            "Rule 2: No Co-Authored-By",
            "Rule 3: Three Operating Modes",
            "Rule 4: Respect Upstream Conventions",
            "Rule 5: Opus Only for Subagents",
            "Rule 6: Verify Issue Is Not Taken",
        ]),
        ("3.", "Phase Reference and Dependencies", []),
        ("4.", "Phase 1: Discover", []),
        ("5.", "Phase 2: Analyze", []),
        ("6.", "Phase 3: Work", []),
        ("7.", "Phase 4: Test", []),
        ("8.", "Phase 5: Submit", []),
        ("9.", "Phase 6: Review", []),
        ("10.", "Phase 7: PR Review", []),
        ("11.", "Phase 8: Release", []),
        ("12.", "Phase 9: Triage", []),
        ("13.", "Phase 10: Sync", []),
        ("14.", "Phase 11: Cleanup", []),
        ("15.", "Agents", ["issue-scout", "deep-reviewer"]),
        ("16.", "State Files", []),
        ("17.", "Plugin Architecture", []),
        ("18.", "Cross-Tool Compatibility", []),
        ("19.", "Test Applicability Matrix", []),
    ]
    for num, title, subs in toc_items:
        story.append(Paragraph(
            f'<font color="{ACCENT_PURPLE.hexval()}">{num}</font>  {title}',
            S["toc_entry"]
        ))
        for sub in subs:
            story.append(Paragraph(f"- {sub}", S["toc_sub"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 1. OVERVIEW
    # ═══════════════════════════════════════
    story.append(Paragraph("1. Overview", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Contributing to open source is high-friction. Finding the right issue takes hours of browsing. "
        "Understanding a new codebase takes days. Matching upstream conventions means reading scattered docs. "
        "Submitting a quality PR means running tests, linters, security checks manually. "
        "Responding to review feedback is another context switch.",
        S["body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '<b><font color="#3fb950">/contribute</font></b> turns the entire process into a guided, '
        '11-phase workflow. One command per phase. Built-in safety rails. Industrial-grade testing '
        'with an 85% quality gate before you can submit.',
        S["body"]
    ))
    story.append(Spacer(1, 10))

    # Workflow diagram as text
    story.append(Paragraph("Workflow Pipeline", S["h3"]))
    story.append(Paragraph(
        '<font name="Courier" color="#58a6ff">'
        'discover -&gt; analyze -&gt; work -&gt; test -&gt; submit -&gt; review<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sync (anytime)<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cleanup (anytime)<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;triage (standalone)<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pr-review (standalone)<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;release (standalone)'
        '</font>',
        S["code_block"]
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 2. CORE RULES
    # ═══════════════════════════════════════
    story.append(Paragraph("2. Core Rules", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Six non-negotiable rules govern every action across every phase, every subagent. "
        "Violating any rule is a hard failure.",
        S["body"]
    ))
    story.append(Spacer(1, 8))

    # Rule 1
    story.append(Paragraph("Rule 1: Read Is Free, Write Requires Permission", S["h2"]))
    story.append(Paragraph(
        "All read-only operations are freely performed: fetching repos, cloning, reading files, "
        "searching code, browsing issues and PRs, running analysis tools, using GitHub CLI for reads.",
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#f85149"><b>Write operations require explicit user approval before execution:</b></font> '
        "creating forks, creating/switching branches, staging files, committing, pushing, "
        "opening/closing/commenting on issues or PRs, posting content visible to others, "
        "modifying files outside the local working copy.",
        S["body"]
    ))
    story.append(Paragraph(
        "When asking permission, the agent states exactly what will happen, which remote or "
        "repository is affected, and what the consequence will be. Multiple write operations "
        "are never bundled into a single approval request.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Rule 2
    story.append(Paragraph("Rule 2: No Co-Authored-By", S["h2"]))
    story.append(Paragraph(
        '<font color="#f85149"><b>Zero exceptions.</b></font> Under no circumstances add a '
        "Co-Authored-By trailer, AI attribution line, or any marker indicating AI involvement. "
        "Every commit appears as sole-authored by the logged-in GitHub user. Identity is determined via:",
        S["body"]
    ))
    story.append(Paragraph(
        '<font name="Courier" color="#3fb950">gh api user --jq \'.login\'</font> and '
        '<font name="Courier" color="#3fb950">git config user.name / git config user.email</font>',
        S["body_indent"]
    ))
    story.append(Paragraph(
        "Verification after every commit:",
        S["body"]
    ))
    story.append(Paragraph(
        '<font name="Courier" color="#3fb950">git log -1 --format="%an &lt;%ae&gt;%n%(trailers:key=Co-authored-by)"</font>',
        S["code"]
    ))
    story.append(Spacer(1, 6))

    # Rule 3
    story.append(Paragraph("Rule 3: Three Operating Modes", S["h2"]))
    story.append(Paragraph(
        "At the start of the work phase, the user selects their preferred level of AI autonomy:",
        S["body"]
    ))
    modes_table = make_table(
        ["Mode", "AI Does", "User Does"],
        [
            ["<b>do</b>", "Everything: code, tests, formatting, validation", "Review diffs, approve write operations"],
            ["<b>guide</b>", "Explain each step, provide snippets and commands", "Execute the commands, write the code"],
            ["<b>adaptive</b>", "Boilerplate, scaffolding, mechanical work", "Logic, design decisions, algorithmic choices"],
        ],
        col_widths=[70, 200, 200]
    )
    story.append(modes_table)
    story.append(Paragraph(
        "The mode persists in <font name='Courier' color='#3fb950'>.claude/contribute-conventions.md</font> "
        "for the duration of the contribution.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Rule 4
    story.append(Paragraph("Rule 4: Respect Upstream Conventions", S["h2"]))
    story.append(Paragraph(
        "Before writing any code, the agent reads and internalizes: CONTRIBUTING.md, CODE_OF_CONDUCT.md, "
        ".editorconfig, linter/formatter configs, PR/issue templates, recent merged PRs for actual conventions, "
        "branch naming conventions, and commit message format. The project's style is matched exactly. "
        "No personal preferences imposed.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Rule 5
    story.append(Paragraph("Rule 5: Opus Only for Subagents", S["h2"]))
    story.append(Paragraph(
        'Every subagent spawned by this skill must use model <font name="Courier" color="#3fb950">opus</font>. '
        "No exceptions for quick or simple tasks. This applies to all Task tool invocations, "
        "all parallel agents, all background agents.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Rule 6
    story.append(Paragraph("Rule 6: Verify Issue Is Not Taken", S["h2"]))
    story.append(Paragraph(
        "Before recommending or analyzing any issue, all four availability checks must pass:",
        S["body"]
    ))
    checks_table = make_table(
        ["Check", "Method", "If Failed"],
        [
            ["Assignees", "gh issue view --json assignees", "Issue is taken, skip"],
            ["Open PRs", 'gh search prs --state=open "issue_number"', "Issue is taken, skip"],
            ["Comment claims", "Read comments for claims within 14 days", "Taken if maintainer acknowledged"],
            ["Linked PRs", "gh issue view --json closedByPullRequests", "Issue is taken, skip"],
        ],
        col_widths=[85, 200, 185]
    )
    story.append(checks_table)
    story.append(Paragraph(
        "Stale claims older than 30 days with no follow-up PR can be ignored. "
        "If taken, the issue is not presented (discover) or the user is immediately informed (analyze).",
        S["body"]
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 3. PHASE REFERENCE & DEPENDENCIES
    # ═══════════════════════════════════════
    story.append(Paragraph("3. Phase Reference and Dependencies", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))

    phase_table = make_table(
        ["#", "Phase", "Command", "Purpose"],
        [
            ["1", "Discover", "/contribute discover", "Find matching open-source issues"],
            ["2", "Analyze", "/contribute analyze URL", "Deep-dive into repo and issue"],
            ["3", "Work", "/contribute work", "Implement the contribution"],
            ["4", "Test", "/contribute test", "Industrial-grade validation (85% gate)"],
            ["5", "Submit", "/contribute submit", "Push and open PR"],
            ["6", "Review", "/contribute review", "Monitor PR, respond to feedback"],
            ["7", "PR Review", "/contribute pr-review URL", "Review someone else's PR"],
            ["8", "Release", "/contribute release", "Create GitHub releases"],
            ["9", "Triage", "/contribute triage URL", "Triage upstream issues"],
            ["10", "Sync", "/contribute sync", "Keep fork in sync with upstream"],
            ["11", "Cleanup", "/contribute cleanup", "Clean up contribution state"],
        ],
        col_widths=[25, 65, 145, 235]
    )
    story.append(phase_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Phase Dependencies", S["h3"]))
    story.append(Paragraph(
        '<b>test</b> writes <font name="Courier" color="#3fb950">.claude/contribute-test-report.md</font> '
        '&#8212; submit reads it and refuses if score &lt; 85% or any BLOCKER exists.',
        S["bullet"]
    ))
    story.append(Paragraph(
        '<b>analyze</b> writes <font name="Courier" color="#3fb950">.claude/contribute-conventions.md</font> '
        '&#8212; all subsequent phases read it.',
        S["bullet"]
    ))
    story.append(Paragraph(
        '<b>work</b> requires <font name="Courier" color="#3fb950">.claude/contribute-conventions.md</font> to exist.',
        S["bullet"]
    ))
    story.append(Paragraph(
        '<b>submit</b> requires <font name="Courier" color="#3fb950">.claude/contribute-test-report.md</font> with passing score.',
        S["bullet"]
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # PHASES 1-11 (detailed)
    # ═══════════════════════════════════════

    # --- PHASE 1: DISCOVER ---
    story.append(Paragraph("4. Phase 1: Discover", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Find open-source issues that match the user\'s skills, '
        'interests, and available time.',
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Entry point:</b></font> <font name="Courier" color="#3fb950">/contribute discover</font>',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 1: Understand What the User Wants", S["h3"]))
    story.append(Paragraph(
        "A single question is asked with five options:",
        S["body"]
    ))
    options = [
        ("<b>A)</b> I have a specific repo or issue in mind &#8212; transitions directly to analyze"),
        ("<b>B)</b> Find me something in AI/ML/Data Science (Python) &#8212; ML, deep learning, NLP, CV domains"),
        ("<b>C)</b> Find me something in systems programming (C/C++) &#8212; compilers, runtimes, databases, OS"),
        ("<b>D)</b> Find me something in frontend &#8212; JS/TS frameworks, UI libraries, design systems"),
        ("<b>E)</b> Surprise me &#8212; searches across all domains, prioritizing highly-starred repos"),
    ]
    for opt in options:
        story.append(Paragraph(opt, S["bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 2: Search GitHub for Candidate Issues", S["h3"]))
    story.append(Paragraph(
        "Multiple parallel searches are executed via GitHub CLI:",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Label-based search:</b> Issues with <font name='Courier' color='#3fb950'>good first issue</font> "
        "and <font name='Courier' color='#3fb950'>help wanted</font> labels, sorted by recently updated, "
        "limited to 20 results per query.",
        S["body_indent"]
    ))
    story.append(Paragraph(
        "<b>Activity-based filtering:</b> Discard issues inactive for 90+ days, issues with linked PRs, "
        "repos with fewer than 50 stars. Rule 6 is applied to every candidate.",
        S["body_indent"]
    ))
    story.append(Paragraph(
        "<b>Quality signals:</b> CONTRIBUTING.md exists, CI configured, clear acceptance criteria, "
        "maintainer has responded, repo has had a release in the last 6 months.",
        S["body_indent"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3: Present and Persist the Shortlist", S["h3"]))
    story.append(Paragraph(
        "3-5 candidate issues are presented with: stars, language, last activity, labels, complexity "
        "(Small/Medium/Large), and reasoning. The shortlist is persisted to "
        "<font name='Courier' color='#3fb950'>.claude/contribute-discover.md</font>.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Complexity categories:</b>",
        S["body"]
    ))
    cx_table = make_table(
        ["Complexity", "Files", "Lines", "Description"],
        [
            ["Small", "1-2", "< 50", "Straightforward fix"],
            ["Medium", "3-5", "50-200", "Requires understanding a subsystem"],
            ["Large", "5+", "200+", "Requires understanding architecture"],
        ],
        col_widths=[75, 50, 55, 290]
    )
    story.append(cx_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 4: User Selects", S["h3"]))
    story.append(Paragraph(
        "The user picks by number or requests a new search. Selection transitions to the analyze phase.",
        S["body"]
    ))
    story.append(PageBreak())

    # --- PHASE 2: ANALYZE ---
    story.append(Paragraph("5. Phase 2: Analyze", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Build a complete mental model of the repository, '
        'the issue, and the optimal contribution strategy before touching any code.',
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Entry point:</b></font> '
        '<font name="Courier" color="#3fb950">/contribute analyze URL</font>',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 1: Read Contribution Rules", S["h3"]))
    story.append(Paragraph(
        "Fetch and read in parallel: CONTRIBUTING.md, CODE_OF_CONDUCT.md, PR/issue templates, "
        ".editorconfig, linter/formatter configs, build system files (Makefile, CMakeLists.txt, "
        "setup.py, package.json), and CI workflows. Branch naming is inferred from recent PRs if not documented.",
        S["body"]
    ))
    story.append(Paragraph(
        "The synthesized conventions are written to "
        "<font name='Courier' color='#3fb950'>.claude/contribute-conventions.md</font>.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 2: Understand the Codebase", S["h3"]))
    story.append(Paragraph(
        "Structured exploration: project structure, architecture (entry points, module organization), "
        "build system (build, install, test), test framework (runner, directory, naming, single-test command), "
        "and dependencies. Installing dependencies is a write operation requiring explicit permission.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3: Analyze the Specific Issue", S["h3"]))
    story.append(Paragraph(
        '<font color="#f85149"><b>GATE CHECK (Rule 6):</b></font> Before deep analysis, verify the issue is not taken. '
        "If taken, STOP immediately, inform the user, and suggest pivoting.",
        S["body"]
    ))
    story.append(Paragraph(
        "Then: read the full issue thread extracting the core ask, maintainer signals, and prior attempts. "
        "Trace relevant code paths. Identify files to modify. Search for related open/closed PRs.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 4: Present the Contribution Brief", S["h3"]))
    story.append(Paragraph(
        "A structured brief is presented covering: issue summary, core ask, maintainer signals, "
        "prior attempts, upstream conventions (branch naming, commit format, test framework, linter, "
        "PR template), files to modify, environment setup commands, recommended approach with edge cases, "
        "and risks classified as BLOCKER (must resolve first) or FLAG (proceed with awareness).",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 5: User Confirms", S["h3"]))
    story.append(Paragraph(
        'The user confirms the approach or requests deeper investigation. No BLOCKER risks may remain '
        'unresolved before transitioning to work.',
        S["body"]
    ))
    story.append(PageBreak())

    # --- PHASE 3: WORK ---
    story.append(Paragraph("6. Phase 3: Work", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Implement the contribution &#8212; write code, '
        'write tests, validate locally, and prepare a clean changeset.',
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Prerequisite:</b></font> '
        '<font name="Courier" color="#3fb950">.claude/contribute-conventions.md</font> must exist.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Load Context",
         "Read .claude/contribute-conventions.md to restore conventions, branch naming, test/lint commands, and the recommended approach."),
        ("Step 2: Select Operating Mode",
         "Check conventions file for a previously set mode. If not found, ask once (do/guide/adaptive) and persist the choice."),
        ("Step 3: Set Up Local Environment",
         "Each operation requires permission: fork the repo (if not already forked), configure upstream remote, create branch following naming conventions, install dependencies and verify baseline tests pass."),
        ("Step 4: Implement the Change",
         "Read every file listed in the brief before writing. Write a failing test first (TDD). Implement the fix/feature to make the test pass. Format using the project's formatter. Match upstream style exactly. Write minimal, focused changes only."),
        ("Step 5: Validate",
         "Run in sequence: full test suite, linter and formatter (zero new warnings), functional verification reproducing the original scenario. Fix any failure before proceeding."),
        ("Step 6: Present Changeset",
         "Show git diff stat, then full diff. For each changed file: what changed and why, decision points, edge cases, anything that might surprise a reviewer."),
        ("Step 7: Commit",
         "Only after explicit approval. Stage only relevant files (never git add -A). Commit using upstream format. Verify sole authorship (Rule 2). If an AI trailer is detected, present the violation and ask permission to amend."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 4: TEST ---
    story.append(Paragraph("7. Phase 4: Test", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Industrial-grade validation. Acts as a hard gate &#8212; '
        'submit will not proceed without a passing report.',
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#f85149"><b>HARD GATE:</b></font> Submit checks for '
        '<font name="Courier" color="#3fb950">.claude/contribute-test-report.md</font>. '
        'If missing, score &lt; 85%, or any BLOCKER exists, submit refuses.',
        S["body"]
    ))
    story.append(Spacer(1, 8))

    # Stage 1
    story.append(Paragraph("Stage 1: Upstream Test Suite", S["h2"]))
    story.append(Paragraph(
        "Run the project's complete test suite. Establish baseline first by stashing changes and running tests "
        "on the unmodified branch if no baseline exists. Classify failures as:",
        S["body"]
    ))
    fail_table = make_table(
        ["Type", "Description", "Counts Against Score"],
        [
            ["(a) Regression", "Passed before, fails now", "Yes"],
            ["(b) Pre-existing", "Already failing on clean branch", "No"],
            ["(c) Flaky", "Non-deterministic, run 3x to confirm", "No (if confirmed flaky)"],
        ],
        col_widths=[100, 230, 140]
    )
    story.append(fail_table)
    story.append(Spacer(1, 6))

    # Stage 2
    story.append(Paragraph("Stage 2: Static Analysis and Code Quality", S["h2"]))
    story.append(Paragraph(
        "Run every applicable tool based on the project's language:",
        S["body"]
    ))
    sa_table = make_table(
        ["Language", "Tools"],
        [
            ["Python", "flake8/pylint/ruff, mypy/pyright, black --check/isort --check, radon cc, vulture"],
            ["C/C++", "clang-tidy, cppcheck, clang-format --dry-run, -Wall -Wextra -Wpedantic rebuild"],
            ["JS/TS", "eslint, tsc --noEmit, prettier --check"],
        ],
        col_widths=[75, 395]
    )
    story.append(sa_table)
    story.append(Paragraph(
        "CodeRabbit AI Review is also run if configured in the repo (.coderabbit.yaml). "
        "If not configured, marked as SKIP.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Stage 3
    story.append(Paragraph("Stage 3: Security", S["h2"]))
    story.append(Paragraph(
        "<b>All projects:</b> Dependency audit (pip audit / npm audit), secret detection (any finding = BLOCKER), "
        "input validation, injection scan (SQL, command, path traversal, XSS).",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Python specific:</b> Unsafe eval/exec, unsafe yaml.load without SafeLoader, "
        "subprocess.call with shell=True.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>C/C++ specific:</b> Buffer overflows (strcpy, sprintf, gets), memory safety (use-after-free, "
        "double-free, leaks), integer overflow. Suggest AddressSanitizer/MemorySanitizer if supported.",
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#f85149"><b>Any security BLOCKER = automatic overall FAIL regardless of score.</b></font>',
        S["warning"]
    ))
    story.append(Spacer(1, 6))

    # Stage 4
    story.append(Paragraph("Stage 4: Functional Verification", S["h2"]))
    story.append(Paragraph(
        "<b>Clean build:</b> Run the project's clean command if one exists, then rebuild from scratch. "
        "Do NOT delete directories manually if no clean target exists.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Edge cases:</b> Test with null/None, empty strings, empty collections, boundary values "
        "(0, -1, MAX_INT, empty file, single element). Run as ad-hoc scripts, not permanent tests.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Error handling:</b> Error paths produce meaningful messages, don't crash, don't leak resources.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Integration:</b> Imports resolve, APIs match, types are compatible.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    # Stage 5
    story.append(Paragraph("Stage 5: AI Deep Review (Opus)", S["h2"]))
    story.append(Paragraph(
        "An isolated Opus subagent (the <b>deep-reviewer</b> agent) reviews the diff against 6 dimensions: "
        "Correctness, Efficiency, Readability, Maintainability, Completeness, Pushback Risk. "
        "Each finding is rated BLOCKER, WARNING, or SUGGESTION. Any BLOCKER = automatic FAIL.",
        S["body"]
    ))
    story.append(Spacer(1, 8))

    # Scoring
    story.append(Paragraph("Scoring Formula", S["h2"]))
    scoring_table = make_table(
        ["Status", "Points Earned", "Points Possible", "Notes"],
        [
            ["PASS", "1", "1", "Full credit"],
            ["WARN", "0.5", "1", "Half credit"],
            ["FAIL", "0", "1", "No credit"],
            ["SKIP", "0", "0", "Not counted in total"],
        ],
        col_widths=[70, 100, 100, 200]
    )
    story.append(scoring_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '<font name="Courier" color="#58a6ff">Score = (earned / possible) x 100</font>',
        S["code"]
    ))
    story.append(Paragraph(
        '<font color="#3fb950"><b>PASS requires: score &gt;= 85% AND zero BLOCKERs</b></font>',
        S["body"]
    ))
    story.append(Paragraph(
        "FAIL lists all failures and warnings and directs the user to /contribute work.",
        S["body"]
    ))
    story.append(Spacer(1, 8))

    # Test Report Format
    story.append(Paragraph("Test Report Format", S["h3"]))
    report_text = (
        "============================================<br/>"
        "&nbsp;&nbsp;CONTRIBUTION TEST REPORT<br/>"
        "============================================<br/><br/>"
        "Stage 1 - Upstream Tests<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] N/total passed (N regressions)<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] N new tests<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] Coverage: X%<br/><br/>"
        "Stage 2 - Code Quality<br/>"
        "&nbsp;&nbsp;[PASS/FAIL/SKIP] Linter, Type checker, Formatter<br/>"
        "&nbsp;&nbsp;[PASS/FAIL/SKIP] Complexity, Dead code, CodeRabbit<br/><br/>"
        "Stage 3 - Security<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] Dependency audit, Secret detection<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] Input validation, Injection scan<br/><br/>"
        "Stage 4 - Functional<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] Clean build, Edge cases<br/>"
        "&nbsp;&nbsp;[PASS/FAIL] Error handling, Integration<br/><br/>"
        "Stage 5 - AI Deep Review<br/>"
        "&nbsp;&nbsp;[PASS/WARN/FAIL] 6 dimensions<br/><br/>"
        "--------------------------------------------<br/>"
        "&nbsp;&nbsp;Score: X% | Status: PASS/FAIL<br/>"
        "&nbsp;&nbsp;(Threshold: 85% with zero BLOCKERs)<br/>"
        "============================================"
    )
    story.append(Paragraph(
        f'<font name="Courier" size="8" color="#c9d1d9">{report_text}</font>',
        S["code_block"]
    ))
    story.append(PageBreak())

    # --- PHASE 5: SUBMIT ---
    story.append(Paragraph("8. Phase 5: Submit", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Push to fork and open a pull request.',
        S["body"]
    ))
    story.append(Paragraph(
        '<font color="#f85149"><b>Prerequisite:</b></font> Test report must exist with score &gt;= 85% and zero BLOCKERs. '
        "Otherwise submit refuses to proceed.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Pre-flight Checks",
         "Determine upstream default branch. Rebase on latest upstream (with permission). "
         "Resolve conflicts if any, then re-run tests. Verify branch is clean. "
         "Re-confirm test report is not stale (compare timestamps)."),
        ("Step 2: Push to Fork",
         "If branch doesn't exist on remote: normal push with permission. "
         "If branch already exists (re-submission): force-push with --force-with-lease (never --force)."),
        ("Step 3: Draft the Pull Request",
         "Follow upstream PR conventions. Title: concise, under 70 chars, mirrors conventional commit style. "
         "Body: summary, Fixes #NUMBER, changes list, testing summary from test report, notes for reviewers. "
         "Labels and draft flag per contribution guide."),
        ("Step 4: Present Draft to User",
         "Show the complete PR: title, body, source/target branches, labels, draft status."),
        ("Step 5: Open the PR",
         "Only after explicit approval. PR body is written to .claude/contribute-pr-body.md to avoid "
         "shell escaping issues."),
        ("Step 6: Post-submission",
         "Display PR URL. Run one CI status check. If CI fails, analyze and suggest fixes. "
         "If CI passes, inform the user the PR is ready for maintainer review."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 6: REVIEW ---
    story.append(Paragraph("9. Phase 6: Review", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Monitor the PR, respond to maintainer feedback, '
        'iterate until merged or closed.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Resolve PR Identity",
         "Read PR number from conventions file or detect from current branch via gh pr list."),
        ("Step 2: Check PR Status",
         "Fetch CI status, mergeability, review status, open comments. Flag conflicts immediately."),
        ("Step 3: Handle PR State",
         "Changes requested: summarize feedback, recommend responses, transition to work if needed. "
         "Approved: check merge permissions, provide merge command. "
         "Merged: congratulate and offer branch cleanup. "
         "Closed: surface closing reason. "
         "CI failure: classify as related vs pre-existing, suggest fix or draft PR comment."),
        ("Step 4: Respond to Comments",
         "Draft all responses together as a single consolidated comment. Professional, concise, constructive tone. "
         "Never argue with maintainers. Show draft to user before posting."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 7: PR REVIEW ---
    story.append(Paragraph("10. Phase 7: PR Review", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Review someone else\'s PR &#8212; read code, '
        'analyze quality, draft constructive feedback.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Parse URL and Fetch PR Context",
         "Extract owner/repo/PR number. Fetch PR metadata, diff, and CI status. "
         "Store headRefOid for line comments. If PR is merged/closed, analysis proceeds for reference only."),
        ("Step 2: Understand Context",
         "Read the linked issue. Read all existing reviews and comments to avoid duplicate feedback."),
        ("Step 3: Establish Style Conventions",
         "Check contribute-conventions.md, linter/formatter configs, or infer from recent merged PRs."),
        ("Step 4: Code Review Analysis",
         "Review across 5 dimensions: Correctness, Style, Tests, Security, Performance."),
        ("Step 5: Draft Review Comments",
         "Each issue: file, line, severity (BLOCKER/WARNING/SUGGESTION), specific comment. "
         "Overall verdict: Approve, Request changes, or Comment only."),
        ("Step 6: Present to User",
         "Show aggregate counts first, then full draft. Ask for user approval."),
        ("Step 7: Post Review",
         "Post line comments first via GitHub API, then overall verdict. "
         "Never use --force. Report any failed line comments before posting verdict."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 8: RELEASE ---
    story.append(Paragraph("11. Phase 8: Release", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Create GitHub releases with proper tags, changelogs, '
        'and release notes.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Determine Version",
         "Fetch existing tags and releases. Analyze commits since last tag. Recommend semver bump: "
         "patch (bug fixes), minor (new features), major (breaking changes)."),
        ("Step 2: Generate Changelog",
         "Verify clean working tree. Parse commits since last tag. Group by conventional commit types "
         "if applicable. Include PR numbers where present."),
        ("Step 3: Draft Release Notes",
         "Match format of previous releases. Includes: version/date, highlights, breaking changes with "
         "migration notes, and full categorized changelog. Written to .claude/contribute-release-notes.md."),
        ("Step 4: Present Draft to User",
         "Show complete release notes and ask for approval or modifications."),
        ("Step 5: Create Tag",
         "Annotated tag with release message. Confirm target remote if ambiguous."),
        ("Step 6: Push Tag and Create Release",
         "Two separate permission gates: tag push and release creation. Supports --draft flag."),
        ("Step 7: Verify",
         "Confirm release exists via gh release view. Verify tag points to correct commit."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 9: TRIAGE ---
    story.append(Paragraph("12. Phase 9: Triage", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Help triage issues on upstream repos &#8212; '
        'reproduce, categorize, gather context, draft responses.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Parse URL and Read Issue",
         "Fetch full issue metadata: title, body, comments, labels, assignees, state, author, timestamps."),
        ("Step 2: Categorize and Surface",
         "Classify as: Bug, Feature request, Question, Duplicate, or Invalid. State classification explicitly."),
        ("Step 3: Reproduce (Bugs Only)",
         "Determine latest version. Follow reproduction steps exactly. Confirm or deny reproduction "
         "with version and environment details. Trace code path to offending function if possible."),
        ("Step 4: Check for Duplicates",
         "Extract keywords and error strings. Search open and closed issues."),
        ("Step 5: Suggest Labels",
         "Fetch repo's label taxonomy. Suggest 1-3 matching labels. Apply if user has triage permissions."),
        ("Step 6: Draft Response",
         "Tailored to category: Bug (reproduction, workaround, severity), Feature (feasibility, roadmap), "
         "Question (answer or point to docs), Duplicate (link to original), Invalid (polite explanation)."),
        ("Step 7: Present and Post",
         "Show complete triage summary and draft. Post only after explicit user approval."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 10: SYNC ---
    story.append(Paragraph("13. Phase 10: Sync", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Keep fork in sync with upstream, handle divergence '
        'and conflicts.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Verify Fork and Configure Upstream",
         "Confirm this is a fork. Check for upstream remote, detect parent repo if needed. "
         "Fetch upstream and detect default branch."),
        ("Step 2: Detect Divergence",
         "Compare commits ahead/behind using git rev-list --left-right --count."),
        ("Step 3: Check Working Tree",
         "Verify clean working tree. Offer to stash uncommitted changes."),
        ("Step 4: Select Sync Strategy",
         "Default branch: fast-forward reset with explicit warning about lost commits. "
         "Feature branch: offer rebase (linear history) or merge (preserves history). "
         "Warn about force-push requirements for pushed branches."),
        ("Step 5: Execute Sync",
         "Rebase or merge with explicit user approval."),
        ("Step 6: Handle Conflicts",
         "List all conflicted files. Present both sides with context. Help resolve interactively. "
         "For rebase: loop through each replayed commit. For merge: resolve all then commit."),
        ("Step 7: Verify",
         "Run the project's test suite. Diagnose failures from upstream changes vs conflict resolution."),
        ("Step 8: Push",
         "After rebase: --force-with-lease (never --force). After merge: normal push."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- PHASE 11: CLEANUP ---
    story.append(Paragraph("14. Phase 11: Cleanup", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font color="#8b949e"><b>Purpose:</b></font> Cleanly abandon or complete a contribution '
        'workflow &#8212; remove state files, branches, and optionally close PRs.',
        S["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Invocation Modes", S["h3"]))
    inv_table = make_table(
        ["Command", "Behavior"],
        [
            ["/contribute cleanup", "Interactive cleanup with per-item prompts"],
            ["/contribute cleanup --dry-run", "Show what would be removed, touch nothing"],
            ["/contribute cleanup --full", "Remove everything with one upfront confirmation"],
        ],
        col_widths=[200, 270]
    )
    story.append(inv_table)
    story.append(Spacer(1, 6))

    for step_title, step_body in [
        ("Step 1: Audit Current State",
         "Read everything before touching anything: state files, current/contribution branches, "
         "remote branches, open PRs, sync stashes. Present full inventory."),
        ("Step 2: Determine Cleanup Scope",
         "--full: one confirmation for everything. Otherwise: per-category questions."),
        ("Step 3: Handle Open PRs",
         "Surface engagement (reviews, comments, approvals). Options: Close (with comment), "
         "Draft (convert to draft), Leave open. Two permission gates for close."),
        ("Step 4: Remove Remote Branches",
         "Warn about open PRs. Treat 'remote ref not found' as success (auto-deleted after merge)."),
        ("Step 5: Remove Local Branches",
         "Switch to default branch first if current. Warn about unmerged commits. "
         "Use -d first, -D only after explicit warning and approval."),
        ("Step 6: Clear State Files",
         "Ask about each file individually. Remove .claude/ directory if empty."),
        ("Step 7: Clear Sync Stashes",
         "Only target sync-stash-* stashes. Show contents. Drop from highest to lowest index."),
        ("Step 8: Verification",
         "Run final audit to confirm clean state. Present summary."),
    ]:
        story.append(Paragraph(step_title, S["h3"]))
        story.append(Paragraph(step_body, S["body"]))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Edge Cases", S["h3"]))
    edge_cases = [
        "Merged PR with branch auto-deleted by GitHub: treat as success",
        "No .claude/ directory: skip state file steps gracefully",
        "Detached HEAD: inform user, skip branch deletion",
        "Multiple contributions in same repo: warn about shared state files",
        "Upstream fork relationship broken: skip remote operations",
        "Non-standard branch names: include branches from conventions file",
    ]
    for ec in edge_cases:
        story.append(Paragraph(f"&#8226; {ec}", S["bullet"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 15. AGENTS
    # ═══════════════════════════════════════
    story.append(Paragraph("15. Agents", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Two dedicated agents handle isolated, parallelizable work. Both run on Claude Opus (Rule 5).",
        S["body"]
    ))
    story.append(Spacer(1, 8))

    # issue-scout
    story.append(Paragraph("issue-scout", S["h2"]))
    scout_table = make_table(
        ["Property", "Value"],
        [
            ["Model", "opus"],
            ["Color", "cyan"],
            ["Tools", "Bash, Read, Grep, Glob"],
            ["Invoked by", "Discover phase (Step 2)"],
            ["Input", "Domain selection + search parameters"],
            ["Output", "Scored shortlist of 3-5 issues with Rule 6 verification"],
        ],
        col_widths=[100, 370]
    )
    story.append(scout_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Search Process:</b> Execute parallel GitHub searches by label (good first issue, help wanted). "
        "Filter by activity (90 days), stars (50+), CONTRIBUTING.md presence. "
        "Apply all 4 Rule 6 checks. Score 5 quality signals. Estimate complexity.",
        S["body"]
    ))
    story.append(Paragraph(
        "<b>Quality Signals (1 point each, max 5):</b>",
        S["body"]
    ))
    for sig in [
        "CONTRIBUTING.md exists",
        "CI configured (.github/workflows/)",
        "Clear acceptance criteria in issue body",
        "Maintainer has commented on the issue",
        "Repo has had a release in the last 6 months",
    ]:
        story.append(Paragraph(f"&#8226; {sig}", S["bullet"]))
    story.append(Spacer(1, 10))

    # deep-reviewer
    story.append(Paragraph("deep-reviewer", S["h2"]))
    reviewer_table = make_table(
        ["Property", "Value"],
        [
            ["Model", "opus"],
            ["Color", "yellow"],
            ["Tools", "Read, Grep, Glob (read-only)"],
            ["Invoked by", "Test phase (Stage 5)"],
            ["Input", "Full diff + issue description + contribution brief"],
            ["Output", "Structured severity ratings per 6 dimensions, findings table, verdict"],
        ],
        col_widths=[100, 370]
    )
    story.append(reviewer_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Review Dimensions:</b>",
        S["body"]
    ))
    dims_table = make_table(
        ["Dimension", "What It Checks"],
        [
            ["Correctness", "Does it solve the issue? Edge cases? Error conditions? Off-by-one errors?"],
            ["Efficiency", "Algorithm appropriateness? Unnecessary complexity? Blocking calls in async?"],
            ["Readability", "Understandable in 6 months? Clear names? Straightforward control flow?"],
            ["Maintainability", "Follows existing patterns? Easy to extend? Tight coupling?"],
            ["Completeness", "Tests adequate? Docs updated? Error messages helpful?"],
            ["Pushback Risk", "What would a strict maintainer object to?"],
        ],
        col_widths=[105, 365]
    )
    story.append(dims_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Severity Levels:</b> BLOCKER (must fix, auto-fail), WARNING (0.5 pts, should fix), "
        "SUGGESTION (no score impact, take it or leave it).",
        S["body"]
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 16. STATE FILES
    # ═══════════════════════════════════════
    story.append(Paragraph("16. State Files", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "All contribution state persists in <font name='Courier' color='#3fb950'>.claude/</font> "
        "in the working directory across sessions:",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    state_table = make_table(
        ["File", "Written By", "Read By", "Contents"],
        [
            ["contribute-conventions.md", "analyze", "work, test, submit, review, pr-review, sync, cleanup",
             "Repo, issue, branch, mode, conventions, approach"],
            ["contribute-test-report.md", "test", "submit",
             "Scored test report with pass/fail per check"],
            ["contribute-discover.md", "discover", "analyze (optional)",
             "Search criteria and issue shortlist"],
            ["contribute-release-notes.md", "release", "release",
             "Draft release notes for --notes-file"],
            ["contribute-pr-body.md", "submit", "submit",
             "PR body content for --body-file"],
        ],
        col_widths=[135, 60, 130, 145]
    )
    story.append(state_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 17. PLUGIN ARCHITECTURE
    # ═══════════════════════════════════════
    story.append(Paragraph("17. Plugin Architecture", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))

    arch_text = (
        "contribute/<br/>"
        "&#9500;&#9472;&#9472; .claude-plugin/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; plugin.json&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Plugin manifest<br/>"
        "&#9500;&#9472;&#9472; agents/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9500;&#9472;&#9472; deep-reviewer.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AI deep review (test Stage 5)<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; issue-scout.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Parallel issue discovery<br/>"
        "&#9500;&#9472;&#9472; commands/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; contribute.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# /contribute command + routing<br/>"
        "&#9500;&#9472;&#9472; skills/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; contribute/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9500;&#9472;&#9472; SKILL.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Core rules + phase routing<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; references/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 11 phase reference files<br/>"
        "&#9500;&#9472;&#9472; docs/<br/>"
        "&#9474;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&#9472; index.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# GitHub Pages documentation<br/>"
        "&#9500;&#9472;&#9472; banner.png<br/>"
        "&#9500;&#9472;&#9472; README.md<br/>"
        "&#9500;&#9472;&#9472; LICENSE<br/>"
        "&#9492;&#9472;&#9472; .gitignore"
    )
    story.append(Paragraph(
        f'<font name="Courier" size="9" color="#c9d1d9">{arch_text}</font>',
        S["code_block"]
    ))
    story.append(Spacer(1, 10))

    comp_table = make_table(
        ["Component", "Purpose"],
        [
            ["Skill (SKILL.md)", "Core rules, phase routing table, state file schema. Progressive disclosure &#8212; phase details load on demand from references/."],
            ["Command (contribute.md)", "Entry point for /contribute. Owns argument parsing, phase routing, and auto-detection logic."],
            ["deep-reviewer agent", "Isolated Opus agent for test Stage 5. Gets diff + issue + brief. Returns structured severity ratings."],
            ["issue-scout agent", "Isolated Opus agent for discover phase. Runs parallel gh search queries, applies Rule 6, scores quality signals."],
        ],
        col_widths=[140, 330]
    )
    story.append(comp_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Auto-Detection Logic", S["h3"]))
    story.append(Paragraph(
        "When <font name='Courier' color='#3fb950'>/contribute</font> is invoked without arguments:",
        S["body"]
    ))
    for i, rule in enumerate([
        "If the current directory is a fork with uncommitted changes: suggest test or submit",
        "If the current directory is a fork with a feature branch and committed changes: suggest test",
        "If the current directory is a fork with no changes: suggest work",
        "If the user recently ran analyze: suggest work",
        "Otherwise: ask which phase the user wants",
    ], 1):
        story.append(Paragraph(f"<b>{i}.</b> {rule}", S["bullet"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 18. CROSS-TOOL COMPATIBILITY
    # ═══════════════════════════════════════
    story.append(Paragraph("18. Cross-Tool Compatibility", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Built for Claude Code, but the skill content is pure markdown. Other AI coding tools can use it too.",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    compat_table = make_table(
        ["Feature", "Claude Code", "Cursor / Antigravity / Others"],
        [
            ["Phase instructions", "Via /contribute command", "Read SKILL.md + references directly"],
            ["Core rules", "Enforced by skill", "Enforced by skill"],
            ["State files", ".claude/ directory", ".claude/ directory"],
            ["GitHub CLI commands", "Works", "Works"],
            ["deep-reviewer agent", "Isolated subagent", "Inline review"],
            ["issue-scout agent", "Isolated subagent", "Inline search"],
            ["Auto-detection", "Built into command", "Manual phase selection"],
        ],
        col_widths=[120, 170, 180]
    )
    story.append(compat_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 19. TEST APPLICABILITY MATRIX
    # ═══════════════════════════════════════
    story.append(Paragraph("19. Test Applicability Matrix", S["h1"]))
    story.append(AccentLine(W, ACCENT_BLUE, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Not every check applies to every project. This matrix determines which checks run:",
        S["body"]
    ))
    story.append(Spacer(1, 6))

    matrix_table = make_table(
        ["Check", "Python", "C/C++", "JS/TS"],
        [
            ["Upstream test suite", "Yes", "Yes", "Yes"],
            ["Linting", "Yes", "Yes", "Yes"],
            ["Type checking", "Yes", "Yes", "Yes"],
            ["Formatting", "Yes", "Yes", "Yes"],
            ["Complexity analysis", "Yes", "Yes", "No"],
            ["Dead code", "Yes", "No", "Yes"],
            ["CodeRabbit review", "Yes", "Yes", "Yes"],
            ["Dependency audit", "Yes", "If pkg mgr", "Yes"],
            ["Secret detection", "Yes", "Yes", "Yes"],
            ["Input validation", "Yes", "Yes", "Yes"],
            ["Injection scan", "Yes", "Yes", "Yes"],
            ["Buffer overflow", "No", "Yes", "No"],
            ["Memory safety", "No", "Yes", "No"],
            ["Integer overflow", "No", "Yes", "No"],
            ["Unsafe operations", "Yes", "Yes", "Yes"],
            ["Clean build", "Yes", "Yes", "Yes"],
            ["Edge cases", "Yes", "Yes", "Yes"],
            ["Error handling", "Yes", "Yes", "Yes"],
            ["Integration", "Yes", "Yes", "Yes"],
            ["AI Deep Review", "Yes", "Yes", "Yes"],
        ],
        col_widths=[140, 90, 90, 90]
    )
    story.append(matrix_table)
    story.append(Spacer(1, 20))

    # Final footer
    story.append(AccentLine(W, ACCENT_PURPLE, 2))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        '<font color="#8b949e">Generated for /contribute v1.0.0 | '
        'github.com/LuciferDono/contribute | MIT License</font>',
        ParagraphStyle("FinalFooter", fontName="Helvetica", fontSize=9,
                       textColor=TEXT_MUTED, alignment=TA_CENTER, leading=14)
    ))

    # ═══════════════════════════════════════
    # BUILD THE PDF
    # ═══════════════════════════════════════
    output_path = os.path.join(os.path.dirname(__file__), "contribute-documentation.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=40,
        title="/contribute - Complete Documentation",
        author="LuciferDono",
        subject="Open-Source Contribution Plugin Documentation",
    )
    doc.build(story, onFirstPage=title_page_bg, onLaterPages=page_bg)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
