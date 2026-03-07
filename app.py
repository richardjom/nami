import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health Bill Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Bill data
# ---------------------------------------------------------------------------
BILLS = [
    {
        "id": "HR-4321",
        "title": "Mental Health Parity Enforcement Act",
        "status": "In Committee",
        "status_step": 2,
        "chamber": "House",
        "introduced": "Jan 15, 2026",
        "sponsors": 24,
        "lead_sponsor": "Rep. Sarah Mitchell (D-CA)",
        "summary": "Strengthens enforcement of the Mental Health Parity and Addiction Equity Act by requiring insurers to submit annual compliance reports and increasing penalties for violations.",
        "impact": "Would affect an estimated 150 million Americans with employer-sponsored insurance by ensuring equal coverage for mental health and substance use disorder treatments.",
        "provisions": [
            "Annual insurer compliance audits",
            "Tripled penalties for parity violations",
            "Patient complaint hotline establishment",
            "Transparency reports made public",
        ],
        "tags": ["Insurance", "Parity", "Enforcement"],
        "urgency": "high",
    },
    {
        "id": "S-2187",
        "title": "988 Lifeline Expansion & Sustainability Act",
        "status": "Passed Senate",
        "status_step": 4,
        "chamber": "Senate",
        "introduced": "Nov 3, 2025",
        "sponsors": 38,
        "lead_sponsor": "Sen. David Chen (D-WA)",
        "summary": "Provides permanent federal funding for the 988 Suicide and Crisis Lifeline, expands text and chat capabilities, and mandates response time standards.",
        "impact": "Would ensure 24/7 crisis support for all Americans, with targeted investments in underserved rural and tribal communities.",
        "provisions": [
            "Permanent annual funding of $1.2B",
            "90-second answer time mandate",
            "Rural crisis center grants",
            "Specialized veteran and youth lines",
        ],
        "tags": ["Crisis", "Funding", "988"],
        "urgency": "medium",
    },
    {
        "id": "HR-7890",
        "title": "Youth Mental Health & Schools Act",
        "status": "Introduced",
        "status_step": 1,
        "chamber": "House",
        "introduced": "Feb 28, 2026",
        "sponsors": 12,
        "lead_sponsor": "Rep. Maria Torres (D-TX)",
        "summary": "Establishes a federal grant program to place licensed mental health professionals in K-12 schools and fund evidence-based prevention programs.",
        "impact": "Targets the youth mental health crisis by aiming for a 1:250 counselor-to-student ratio in every public school district.",
        "provisions": [
            "Federal school counselor grants",
            "Trauma-informed training for educators",
            "Student mental health screening opt-in",
            "After-school wellness programs",
        ],
        "tags": ["Youth", "Schools", "Prevention"],
        "urgency": "medium",
    },
    {
        "id": "S-5544",
        "title": "Community Mental Health Infrastructure Act",
        "status": "Floor Vote Scheduled",
        "status_step": 3,
        "chamber": "Senate",
        "introduced": "Sep 12, 2025",
        "sponsors": 31,
        "lead_sponsor": "Sen. James Wright (R-OH)",
        "summary": "Authorizes $3 billion over 5 years to build and renovate community mental health centers, with priority given to mental health professional shortage areas.",
        "impact": "Would create over 500 new community mental health centers in underserved areas, reducing average travel time to care by 40%.",
        "provisions": [
            "$3B over 5 years for new centers",
            "Workforce loan forgiveness program",
            "Telehealth infrastructure grants",
            "Bipartisan oversight commission",
        ],
        "tags": ["Infrastructure", "Community", "Funding"],
        "urgency": "high",
    },
    {
        "id": "HR-3210",
        "title": "Maternal Mental Health Access Act",
        "status": "In Committee",
        "status_step": 2,
        "chamber": "House",
        "introduced": "Dec 5, 2025",
        "sponsors": 19,
        "lead_sponsor": "Rep. Angela Brooks (D-GA)",
        "summary": "Extends Medicaid postpartum coverage for mental health services to 12 months and creates a national maternal mental health hotline.",
        "impact": "Would provide critical support to the estimated 1 in 5 new mothers who experience perinatal mood disorders.",
        "provisions": [
            "12-month postpartum Medicaid extension",
            "National maternal mental health hotline",
            "Provider screening mandate",
            "Peer support specialist funding",
        ],
        "tags": ["Maternal", "Medicaid", "Postpartum"],
        "urgency": "medium",
    },
    {
        "id": "S-8877",
        "title": "Veterans Mental Health Modernization Act",
        "status": "Signed Into Law",
        "status_step": 5,
        "chamber": "Senate",
        "introduced": "Jun 20, 2025",
        "sponsors": 67,
        "lead_sponsor": "Sen. Robert Hayes (R-TX)",
        "summary": "Modernizes VA mental health services by expanding telehealth, integrating AI-assisted screening tools, and removing barriers to community care referrals.",
        "impact": "Directly benefits 9.1 million veterans enrolled in VA healthcare, with emphasis on reducing the 17 veteran suicides per day.",
        "provisions": [
            "VA telehealth expansion to all facilities",
            "AI-assisted PTSD screening pilot",
            "Streamlined community care referrals",
            "Peer specialist hiring initiative",
        ],
        "tags": ["Veterans", "VA", "Telehealth"],
        "urgency": "low",
    },
]

STATUS_STEPS = ["Introduced", "In Committee", "Floor Vote", "Passed Chamber", "Signed Into Law"]

URGENCY_MAP = {
    "high": {"label": "High Priority", "color": "#EF4444", "bg": "#FEE2E2", "text": "#991B1B"},
    "medium": {"label": "Medium Priority", "color": "#F59E0B", "bg": "#FEF3C7", "text": "#92400E"},
    "low": {"label": "Low Priority", "color": "#10B981", "bg": "#D1FAE5", "text": "#065F46"},
}

TAG_COLORS = [
    ("#EDE9FE", "#5B21B6"),
    ("#E0F2FE", "#075985"),
    ("#FCE7F3", "#9D174D"),
    ("#ECFDF5", "#065F46"),
    ("#FFF7ED", "#9A3412"),
]

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700;9..144,900&family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* Global overrides */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FAFAF8 !important;
    font-family: 'DM Sans', sans-serif;
}
header[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding-top: 0 !important; max-width: 1100px; }
div[data-testid="stVerticalBlock"] > div { gap: 0; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 40%, #40916C 100%);
    padding: 52px 48px 44px;
    border-radius: 0 0 24px 24px;
    position: relative;
    overflow: hidden;
    margin-bottom: 28px;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -40px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(183,228,199,0.08);
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -90px; left: 8%;
    width: 380px; height: 380px;
    border-radius: 50%;
    background: rgba(183,228,199,0.05);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 10px;
    margin-bottom: 14px;
}
.hero-badge span {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px; font-weight: 600;
    color: #B7E4C7;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 44px; font-weight: 900;
    color: #FFFFFF; line-height: 1.08;
    margin: 0 0 12px; max-width: 560px;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px; color: #B7E4C7;
    line-height: 1.6; max-width: 480px; margin: 0;
}

/* Stat cards row */
.stats-row {
    display: flex; gap: 16px;
    margin-top: 32px; flex-wrap: wrap;
    position: relative; z-index: 1;
}
.stat-card {
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 22px;
    min-width: 135px;
}
.stat-card .icon { font-size: 15px; margin-bottom: 4px; }
.stat-card .value {
    font-family: 'Fraunces', serif;
    font-size: 30px; font-weight: 900;
    color: #FFFFFF;
}
.stat-card .label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10.5px; color: #B7E4C7;
    letter-spacing: 0.07em;
    text-transform: uppercase; font-weight: 500;
}

/* Filter pills */
.filter-row {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin-bottom: 20px; align-items: center;
}
.filter-pill {
    font-family: 'DM Sans', sans-serif;
    font-size: 12.5px; font-weight: 600;
    padding: 8px 18px;
    border-radius: 9px;
    cursor: pointer; border: 1.5px solid #E5E7EB;
    background: #FFFFFF; color: #4B5563;
    transition: all 0.2s;
}
.filter-pill:hover { border-color: #2D6A4F; color: #2D6A4F; }
.filter-pill.active {
    background: #2D6A4F; color: #FFFFFF;
    border-color: #2D6A4F;
}

/* Bill card */
.bill-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 28px 28px 24px;
    margin-bottom: 16px;
    border-left: 4px solid;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04), 0 0 0 1px rgba(0,0,0,0.02);
    transition: box-shadow 0.3s, transform 0.2s;
}
.bill-card:hover {
    box-shadow: 0 8px 30px rgba(0,0,0,0.07);
    transform: translateY(-1px);
}
.bill-card.urgency-high   { border-left-color: #EF4444; }
.bill-card.urgency-medium { border-left-color: #F59E0B; }
.bill-card.urgency-low    { border-left-color: #10B981; }

/* Bill header row */
.bill-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
.bill-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.bill-id {
    font-family: 'DM Mono', monospace;
    font-size: 11px; font-weight: 500;
    color: #6B7280; background: #F3F4F6;
    padding: 3px 9px; border-radius: 5px;
    letter-spacing: 0.04em;
}
.chamber-badge {
    font-size: 11px; font-weight: 600;
    padding: 3px 11px; border-radius: 20px;
    letter-spacing: 0.03em;
}
.chamber-house { color: #1E40AF; background: #DBEAFE; }
.chamber-senate { color: #7C3AED; background: #EDE9FE; }
.urgency-badge {
    font-size: 11px; font-weight: 600;
    padding: 3px 11px; border-radius: 20px;
    display: inline-flex; align-items: center; gap: 6px;
}
.urgency-dot {
    width: 6px; height: 6px;
    border-radius: 50%; display: inline-block;
}
.bill-title {
    font-family: 'Fraunces', serif;
    font-size: 20px; font-weight: 700;
    color: #111827; line-height: 1.3;
    margin: 0;
}
.bill-summary {
    font-size: 14px; color: #4B5563;
    line-height: 1.65; margin: 0 0 16px;
}

/* Tags */
.tag-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 14px; }
.tag {
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 6px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
}

/* Progress track */
.progress-track {
    display: flex; align-items: flex-start;
    width: 100%; margin-top: 4px;
}
.progress-step {
    display: flex; flex-direction: column;
    align-items: center; flex: 1;
    position: relative;
}
.progress-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #D1D5DB;
    position: relative; z-index: 2;
    transition: all 0.3s;
}
.progress-dot.completed { background: #2D6A4F; }
.progress-dot.current {
    width: 18px; height: 18px;
    background: #2D6A4F;
    box-shadow: 0 0 0 4px #B7E4C7, 0 0 14px rgba(45,106,79,0.35);
}
.progress-label {
    font-size: 9px; color: #9CA3AF;
    margin-top: 7px; text-align: center;
    width: 72px; letter-spacing: 0.02em;
}
.progress-label.active { color: #2D6A4F; font-weight: 700; }
.progress-line {
    position: absolute;
    top: 6px; left: 50%; right: -50%;
    height: 2px; background: #E5E7EB; z-index: 1;
}
.progress-line.filled { background: #2D6A4F; }

/* Expanded details */
.impact-box {
    background: #F0FDF4;
    border-left: 4px solid #2D6A4F;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}
.impact-box h4 {
    font-family: 'Fraunces', serif;
    font-size: 12px; font-weight: 700;
    color: #2D6A4F; margin: 0 0 8px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.impact-box p {
    font-size: 14px; color: #1F2937;
    line-height: 1.65; margin: 0;
}
.provision-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px; margin-bottom: 20px;
}
.provision-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 12px; background: #F9FAFB;
    border-radius: 8px;
}
.provision-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: #2D6A4F; color: #FFF;
    font-size: 10px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-family: 'DM Mono', monospace;
}
.provision-text {
    font-size: 13px; color: #374151; line-height: 1.5;
}
.meta-row {
    display: flex; gap: 28px;
    padding-top: 16px;
    border-top: 1px solid #F3F4F6;
    flex-wrap: wrap; align-items: flex-end;
}
.meta-item .lbl {
    font-size: 10.5px; color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.meta-item .val {
    font-size: 13px; color: #1F2937;
    font-weight: 600; margin-top: 3px;
}
.action-btn {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px; font-weight: 700;
    color: #FFF; background: #2D6A4F;
    border: none; border-radius: 10px;
    padding: 12px 28px;
    cursor: pointer; letter-spacing: 0.03em;
    text-decoration: none;
    box-shadow: 0 2px 8px rgba(45,106,79,0.3);
    transition: all 0.2s;
    margin-left: auto;
}
.action-btn:hover { background: #1B4332; transform: translateY(-1px); }

/* Section label */
.section-label {
    font-family: 'Fraunces', serif;
    font-size: 12px; font-weight: 700;
    color: #374151; margin: 0 0 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Footer CTA */
.footer-cta {
    background: #1B4332;
    border-radius: 16px;
    padding: 36px;
    text-align: center;
    margin-top: 28px;
    position: relative;
    overflow: hidden;
}
.footer-cta::before {
    content: '';
    position: absolute;
    top: -30px; right: 10%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(183,228,199,0.06);
}
.footer-cta h3 {
    font-family: 'Fraunces', serif;
    font-size: 24px; font-weight: 900;
    color: #FFF; margin: 0 0 8px;
    position: relative;
}
.footer-cta p {
    font-size: 14px; color: #B7E4C7;
    margin: 0 0 20px; position: relative;
}
.footer-btn {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px; font-weight: 700;
    color: #1B4332; background: #B7E4C7;
    border: none; border-radius: 10px;
    padding: 14px 34px;
    cursor: pointer; letter-spacing: 0.03em;
    text-decoration: none;
    position: relative;
    transition: all 0.2s;
}
.footer-btn:hover { background: #FFF; }

/* Hide default streamlit elements */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stExpander"] { border: none !important; }
div[data-testid="stExpander"] summary { display: block !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Helper: render progress track HTML
# ---------------------------------------------------------------------------
def progress_html(current_step: int) -> str:
    dots = []
    for i, label in enumerate(STATUS_STEPS):
        step_num = i + 1
        completed = step_num < current_step
        is_current = step_num == current_step
        dot_cls = "completed" if completed else ("current" if is_current else "")
        lbl_cls = "active" if completed or is_current else ""
        line_html = ""
        if i < len(STATUS_STEPS) - 1:
            line_cls = "filled" if completed else ""
            line_html = f'<div class="progress-line {line_cls}"></div>'
        dots.append(
            f'<div class="progress-step">{line_html}'
            f'<div class="progress-dot {dot_cls}"></div>'
            f'<div class="progress-label {lbl_cls}">{label}</div>'
            "</div>"
        )
    return f'<div class="progress-track">{"".join(dots)}</div>'


# ---------------------------------------------------------------------------
# Helper: render tag pills
# ---------------------------------------------------------------------------
def tags_html(tags: list) -> str:
    out = ""
    for i, t in enumerate(tags):
        bg, fg = TAG_COLORS[i % len(TAG_COLORS)]
        out += f'<span class="tag" style="background:{bg};color:{fg}">{t}</span>'
    return f'<div class="tag-row">{out}</div>'


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
total = len(BILLS)
active = sum(1 for b in BILLS if b["status_step"] < 5)
passed = sum(1 for b in BILLS if b["status_step"] >= 4)
high_p = sum(1 for b in BILLS if b["urgency"] == "high")

st.markdown(
    f"""
<div class="hero-banner">
    <div class="hero-badge">
        <span>🧠</span>
        <span>Legislative Tracker</span>
    </div>
    <h1 class="hero-title">Mental Health<br>Bill Tracker</h1>
    <p class="hero-sub">Follow the legislation that shapes mental health care in America. Know what's happening. Make your voice heard.</p>
    <div class="stats-row">
        <div class="stat-card">
            <div class="icon">📋</div>
            <div class="value">{total}</div>
            <div class="label">Bills Tracked</div>
        </div>
        <div class="stat-card">
            <div class="icon">⚡</div>
            <div class="value">{active}</div>
            <div class="label">Currently Active</div>
        </div>
        <div class="stat-card">
            <div class="icon">✅</div>
            <div class="value">{passed}</div>
            <div class="label">Passed / Signed</div>
        </div>
        <div class="stat-card">
            <div class="icon">🔴</div>
            <div class="value">{high_p}</div>
            <div class="label">High Priority</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Filters + search
# ---------------------------------------------------------------------------
FILTER_OPTIONS = ["All", "House", "Senate", "High Urgency", "Signed Into Law"]

col_filters, col_search = st.columns([3, 1])
with col_filters:
    active_filter = st.radio(
        "Filter",
        FILTER_OPTIONS,
        horizontal=True,
        label_visibility="collapsed",
    )
with col_search:
    search = st.text_input("Search", placeholder="Search bills...", label_visibility="collapsed")

# ---------------------------------------------------------------------------
# Filter logic
# ---------------------------------------------------------------------------
filtered = BILLS
if active_filter == "House":
    filtered = [b for b in filtered if b["chamber"] == "House"]
elif active_filter == "Senate":
    filtered = [b for b in filtered if b["chamber"] == "Senate"]
elif active_filter == "High Urgency":
    filtered = [b for b in filtered if b["urgency"] == "high"]
elif active_filter == "Signed Into Law":
    filtered = [b for b in filtered if b["status_step"] == 5]

if search:
    q = search.lower()
    filtered = [
        b
        for b in filtered
        if q in b["title"].lower()
        or q in b["id"].lower()
        or any(q in t.lower() for t in b["tags"])
    ]

# ---------------------------------------------------------------------------
# Bill cards
# ---------------------------------------------------------------------------
if not filtered:
    st.markdown(
        """
    <div style="text-align:center;padding:60px 20px;color:#9CA3AF">
        <div style="font-size:40px;margin-bottom:12px">🔍</div>
        <p style="font-size:16px;font-weight:600;color:#6B7280">No bills match your filters</p>
        <p style="font-size:13px">Try adjusting your search or filter criteria</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

for bill in filtered:
    u = URGENCY_MAP[bill["urgency"]]
    chamber_cls = "chamber-house" if bill["chamber"] == "House" else "chamber-senate"

    # Card header + summary + progress (always visible)
    card_html = f"""
    <div class="bill-card urgency-{bill['urgency']}">
        <div class="bill-meta">
            <span class="bill-id">{bill['id']}</span>
            <span class="chamber-badge {chamber_cls}">{bill['chamber']}</span>
            <span class="urgency-badge" style="background:{u['bg']};color:{u['text']}">
                <span class="urgency-dot" style="background:{u['color']}"></span>
                {u['label']}
            </span>
        </div>
        <h3 class="bill-title">{bill['title']}</h3>
        {tags_html(bill['tags'])}
        <p class="bill-summary">{bill['summary']}</p>
        {progress_html(bill['status_step'])}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Expandable details
    with st.expander(f"Details: {bill['title']}", expanded=False):
        # Impact box
        st.markdown(
            f"""
        <div class="impact-box">
            <h4>Why This Matters</h4>
            <p>{bill['impact']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Provisions
        prov_items = ""
        for idx, prov in enumerate(bill["provisions"], 1):
            prov_items += f"""
            <div class="provision-item">
                <div class="provision-num">{idx}</div>
                <div class="provision-text">{prov}</div>
            </div>"""
        st.markdown(
            f"""
        <div class="section-label">Key Provisions</div>
        <div class="provision-grid">{prov_items}</div>
        """,
            unsafe_allow_html=True,
        )

        # Meta row
        st.markdown(
            f"""
        <div class="meta-row">
            <div class="meta-item">
                <div class="lbl">Lead Sponsor</div>
                <div class="val">{bill['lead_sponsor']}</div>
            </div>
            <div class="meta-item">
                <div class="lbl">Co-sponsors</div>
                <div class="val">{bill['sponsors']}</div>
            </div>
            <div class="meta-item">
                <div class="lbl">Introduced</div>
                <div class="val">{bill['introduced']}</div>
            </div>
            <a class="action-btn" href="#">Take Action →</a>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Footer CTA
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="footer-cta">
    <h3>Your voice matters.</h3>
    <p>Contact your representatives and advocate for mental health legislation.</p>
    <a class="footer-btn" href="#">Find Your Representative →</a>
</div>
""",
    unsafe_allow_html=True,
)
