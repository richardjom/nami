import re
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
        "action": "Ask for a protected funding mechanism tied to annual reporting and transparency.",
    },
    {
        "title": "Mobile Crisis Teams",
        "why": "Mobile response gives people in crisis care in community settings and reduces law enforcement involvement.",
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
        "why": "Youth-specific crisis protocols reduce barriers to care and improve continuity after the first call.",
        "model": "Add youth line standards, school referral pathways, and family peer support reimbursement.",
        "states": ["Minnesota", "Oregon", "Washington"],
        "action": "Require youth response metrics in annual 988 performance reports.",
    },
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def state_row(record: dict) -> dict:
    return {
        "State": record["state"],
        "Funding": record["funding_model"],
        "Monthly 988 Fee": record["monthly_fee"],
        "Annual Revenue": record["annual_revenue"],
        "Trust Fund": "Yes" if record["trust_fund"] else "No",
        "Mobile Crisis": record["mobile_crisis"],
        "Stabilization": record["stabilization"],
        "Youth Services": record["youth_services"],
        "Latest Bill": record["latest_bill"],
        "Year": record["year"],
    }


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,900&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F6F7F4 !important;
    font-family: 'DM Sans', sans-serif;
}
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"] {
    display: none !important;
}
.block-container {
    max-width: 1150px;
    padding-top: 0.5rem;
}

.hero {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%);
    border-radius: 18px;
    padding: 30px 34px;
    margin-bottom: 20px;
}
.hero-kicker {
    color: #B7E4C7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-size: 38px;
    line-height: 1.08;
    color: #FFFFFF;
    margin: 0 0 8px;
}
.hero p {
    color: #D8F3DC;
    font-size: 15px;
    margin: 0;
    max-width: 760px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 14px 16px;
}
.metric-card .label {
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 4px;
}
.metric-card .value {
    font-family: 'Fraunces', serif;
    font-size: 26px;
    color: #111827;
}

div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 8px;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] [role="radiogroup"] > label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border: 1px solid #D1D5DB;
    border-radius: 999px;
    background: #FFFFFF;
}
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    border-color: #2D6A4F;
    background: #F0FDF4;
}
div[data-testid="stRadio"] [role="radiogroup"] > label p,
div[data-testid="stRadio"] [role="radiogroup"] > label span {
    color: #111827 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 11.5px !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label input[type="radio"] {
    width: 12px;
    height: 12px;
    margin: 0;
}

.trend-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 14px 16px;
    min-height: 122px;
}
.trend-title {
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #6B7280;
    margin: 0 0 4px;
}
.trend-value {
    font-family: 'Fraunces', serif;
    font-size: 28px;
    color: #111827;
    margin: 0 0 2px;
}
.trend-detail {
    font-size: 13px;
    color: #4B5563;
    margin: 0;
}

.section-head {
    font-family: 'Fraunces', serif;
    font-size: 24px;
    color: #111827;
    margin: 26px 0 10px;
}

.note-box {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-left: 4px solid #2D6A4F;
    border-radius: 12px;
    padding: 16px;
}
</style>
""",
    unsafe_allow_html=True,
)

fee_count = sum(1 for s in STATE_POLICIES if s["funding_model"] == "Fee enacted")
trust_count = sum(1 for s in STATE_POLICIES if s["trust_fund"])
statewide_mobile = sum(1 for s in STATE_POLICIES if s["mobile_crisis"] == "Statewide")
youth_yes = sum(1 for s in STATE_POLICIES if s["youth_services"] == "Yes")

st.markdown(
    f"""
<div class="hero">
    <div class="hero-kicker">NAMI Policy Product Prototype</div>
    <h1>988 State Policy Tracker</h1>
    <p>Table-first policy experience for advocates. Explore state funding and crisis response policy, scan annual trends, then use a ready-to-send action script.</p>
</div>
""",
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
metrics = [
    ("States tracked", str(len(STATE_POLICIES))),
    ("Fee enacted", str(fee_count)),
    ("Trust funds", str(trust_count)),
    ("Statewide mobile", str(statewide_mobile)),
]
for col, (label, value) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
<div class="metric-card">
    <div class="label">{label}</div>
    <div class="value">{value}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-head">State Explorer</div>', unsafe_allow_html=True)

FUNDING_OPTIONS = ["All", "Fee enacted", "Recurring appropriation", "No dedicated funding"]
col_filters, col_trust, col_search = st.columns([4, 1.5, 2.5])

with col_filters:
    funding_filter = st.radio(
        "Funding filter",
        FUNDING_OPTIONS,
        horizontal=True,
        label_visibility="collapsed",
    )
with col_trust:
    trust_only = st.checkbox("Trust fund only", value=False)
with col_search:
    query = st.text_input("Search", placeholder="State, bill, or policy term")

filtered = []
q = query.strip().lower()
for row in STATE_POLICIES:
    if funding_filter != "All" and row["funding_model"] != funding_filter:
        continue
    if trust_only and not row["trust_fund"]:
        continue
    haystack = " ".join(
        [
            row["state"],
            row["latest_bill"],
            row["mobile_crisis"],
            row["stabilization"],
            row["youth_services"],
        ]
    ).lower()
    if q and q not in haystack:
        continue
    filtered.append(row)

if filtered:
    st.dataframe(
        [state_row(record) for record in filtered],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning("No states matched this filter set. Try broadening the search.")

st.caption(
    "Prototype dataset for layout and flow. Replace these rows with verified state records before publishing."
)

st.markdown('<div class="section-head">What Changed This Year</div>', unsafe_allow_html=True)

trend_cards = [
    {
        "title": "Funding coverage",
        "value": f"{fee_count} states",
        "detail": "Use dedicated 988 fees in this prototype dataset.",
    },
    {
        "title": "Trust fund adoption",
        "value": f"{trust_count} states",
        "detail": "Protect 988 dollars from being absorbed into general budgets.",
    },
    {
        "title": "Mobile crisis reach",
        "value": f"{statewide_mobile} statewide",
        "detail": "Have statewide mobile crisis as the baseline service model.",
    },
    {
        "title": "Youth readiness",
        "value": f"{youth_yes} states",
        "detail": "Show explicit youth-focused response standards.",
    },
]

trend_cols = st.columns(4)
for col, card in zip(trend_cols, trend_cards):
    with col:
        st.markdown(
            f"""
<div class="trend-card">
    <p class="trend-title">{card['title']}</p>
    <p class="trend-value">{card['value']}</p>
    <p class="trend-detail">{card['detail']}</p>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-head">Policy Playbook</div>', unsafe_allow_html=True)
for item in PLAYBOOK:
    with st.expander(item["title"], expanded=False):
        st.markdown(f"**Why this matters**  \n{item['why']}")
        st.markdown(f"**Model policy language**  \n{item['model']}")
        st.markdown(f"**States to cite**  \n{', '.join(item['states'])}")
        st.markdown(f"**Action ask**  \n{item['action']}")

st.markdown('<div class="section-head">Advocate Toolkit</div>', unsafe_allow_html=True)

state_names = sorted([row["state"] for row in STATE_POLICIES])
selected_state = st.selectbox("Build script for state", state_names)
current = next(row for row in STATE_POLICIES if row["state"] == selected_state)

script = f"""Subject: Strengthen 988 crisis response policy in {current['state']}

Hello [Legislator Name],

I am your constituent and I support stronger 988 crisis response policy in {current['state']}.

Current tracker snapshot for {current['state']}:
- Funding model: {current['funding_model']}
- Monthly 988 fee: {current['monthly_fee']}
- Trust fund protection: {'Yes' if current['trust_fund'] else 'No'}
- Mobile crisis coverage: {current['mobile_crisis']}
- Latest policy vehicle: {current['latest_bill']} ({current['year']})

Please support policy that guarantees sustainable funding, statewide mobile crisis access,
and transparent annual performance reporting.

Thank you,
[Your Name]
[City, ZIP]
"""

st.markdown('<div class="note-box">Use this script as a base, then personalize with your local context.</div>', unsafe_allow_html=True)
st.code(script, language="markdown")
st.download_button(
    "Download advocacy script",
    data=script,
    file_name=f"{slugify(selected_state)}-988-advocacy-script.txt",
    mime="text/plain",
)

st.markdown(
    "[Find your elected officials](https://www.usa.gov/elected-officials) | [NAMI public policy reports](https://www.nami.org/research/publications-reports/public-policy-reports/)"
)
