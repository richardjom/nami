import re
from html import escape

import streamlit as st

st.set_page_config(
    page_title="988 State Policy Tracker",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STATE_POLICIES = [
    {
        "state": "California",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.08",
        "annual_revenue": "$30M est.",
        "trust_fund": True,
        "mobile_crisis": "Partial",
        "stabilization": "Dedicated grants",
        "youth_services": "In progress",
        "latest_bill": "AB 988",
        "year": 2024,
    },
    {
        "state": "Colorado",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.35",
        "annual_revenue": "$26M est.",
        "trust_fund": True,
        "mobile_crisis": "Statewide",
        "stabilization": "State + Medicaid",
        "youth_services": "Yes",
        "latest_bill": "SB24-001",
        "year": 2024,
    },
    {
        "state": "Illinois",
        "funding_model": "Recurring appropriation",
        "monthly_fee": "$0.00",
        "annual_revenue": "General fund",
        "trust_fund": False,
        "mobile_crisis": "Partial",
        "stabilization": "Medicaid only",
        "youth_services": "In progress",
        "latest_bill": "HB 2450",
        "year": 2025,
    },
    {
        "state": "Minnesota",
        "funding_model": "Recurring appropriation",
        "monthly_fee": "$0.00",
        "annual_revenue": "$20M est.",
        "trust_fund": False,
        "mobile_crisis": "Statewide",
        "stabilization": "Dedicated grants",
        "youth_services": "Yes",
        "latest_bill": "SF 2995",
        "year": 2024,
    },
    {
        "state": "Nevada",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.35",
        "annual_revenue": "$12M est.",
        "trust_fund": True,
        "mobile_crisis": "Partial",
        "stabilization": "State grants",
        "youth_services": "In progress",
        "latest_bill": "SB 390",
        "year": 2023,
    },
    {
        "state": "New York",
        "funding_model": "Recurring appropriation",
        "monthly_fee": "$0.00",
        "annual_revenue": "$35M est.",
        "trust_fund": False,
        "mobile_crisis": "Partial",
        "stabilization": "State + Medicaid",
        "youth_services": "Yes",
        "latest_bill": "S9124",
        "year": 2025,
    },
    {
        "state": "Ohio",
        "funding_model": "Recurring appropriation",
        "monthly_fee": "$0.00",
        "annual_revenue": "$40M est.",
        "trust_fund": False,
        "mobile_crisis": "Statewide",
        "stabilization": "Dedicated grants",
        "youth_services": "In progress",
        "latest_bill": "HB 33",
        "year": 2023,
    },
    {
        "state": "Oregon",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.40",
        "annual_revenue": "$14M est.",
        "trust_fund": True,
        "mobile_crisis": "Statewide",
        "stabilization": "State + Medicaid",
        "youth_services": "Yes",
        "latest_bill": "SB 955",
        "year": 2023,
    },
    {
        "state": "Texas",
        "funding_model": "No dedicated funding",
        "monthly_fee": "$0.00",
        "annual_revenue": "One-time grants",
        "trust_fund": False,
        "mobile_crisis": "Partial",
        "stabilization": "Limited",
        "youth_services": "No",
        "latest_bill": "HB 13",
        "year": 2025,
    },
    {
        "state": "Virginia",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.12",
        "annual_revenue": "$8M est.",
        "trust_fund": True,
        "mobile_crisis": "Statewide",
        "stabilization": "State grants",
        "youth_services": "In progress",
        "latest_bill": "SB 429",
        "year": 2024,
    },
    {
        "state": "Washington",
        "funding_model": "Fee enacted",
        "monthly_fee": "$0.40",
        "annual_revenue": "$38M est.",
        "trust_fund": True,
        "mobile_crisis": "Statewide",
        "stabilization": "State + Medicaid",
        "youth_services": "Yes",
        "latest_bill": "HB 1134",
        "year": 2024,
    },
    {
        "state": "Wisconsin",
        "funding_model": "No dedicated funding",
        "monthly_fee": "$0.00",
        "annual_revenue": "Federal grants",
        "trust_fund": False,
        "mobile_crisis": "Pilot",
        "stabilization": "Limited",
        "youth_services": "No",
        "latest_bill": "AB 128",
        "year": 2025,
    },
]

PLAYBOOK = [
    {
        "title": "Sustainable 988 Funding",
        "why": "Without recurring dollars, call centers and crisis teams cannot keep staffing levels stable.",
        "model": "Create a dedicated 988 fee or protected recurring appropriation in state statute.",
        "states": ["Colorado", "Oregon", "Washington", "Virginia"],
        "action": "Ask for protected funding tied to annual transparency and outcomes reporting.",
    },
    {
        "title": "Mobile Crisis Teams",
        "why": "Mobile response gives people in crisis community-based care and reduces law enforcement involvement.",
        "model": "Require statewide 24/7 mobile crisis coverage with Medicaid and non-Medicaid funding paths.",
        "states": ["Minnesota", "Ohio", "Washington"],
        "action": "Push for statewide coverage targets and response-time standards.",
    },
    {
        "title": "Crisis Stabilization Services",
        "why": "Call diversion only works if states also fund places where people can receive immediate stabilization care.",
        "model": "Fund crisis receiving and stabilization facilities in shortage regions first.",
        "states": ["California", "Colorado", "New York"],
        "action": "Pair 988 legislation with stabilization capacity investments in the same bill.",
    },
    {
        "title": "Youth and Family Access",
        "why": "Youth-specific crisis protocols reduce barriers to care and improve continuity after first contact.",
        "model": "Add youth line standards, school referral pathways, and family peer support reimbursement.",
        "states": ["Minnesota", "Oregon", "Washington"],
        "action": "Require youth response metrics in annual 988 performance reports.",
    },
]

FUNDING_OPTIONS = ["All", "Fee enacted", "Recurring appropriation", "No dedicated funding"]
MOBILE_OPTIONS = ["All", "Statewide", "Partial", "Pilot"]
SORT_OPTIONS = ["State A-Z", "Newest policy year", "Highest estimated revenue"]

FUNDING_TONE = {
    "Fee enacted": "chip-green",
    "Recurring appropriation": "chip-amber",
    "No dedicated funding": "chip-rose",
}

MOBILE_TONE = {
    "Statewide": "chip-navy",
    "Partial": "chip-slate",
    "Pilot": "chip-violet",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def revenue_to_millions(value: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*M", value)
    return float(match.group(1)) if match else 0.0


def chip(label: str, css_class: str) -> str:
    return f'<span class="chip {css_class}">{escape(label)}</span>'


def state_cards_html(records: list[dict]) -> str:
    cards = []
    for item in records:
        funding_class = FUNDING_TONE.get(item["funding_model"], "chip-slate")
        mobile_class = MOBILE_TONE.get(item["mobile_crisis"], "chip-slate")
        trust_class = "chip-green" if item["trust_fund"] else "chip-rose"
        trust_text = "Trust Fund: Yes" if item["trust_fund"] else "Trust Fund: No"

        cards.append(
            """
<article class="state-card">
    <div class="state-card-top">
        <h3>{state}</h3>
        <span class="state-year">{year}</span>
    </div>
    <div class="chip-row">
        {funding_chip}
        {mobile_chip}
        {trust_chip}
    </div>
    <div class="state-kv-grid">
        <div class="kv"><span>Monthly Fee</span><strong>{fee}</strong></div>
        <div class="kv"><span>Annual Revenue</span><strong>{revenue}</strong></div>
        <div class="kv"><span>Stabilization</span><strong>{stabilization}</strong></div>
        <div class="kv"><span>Youth Services</span><strong>{youth}</strong></div>
    </div>
    <div class="state-card-foot">
        <span>Latest Bill</span>
        <code>{bill}</code>
    </div>
</article>
""".format(
                state=escape(item["state"]),
                year=item["year"],
                funding_chip=chip(item["funding_model"], funding_class),
                mobile_chip=chip(f"Mobile: {item['mobile_crisis']}", mobile_class),
                trust_chip=chip(trust_text, trust_class),
                fee=escape(item["monthly_fee"]),
                revenue=escape(item["annual_revenue"]),
                stabilization=escape(item["stabilization"]),
                youth=escape(item["youth_services"]),
                bill=escape(item["latest_bill"]),
            )
        )

    return '<div class="state-grid">' + "".join(cards) + "</div>"


def playbook_cards_html(items: list[dict]) -> str:
    cards = []
    for item in items:
        state_chips = "".join(chip(state, "chip-slate") for state in item["states"])
        cards.append(
            """
<article class="playbook-card">
    <h3>{title}</h3>
    <p><strong>Why:</strong> {why}</p>
    <p><strong>Model:</strong> {model}</p>
    <div class="playbook-states">{states}</div>
    <p class="playbook-ask"><strong>Action Ask:</strong> {action}</p>
</article>
""".format(
                title=escape(item["title"]),
                why=escape(item["why"]),
                model=escape(item["model"]),
                states=state_chips,
                action=escape(item["action"]),
            )
        )
    return '<div class="playbook-grid">' + "".join(cards) + "</div>"


def build_script(item: dict) -> str:
    return f"""Subject: Strengthen 988 crisis response policy in {item['state']}

Hello [Legislator Name],

I am your constituent and I support stronger 988 crisis response policy in {item['state']}.

Current tracker snapshot for {item['state']}:
- Funding model: {item['funding_model']}
- Monthly 988 fee: {item['monthly_fee']}
- Trust fund protection: {'Yes' if item['trust_fund'] else 'No'}
- Mobile crisis coverage: {item['mobile_crisis']}
- Stabilization investment: {item['stabilization']}
- Latest policy vehicle: {item['latest_bill']} ({item['year']})

Please support policy that guarantees sustainable funding, statewide mobile crisis access,
and transparent annual performance reporting.

Thank you,
[Your Name]
[City, ZIP]
"""


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,500;6..72,700;6..72,800&display=swap');

:root {
    --bg: #f4f6f2;
    --surface: #ffffff;
    --ink: #17202a;
    --muted: #5c6672;
    --line: #dde2e8;
    --brand-1: #12343b;
    --brand-2: #1e5f64;
    --brand-3: #2f8f83;
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 6% 0%, #d7eadf 0, transparent 24%),
        radial-gradient(circle at 96% 12%, #d4e8ef 0, transparent 20%),
        var(--bg) !important;
    color: var(--ink);
    font-family: 'Sora', sans-serif;
}

header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"], .stDeployButton {
    display: none !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 0.6rem;
    padding-bottom: 2rem;
}

.hero-shell {
    background: linear-gradient(140deg, var(--brand-1) 0%, var(--brand-2) 52%, var(--brand-3) 100%);
    border-radius: 22px;
    padding: 34px 34px 28px;
    color: #e7f7f3;
    box-shadow: 0 16px 34px rgba(18, 52, 59, 0.22);
    margin-bottom: 16px;
}

.hero-kicker {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.9;
}

.hero-title {
    font-family: 'Newsreader', serif;
    font-size: 46px;
    line-height: 1.02;
    margin: 8px 0 10px;
    color: #ffffff;
}

.hero-sub {
    font-size: 15px;
    line-height: 1.55;
    margin: 0;
    max-width: 760px;
    color: #d9f3ee;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 5px 16px rgba(23, 32, 42, 0.06);
}

.metric-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7380;
}

.metric-value {
    font-family: 'Newsreader', serif;
    font-size: 31px;
    line-height: 1;
    margin-top: 6px;
    color: #121a23;
}

.panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 6px 20px rgba(23, 32, 42, 0.06);
}

.section-title {
    font-family: 'Newsreader', serif;
    font-size: 31px;
    margin: 24px 0 10px;
    color: #111924;
}

.section-sub {
    margin: 0 0 12px;
    color: var(--muted);
    font-size: 14px;
}

div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 7px;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] [role="radiogroup"] > label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #fdfefe;
    border: 1px solid #cfd7df;
    border-radius: 999px;
    padding: 4px 10px;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    border-color: #1f7a68;
    background: #e9f7f2;
}

div[data-testid="stRadio"] [role="radiogroup"] > label p,
div[data-testid="stRadio"] [role="radiogroup"] > label span {
    color: #17202a !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 11.2px !important;
    font-weight: 600 !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label input[type="radio"] {
    width: 11px;
    height: 11px;
    margin: 0;
}

div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-testid="stCheckbox"] {
    font-family: 'Sora', sans-serif !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #5b6674 !important;
    font-weight: 600 !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #f8fbff !important;
    border: 1px solid #cfd7df !important;
    border-radius: 12px !important;
    color: #17202a !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] * {
    color: #17202a !important;
}

div[data-testid="stTextInput"] input {
    background: #f8fbff !important;
    color: #17202a !important;
    border: 1px solid #cfd7df !important;
    border-radius: 12px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #7a8491 !important;
}

div[data-testid="stTextArea"] textarea {
    background: #f8fbff !important;
    color: #17202a !important;
    border: 1px solid #cfd7df !important;
    border-radius: 12px !important;
    line-height: 1.5 !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stTextArea"] textarea:focus-visible,
div[data-testid="stTextArea"] textarea:active {
    border: 1px solid #8fb7ae !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-testid="stTextArea"] > div {
    box-shadow: none !important;
    border: none !important;
}

div[data-testid="stTextArea"] {
    box-shadow: none !important;
}

div[data-testid="stCheckbox"] label {
    color: #17202a !important;
}

div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
    color: #17202a !important;
}

div[data-baseweb="popover"] [role="listbox"] {
    background: #ffffff !important;
    border: 1px solid #d3dbe4 !important;
}

div[data-baseweb="popover"] [role="option"] {
    color: #17202a !important;
}

div[data-baseweb="popover"] [aria-selected="true"] {
    background: #e9f7f2 !important;
}

div.stDownloadButton > button {
    background: linear-gradient(135deg, #1f7a68 0%, #2f8f83 100%) !important;
    border: 1px solid #1f7a68 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 20px rgba(31, 122, 104, 0.24);
}

div.stDownloadButton > button:hover {
    filter: brightness(0.98) !important;
    border-color: #186557 !important;
}

.state-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin-top: 10px;
}

.state-card {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 14px;
    background: #fcfdfc;
    box-shadow: 0 4px 12px rgba(12, 20, 32, 0.04);
}

.state-card-top {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 8px;
}

.state-card h3 {
    margin: 0;
    font-size: 20px;
    color: #111a24;
    font-family: 'Newsreader', serif;
}

.state-year {
    font-size: 11px;
    color: #4d5a68;
    font-weight: 600;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 10px;
}

.chip {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 4px 8px;
    border: 1px solid transparent;
}

.chip-green { color: #1f5f3f; background: #e3f6e9; border-color: #bee6cd; }
.chip-amber { color: #7a5715; background: #fff1d9; border-color: #f3dcae; }
.chip-rose { color: #7e2434; background: #ffe5ea; border-color: #f2c5cf; }
.chip-navy { color: #1f3b6f; background: #e4eefc; border-color: #c8d9f3; }
.chip-slate { color: #394b5d; background: #e9eff6; border-color: #d4e0ec; }
.chip-violet { color: #563985; background: #efe8ff; border-color: #dbccff; }

.state-kv-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}

.kv {
    background: #f7fafc;
    border: 1px solid #e7edf4;
    border-radius: 10px;
    padding: 8px;
}

.kv span {
    font-size: 10px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #6c7481;
}

.kv strong {
    display: block;
    margin-top: 3px;
    color: #19212a;
    font-size: 12px;
    line-height: 1.3;
}

.state-card-foot {
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px dashed #d7dde4;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.state-card-foot span {
    font-size: 10px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #66717f;
}

.state-card-foot code {
    background: #eef2f8;
    border-radius: 8px;
    padding: 3px 7px;
    font-size: 11px;
    color: #1e2a37;
}

.trend-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
}

.trend-card {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 12px;
}

.trend-card h4 {
    margin: 0;
    color: #5e6977;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.trend-card .number {
    margin-top: 4px;
    font-size: 30px;
    line-height: 1;
    font-family: 'Newsreader', serif;
    color: #101822;
}

.trend-card p {
    margin: 4px 0 0;
    color: #4f5b67;
    font-size: 12.5px;
}

.playbook-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
}

.playbook-card {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 14px;
    background: #fcfffd;
}

.playbook-card h3 {
    margin: 0 0 8px;
    font-family: 'Newsreader', serif;
    font-size: 24px;
    color: #121c26;
}

.playbook-card p {
    margin: 0 0 8px;
    color: #495563;
    font-size: 13.2px;
    line-height: 1.45;
}

.playbook-states {
    margin: 5px 0 7px;
}

.playbook-ask {
    padding-top: 8px;
    border-top: 1px dashed #d5dce4;
}

.toolkit-shell {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 14px;
    background: #ffffff;
}

.toolkit-note {
    border-left: 4px solid #1f7a68;
    background: #ecf8f3;
    border-radius: 10px;
    padding: 10px 12px;
    color: #204442;
    font-size: 13px;
    margin-bottom: 10px;
}

.snapshot {
    border: 1px solid #dce3ea;
    border-radius: 12px;
    padding: 12px;
    background: #f7fafc;
}

.snapshot h4 {
    margin: 0 0 8px;
    font-size: 17px;
    color: #131d28;
    font-family: 'Newsreader', serif;
}

.snapshot ul {
    margin: 0;
    padding-left: 16px;
    color: #45525f;
    font-size: 13px;
    line-height: 1.5;
}

.source-links {
    margin-top: 10px;
    font-size: 13px;
}

@media (max-width: 980px) {
    .hero-title { font-size: 35px; }
    .state-grid { grid-template-columns: 1fr; }
    .trend-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .playbook-grid { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
    .hero-shell { padding: 22px 18px; }
    .hero-title { font-size: 30px; }
    .trend-grid { grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)

fee_count = sum(1 for row in STATE_POLICIES if row["funding_model"] == "Fee enacted")
recurring_count = sum(1 for row in STATE_POLICIES if row["funding_model"] == "Recurring appropriation")
trust_count = sum(1 for row in STATE_POLICIES if row["trust_fund"])
statewide_mobile = sum(1 for row in STATE_POLICIES if row["mobile_crisis"] == "Statewide")

top_state = max(STATE_POLICIES, key=lambda row: revenue_to_millions(row["annual_revenue"]))

st.markdown(
    f"""
<section class="hero-shell">
    <div class="hero-kicker">NAMI Policy Product Prototype</div>
    <h1 class="hero-title">988 State Policy Tracker</h1>
    <p class="hero-sub">Policy-first web experience for advocates. Scan funding and crisis infrastructure quickly, identify peer-state examples, and generate outreach language without opening a PDF.</p>
</section>
""",
    unsafe_allow_html=True,
)

metric_specs = [
    ("States tracked", str(len(STATE_POLICIES))),
    ("Fee enacted", str(fee_count)),
    ("Recurring appropriations", str(recurring_count)),
    ("Statewide mobile", str(statewide_mobile)),
]

metric_cols = st.columns(4)
for col, (label, value) in zip(metric_cols, metric_specs):
    with col:
        st.markdown(
            f"""
<div class="metric-card">
    <div class="metric-label">{escape(label)}</div>
    <div class="metric-value">{escape(value)}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<h2 class="section-title">State Explorer</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-sub">Filter by funding model, service maturity, and trust fund status. Cards are optimized for quick scanning on desktop and mobile.</p>',
    unsafe_allow_html=True,
)

with st.container(border=False):
    filter_cols = st.columns([3.4, 2.0, 1.5, 2.4, 1.8])
    with filter_cols[0]:
        funding_filter = st.radio(
            "Funding",
            FUNDING_OPTIONS,
            horizontal=True,
            label_visibility="collapsed",
        )
    with filter_cols[1]:
        mobile_filter = st.selectbox("Mobile coverage", MOBILE_OPTIONS)
    with filter_cols[2]:
        trust_only = st.checkbox("Trust only", value=False)
    with filter_cols[3]:
        search_query = st.text_input("Search", placeholder="State, bill, stabilization")
    with filter_cols[4]:
        sort_by = st.selectbox("Sort", SORT_OPTIONS)

filtered = []
search_norm = search_query.strip().lower()
for row in STATE_POLICIES:
    if funding_filter != "All" and row["funding_model"] != funding_filter:
        continue
    if mobile_filter != "All" and row["mobile_crisis"] != mobile_filter:
        continue
    if trust_only and not row["trust_fund"]:
        continue

    haystack = " ".join(
        [
            row["state"],
            row["latest_bill"],
            row["annual_revenue"],
            row["stabilization"],
            row["youth_services"],
        ]
    ).lower()

    if search_norm and search_norm not in haystack:
        continue

    filtered.append(row)

if sort_by == "State A-Z":
    filtered = sorted(filtered, key=lambda row: row["state"])
elif sort_by == "Newest policy year":
    filtered = sorted(filtered, key=lambda row: (row["year"], row["state"]), reverse=True)
else:
    filtered = sorted(
        filtered,
        key=lambda row: (revenue_to_millions(row["annual_revenue"]), row["state"]),
        reverse=True,
    )

st.markdown(
    f"""
<div class="panel">
    <div class="section-sub"><strong>{len(filtered)}</strong> state profiles shown. Highest estimated revenue in this dataset: <strong>{escape(top_state['state'])}</strong> ({escape(top_state['annual_revenue'])}).</div>
    {state_cards_html(filtered) if filtered else '<div class="toolkit-note">No states matched this filter set. Broaden search terms or reset filters.</div>'}
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-title">What Changed This Year</h2>', unsafe_allow_html=True)

trend_html = f"""
<div class="trend-grid">
    <article class="trend-card">
        <h4>Funding Coverage</h4>
        <div class="number">{fee_count}</div>
        <p>States in this prototype currently using dedicated 988 fees.</p>
    </article>
    <article class="trend-card">
        <h4>Trust Fund Adoption</h4>
        <div class="number">{trust_count}</div>
        <p>States with statutory protection for 988 dollars.</p>
    </article>
    <article class="trend-card">
        <h4>Statewide Mobile</h4>
        <div class="number">{statewide_mobile}</div>
        <p>States reporting statewide mobile crisis coverage.</p>
    </article>
    <article class="trend-card">
        <h4>Most Recent Bills</h4>
        <div class="number">2025</div>
        <p>Latest policy years in this dataset include 2025 sessions.</p>
    </article>
</div>
"""
st.markdown(trend_html, unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Policy Playbook</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-sub">Each card includes a policy frame, model direction, peer-state examples, and a concrete ask.</p>',
    unsafe_allow_html=True,
)
st.markdown(playbook_cards_html(PLAYBOOK), unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Advocate Toolkit</h2>', unsafe_allow_html=True)

tool_cols = st.columns([1.05, 1.35])
with tool_cols[0]:
    st.markdown(
        '<div class="toolkit-note">Use this as a starting point. Personalize with local outcomes or provider stories before sending.</div>',
        unsafe_allow_html=True,
    )
    state_names = sorted([row["state"] for row in STATE_POLICIES])
    selected_state = st.selectbox("Build script for state", state_names)
    selected = next(row for row in STATE_POLICIES if row["state"] == selected_state)
    snapshot_html = f"""
<div class="snapshot">
    <h4>{escape(selected['state'])} Snapshot</h4>
    <ul>
        <li><strong>Funding:</strong> {escape(selected['funding_model'])}</li>
        <li><strong>Monthly fee:</strong> {escape(selected['monthly_fee'])}</li>
        <li><strong>Trust fund:</strong> {'Yes' if selected['trust_fund'] else 'No'}</li>
        <li><strong>Mobile crisis:</strong> {escape(selected['mobile_crisis'])}</li>
        <li><strong>Latest bill:</strong> {escape(selected['latest_bill'])} ({selected['year']})</li>
    </ul>
</div>
"""
    st.markdown(snapshot_html, unsafe_allow_html=True)

with tool_cols[1]:
    draft = st.text_area(
        "Message draft",
        value=build_script(selected),
        height=320,
    )
    st.download_button(
        "Download advocacy script",
        data=draft,
        file_name=f"{slugify(selected_state)}-988-advocacy-script.txt",
        mime="text/plain",
    )

st.markdown(
    '<div class="source-links">Sources: <a href="https://www.usa.gov/elected-officials" target="_blank">Find elected officials</a> | <a href="https://www.nami.org/research/publications-reports/public-policy-reports/" target="_blank">NAMI public policy reports</a></div>',
    unsafe_allow_html=True,
)
