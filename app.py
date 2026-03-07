import streamlit as st
import json
from html import escape

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="988 & Crisis Response | NAMI 2024 Issue Brief",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def rerun_app() -> None:
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ---------------------------------------------------------------------------
# State comparison data
# ---------------------------------------------------------------------------
STATE_DATA = {
    "Colorado": {
        "fee": "$0.50",
        "fee_start": "Jan 2023",
        "est_revenue": "$34.5M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": True,
        "key_bill": "HB 22-1302",
        "highlights": "One of the first states to enact a 988 fee. Comprehensive crisis system investment including mobile teams statewide.",
    },
    "Washington": {
        "fee": "$0.24",
        "fee_start": "Oct 2024",
        "est_revenue": "$43.7M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": True,
        "key_bill": "SB 5120",
        "highlights": "National leader in crisis system redesign. Established dedicated 988 behavioral health crisis response account.",
    },
    "Nevada": {
        "fee": "$0.35",
        "fee_start": "Jan 2024",
        "est_revenue": "$10.5M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": False,
        "youth_services": False,
        "key_bill": "AB 51",
        "highlights": "Enacted fee with trust fund protections against diversion. Building out mobile crisis team infrastructure.",
    },
    "Virginia": {
        "fee": "$0.12",
        "fee_start": "Jan 2024",
        "est_revenue": "$12.8M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": False,
        "key_bill": "HB 2495",
        "highlights": "Bipartisan legislation establishing fee and comprehensive crisis care. Investing in Marcus Alert mobile crisis program.",
    },
    "Maryland": {
        "fee": "$0.25",
        "fee_start": "Oct 2024",
        "est_revenue": "$18.2M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": False,
        "youth_services": True,
        "key_bill": "HB 317",
        "highlights": "Established 988 Trust Fund with dedicated fee revenue. Expanding crisis services with emphasis on youth and underserved communities.",
    },
    "Ohio": {
        "fee": "None",
        "fee_start": "N/A",
        "est_revenue": "N/A",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": True,
        "key_bill": "HB 33",
        "highlights": "Created 988 trust fund through budget process with $45M appropriation. Investing in statewide mobile crisis team expansion.",
    },
    "Minnesota": {
        "fee": "$0.12",
        "fee_start": "Jan 2024",
        "est_revenue": "$8.6M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": True,
        "key_bill": "HF 2310",
        "highlights": "Comprehensive crisis system with mobile teams in every county. Strong advocate community driving sustainable funding model.",
    },
    "Connecticut": {
        "fee": "$0.20",
        "fee_start": "Sept 2024",
        "est_revenue": "$7.2M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": False,
        "key_bill": "SB 2",
        "highlights": "Enacted fee alongside expanded crisis stabilization requirements. Pioneering integration of 988 with existing mobile crisis teams.",
    },
    "California": {
        "fee": "$0.08",
        "fee_start": "Jan 2023",
        "est_revenue": "$120M",
        "trust_fund": True,
        "mobile_crisis": True,
        "crisis_stabilization": True,
        "youth_services": True,
        "key_bill": "AB 988",
        "highlights": "Largest 988 fee revenue in the nation due to population. Building out county-level crisis infrastructure across the state.",
    },
    "Vermont": {
        "fee": "$0.72",
        "fee_start": "Sept 2024",
        "est_revenue": "$2.1M",
        "trust_fund": False,
        "mobile_crisis": True,
        "crisis_stabilization": False,
        "youth_services": False,
        "key_bill": "S.58",
        "highlights": "Highest per-line fee in the nation. Funds distributed to support crisis call center operations and telecommunications relay.",
    },
}

# ---------------------------------------------------------------------------
# Policy categories
# ---------------------------------------------------------------------------
POLICY_CARDS = [
    {
        "icon": "💰",
        "title": "Sustainable Funding",
        "subtitle": "The foundation of effective crisis care",
        "description": "States need permanent, dedicated funding streams to keep 988 and crisis services operational. Telecom fees mirror the proven 911 funding model and provide predictable revenue without relying on annual budget fights.",
        "leading_states": ["Colorado", "Washington", "California"],
        "stat": "12",
        "stat_label": "states with 988 telecom fees",
        "recommendation": "Enact a monthly telecom fee dedicated to 988 and crisis services, protected by a trust fund to prevent fee diversion.",
    },
    {
        "icon": "🚐",
        "title": "Mobile Crisis Teams",
        "subtitle": "Someone to respond",
        "description": "When someone calls 988, they may need more than a phone conversation. Mobile crisis teams bring licensed professionals to the person in distress, providing on-site assessment and de-escalation as an alternative to law enforcement response.",
        "leading_states": ["Virginia", "Ohio", "Minnesota"],
        "stat": "18",
        "stat_label": "states expanded mobile crisis in 2024",
        "recommendation": "Fund and deploy mobile crisis teams statewide, ensuring response in both urban and rural communities within 60 minutes.",
    },
    {
        "icon": "🏥",
        "title": "Crisis Stabilization",
        "subtitle": "A safe place for help",
        "description": "Crisis stabilization facilities provide short-term care for individuals experiencing a mental health crisis, offering an alternative to emergency rooms and jails. These facilities can provide up to 23 hours of observation and treatment.",
        "leading_states": ["Washington", "Ohio", "Connecticut"],
        "stat": "14",
        "stat_label": "states funded new stabilization centers",
        "recommendation": "Invest in crisis stabilization units and crisis residential programs to ensure every community has a safe, therapeutic alternative to ERs.",
    },
    {
        "icon": "🧒",
        "title": "Youth Crisis Services",
        "subtitle": "Meeting young people where they are",
        "description": "Youth experiencing mental health crises have unique needs. Specialized crisis services for children and adolescents include school-based crisis teams, youth-specific hotlines, and age-appropriate stabilization programs.",
        "leading_states": ["Washington", "Maryland", "Minnesota"],
        "stat": "11",
        "stat_label": "states passed youth crisis legislation",
        "recommendation": "Establish youth-specific crisis response protocols and fund specialized training for crisis workers serving children and adolescents.",
    },
    {
        "icon": "🛡️",
        "title": "Trust Fund Protections",
        "subtitle": "Ensuring funds reach crisis services",
        "description": "Without dedicated trust funds, 988 fee revenue can be diverted to unrelated budget items. Trust fund legislation ensures every dollar collected goes directly to supporting crisis call centers, mobile teams, and stabilization services.",
        "leading_states": ["Colorado", "Nevada", "Ohio"],
        "stat": "10",
        "stat_label": "states with 988 trust funds",
        "recommendation": "Establish a dedicated 988 trust fund with statutory protections preventing fee revenue from being diverted to other purposes.",
    },
]

# ---------------------------------------------------------------------------
# Timeline milestones
# ---------------------------------------------------------------------------
TIMELINE = [
    {
        "date": "Oct 2020",
        "title": "National Suicide Hotline Designation Act Signed",
        "description": "Federal law designates 988 as the new three-digit number for the Suicide and Crisis Lifeline, giving states the option to enact telecom fees for funding.",
        "type": "federal",
    },
    {
        "date": "Jul 2022",
        "title": "988 Goes Live Nationwide",
        "description": "The 988 Suicide and Crisis Lifeline officially launches across the country, replacing the previous 10-digit number.",
        "type": "milestone",
    },
    {
        "date": "Jan 2023",
        "title": "First State Fees Take Effect",
        "description": "Colorado and California become among the first states to begin collecting 988 telecom fees, establishing a model for sustainable funding.",
        "type": "state",
    },
    {
        "date": "Jul 2023",
        "title": "One Year: 5M+ Contacts",
        "description": "988 surpasses 5 million calls, texts, and chats in its first year. Answer rates improve but capacity challenges remain in many states.",
        "type": "milestone",
    },
    {
        "date": "2024 Sessions",
        "title": "Wave of State Legislation",
        "description": "Multiple states enact 988 fees, trust funds, mobile crisis team funding, and crisis stabilization investments in their 2024 legislative sessions.",
        "type": "state",
    },
    {
        "date": "Jul 2024",
        "title": "Two Years: 10M+ Contacts",
        "description": "More than 10 million contacts made to 988. Two-thirds of people who contacted 988 report getting the help they needed.",
        "type": "milestone",
    },
    {
        "date": "Jul 2025",
        "title": "Three Years: Awareness Peaks",
        "description": "988 awareness reaches its highest level. 75% of Americans support a monthly phone fee to fund crisis services. 12 states now have 988 fees enacted.",
        "type": "milestone",
    },
    {
        "date": "2025 & Beyond",
        "title": "Building Comprehensive Systems",
        "description": "The focus shifts from launching 988 to building complete crisis care continuums in every state: someone to call, someone to respond, somewhere to go.",
        "type": "federal",
    },
]

# ---------------------------------------------------------------------------
# Advocate quotes
# ---------------------------------------------------------------------------
ADVOCATES = [
    {
        "quote": "If you or someone you know is in crisis, please remember you are not alone. Call or text 988 for support. Mental health touches every family and every community.",
        "name": "Daniel H. Gillison, Jr.",
        "role": "CEO, NAMI",
        "accent": "#2D6A4F",
    },
    {
        "quote": "Sustainable funding is the backbone of any effective crisis system. Without it, call centers can't hire enough counselors, and mobile teams can't reach the communities that need them most.",
        "name": "Sue Abderholden",
        "role": "Executive Director, NAMI Minnesota",
        "accent": "#1E40AF",
    },
    {
        "quote": "We need leaders at every level to keep building strong crisis response systems so that when someone needs help, they have someone to contact, someone to respond, and a safe place for help.",
        "name": "NAMI Reimagine Crisis",
        "role": "National Initiative",
        "accent": "#7C3AED",
    },
]

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --green-900: #0F2D1E;
    --green-800: #1B4332;
    --green-700: #2D6A4F;
    --green-600: #40916C;
    --green-400: #74C69D;
    --green-200: #B7E4C7;
    --green-100: #D8F3DC;
    --green-50: #F0FDF4;
    --slate-900: #0F172A;
    --slate-700: #334155;
    --slate-500: #64748B;
    --slate-300: #CBD5E1;
    --slate-100: #F1F5F9;
    --warm-bg: #FAFAF7;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--warm-bg) !important;
    font-family: 'Source Sans 3', sans-serif !important;
}
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0 !important; max-width: 1100px !important; }
#MainMenu, footer, [data-testid="stToolbar"], .stDeployButton { display: none !important; }

/* ---- HERO ---- */
.hero {
    background: linear-gradient(160deg, #0F2D1E 0%, #1B4332 35%, #2D6A4F 70%, #40916C 100%);
    padding: 60px 52px 56px;
    border-radius: 0 0 28px 28px;
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
}
.hero::before {
    content: '';
    position: absolute;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(183,228,199,0.08) 0%, transparent 70%);
    top: -200px; right: -100px;
}
.hero::after {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    border: 1px solid rgba(183,228,199,0.1);
    bottom: -100px; left: 5%;
}
.hero-eyebrow {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px; font-weight: 600;
    color: var(--green-400);
    letter-spacing: 0.2em; text-transform: uppercase;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 10px;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 28px; height: 1.5px;
    background: var(--green-400);
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 52px; font-weight: 900;
    color: #FFFFFF; line-height: 1.05;
    margin: 0 0 20px; max-width: 650px;
    letter-spacing: -0.02em;
}
.hero h1 em {
    color: var(--green-200);
    font-style: italic; font-weight: 400;
}
.hero-sub {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 18px; font-weight: 300;
    color: var(--green-200);
    line-height: 1.7; max-width: 540px;
    margin: 0;
}

/* ---- BIG NUMBERS ---- */
.big-numbers {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    margin: -32px 32px 0;
    position: relative; z-index: 10;
}
.big-num-card {
    background: #FFFFFF;
    padding: 36px 32px;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.04);
}
.big-num-card:first-child { border-radius: 16px 0 0 16px; }
.big-num-card:last-child { border-radius: 0 16px 16px 0; }
.big-num-card .number {
    font-family: 'Playfair Display', serif;
    font-size: 54px; font-weight: 900;
    color: var(--green-700);
    line-height: 1;
    margin-bottom: 8px;
}
.big-num-card .unit {
    font-family: 'Playfair Display', serif;
    font-size: 24px; font-weight: 400;
    color: var(--green-600);
}
.big-num-card .desc {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px; font-weight: 500;
    color: var(--slate-500);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 4px;
}
.big-num-card .context {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 400;
    color: var(--slate-700);
    line-height: 1.5;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--slate-100);
}

/* ---- SECTION HEADERS ---- */
.section-header {
    padding: 56px 0 8px;
}
.section-header .eyebrow {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px; font-weight: 600;
    color: var(--green-600);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex; align-items: center; gap: 10px;
}
.section-header .eyebrow::before {
    content: '';
    display: inline-block;
    width: 20px; height: 1.5px;
    background: var(--green-600);
}
.section-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 36px; font-weight: 900;
    color: var(--slate-900);
    line-height: 1.15;
    margin: 0 0 12px;
    letter-spacing: -0.02em;
}
.section-header p {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 17px; font-weight: 400;
    color: var(--slate-500);
    line-height: 1.6;
    max-width: 600px;
    margin: 0;
}

/* ---- DATA STORY ---- */
.data-callout {
    background: var(--green-800);
    border-radius: 20px;
    padding: 48px;
    margin: 32px 0;
    position: relative;
    overflow: hidden;
}
.data-callout::before {
    content: '';
    position: absolute;
    width: 250px; height: 250px;
    border-radius: 50%;
    background: rgba(183,228,199,0.06);
    top: -80px; right: -40px;
}
.data-callout .big-stat {
    font-family: 'Playfair Display', serif;
    font-size: 72px; font-weight: 900;
    color: var(--green-200);
    line-height: 1;
    margin-bottom: 8px;
    position: relative;
}
.data-callout .big-label {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 22px; font-weight: 400;
    color: #FFFFFF;
    line-height: 1.4;
    max-width: 500px;
    position: relative;
}
.data-callout .big-context {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 15px; font-weight: 300;
    color: var(--green-400);
    line-height: 1.6;
    max-width: 500px;
    margin-top: 16px;
    position: relative;
}

.fee-bar-section {
    margin: 28px 0;
}
.fee-bar-item {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
}
.fee-bar-state {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 600;
    color: var(--slate-700);
    width: 100px; flex-shrink: 0;
    text-align: right;
}
.fee-bar-track {
    flex: 1;
    height: 32px;
    background: var(--slate-100);
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}
.fee-bar-fill {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; font-weight: 500;
    color: #FFFFFF;
    min-width: 60px;
    transition: width 0.8s ease;
}

/* ---- TIMELINE ---- */
.timeline-container {
    position: relative;
    padding: 20px 0 20px 40px;
    margin: 20px 0;
}
.timeline-container::before {
    content: '';
    position: absolute;
    left: 18px; top: 0; bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, var(--green-200), var(--green-600), var(--green-200));
}
.timeline-item {
    position: relative;
    padding: 0 0 36px 36px;
}
.timeline-item::before {
    content: '';
    position: absolute;
    left: -30px; top: 6px;
    width: 14px; height: 14px;
    border-radius: 50%;
    border: 3px solid var(--green-600);
    background: #FFFFFF;
    z-index: 2;
}
.timeline-item.milestone::before {
    background: var(--green-600);
    box-shadow: 0 0 0 4px var(--green-200);
    width: 16px; height: 16px;
    left: -31px;
}
.timeline-item .t-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; font-weight: 500;
    color: var(--green-600);
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}
.timeline-item .t-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px; font-weight: 700;
    color: var(--slate-900);
    margin-bottom: 6px;
    line-height: 1.3;
}
.timeline-item .t-desc {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 400;
    color: var(--slate-500);
    line-height: 1.6;
    max-width: 520px;
}

/* ---- POLICY CARDS ---- */
.policy-disclosure {
    background: #FFFFFF;
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,0,0,0.04);
    box-shadow: 0 2px 12px rgba(0,0,0,0.03);
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}
.policy-disclosure:hover {
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    transform: translateY(-2px);
}
.policy-disclosure[open] {
    border: 2px solid var(--green-700);
    box-shadow: 0 10px 30px rgba(45,106,79,0.14);
}
.policy-disclosure > summary {
    list-style: none;
    cursor: pointer;
    position: relative;
    padding: 32px;
}
.policy-disclosure > summary::-webkit-details-marker {
    display: none;
}
.policy-disclosure > summary::after {
    content: '+';
    position: absolute;
    top: 22px;
    right: 22px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--slate-100);
    color: var(--slate-500);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    font-weight: 300;
    line-height: 1;
}
.policy-disclosure[open] > summary::after {
    content: '×';
    background: var(--green-700);
    color: #FFFFFF;
    font-size: 32px;
}
.policy-body {
    padding: 0 32px 32px;
}
.policy-disclosure .p-icon {
    font-size: 28px;
    margin-bottom: 12px;
}
.policy-disclosure .p-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px; font-weight: 700;
    color: var(--slate-900);
    margin-bottom: 4px;
}
.policy-disclosure .p-subtitle {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px; font-weight: 500;
    color: var(--green-600);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.policy-disclosure .p-desc {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 15px; font-weight: 400;
    color: var(--slate-700);
    line-height: 1.65;
    margin-bottom: 20px;
}
.policy-stat-badge {
    display: inline-flex;
    align-items: baseline;
    gap: 6px;
    background: var(--green-50);
    border: 1px solid var(--green-200);
    border-radius: 10px;
    padding: 10px 18px;
    margin-bottom: 16px;
}
.policy-stat-badge .ps-num {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 900;
    color: var(--green-700);
    line-height: 1;
}
.policy-stat-badge .ps-label {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px; font-weight: 500;
    color: var(--green-700);
}
.leading-states {
    display: flex; gap: 6px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}
.leading-states .ls-tag {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px; font-weight: 600;
    color: var(--green-700);
    background: var(--green-100);
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.02em;
}
.rec-box {
    background: var(--slate-100);
    border-radius: 10px;
    padding: 16px 20px;
    border-left: 3px solid var(--green-600);
}
.rec-box .rec-label {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10px; font-weight: 700;
    color: var(--green-700);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.rec-box .rec-text {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 400;
    color: var(--slate-700);
    line-height: 1.6;
}

/* ---- ADVOCATE QUOTES ---- */
.advocate-card {
    border-radius: 16px;
    padding: 36px;
    margin-bottom: 20px;
    position: relative;
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.04);
}
.advocate-card::before {
    content: '"';
    font-family: 'Playfair Display', serif;
    font-size: 80px;
    position: absolute;
    top: 16px; left: 28px;
    line-height: 1;
    opacity: 0.12;
}
.advocate-card .aq-text {
    font-family: 'Playfair Display', serif;
    font-size: 18px; font-weight: 400;
    font-style: italic;
    color: var(--slate-900);
    line-height: 1.6;
    margin-bottom: 20px;
    position: relative;
}
.advocate-card .aq-name {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 700;
    color: var(--slate-900);
}
.advocate-card .aq-role {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px; font-weight: 400;
    color: var(--slate-500);
}
.advocate-accent {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
}

/* ---- COMPARISON TABLE ---- */
.compare-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 20px 0;
    background: #FFFFFF;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.compare-table th {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px; font-weight: 700;
    color: var(--slate-500);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 16px 20px;
    background: var(--slate-100);
    text-align: left;
    border-bottom: 2px solid var(--green-200);
}
.compare-table td {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    color: var(--slate-700);
    padding: 14px 20px;
    border-bottom: 1px solid var(--slate-100);
    vertical-align: top;
}
.compare-table tr:last-child td { border-bottom: none; }
.compare-table .state-name {
    font-weight: 700;
    color: var(--slate-900);
}
.check { color: var(--green-600); font-weight: 700; }
.cross { color: var(--slate-300); }

/* ---- STATE CHIP HEADER ---- */
.state-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 2px 0 18px;
}
.state-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 40px;
    padding: 0 20px;
    border-radius: 12px;
    border: 1.5px solid var(--slate-300);
    background: #FFFFFF;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--slate-700);
    line-height: 1;
}
/* Clickable compare chips (Streamlit buttons) */
div[data-testid="stButton"] {
    margin-bottom: 0.2rem;
}
div[data-testid="stButton"] > button {
    background: #FFFFFF;
    border: 1.5px solid var(--slate-300);
    border-radius: 12px;
    color: var(--slate-700);
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;
    padding: 0.35rem 1rem;
    box-shadow: none !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--slate-500);
    color: var(--slate-900);
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: #EEF7F2 !important;
    border-color: var(--green-400) !important;
    color: var(--green-800) !important;
}

/* ---- FOOTER CTA ---- */
.footer-cta {
    background: linear-gradient(135deg, var(--green-900) 0%, var(--green-800) 50%, var(--green-700) 100%);
    border-radius: 20px;
    padding: 52px;
    text-align: center;
    margin: 40px 0 48px;
    position: relative;
    overflow: hidden;
}
.footer-cta::before {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(183,228,199,0.05);
    top: -100px; right: -50px;
}
.footer-cta h3 {
    font-family: 'Playfair Display', serif;
    font-size: 32px; font-weight: 900;
    color: #FFFFFF;
    margin: 0 0 12px; position: relative;
}
.footer-cta p {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 16px; font-weight: 300;
    color: var(--green-200);
    margin: 0 0 28px; position: relative;
    max-width: 480px;
    margin-left: auto; margin-right: auto;
}
.footer-cta .cta-buttons {
    display: flex; gap: 14px;
    justify-content: center; flex-wrap: wrap;
    position: relative;
}
.cta-btn {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px; font-weight: 700;
    padding: 14px 32px;
    border-radius: 12px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-block;
}
.cta-btn.primary {
    background: var(--green-200);
    color: var(--green-900);
}
.cta-btn.primary:hover { background: #FFFFFF; }
.cta-btn.secondary {
    background: rgba(255,255,255,0.1);
    color: #FFFFFF;
    border: 1.5px solid rgba(255,255,255,0.2);
}
.cta-btn.secondary:hover { background: rgba(255,255,255,0.2); }

/* Streamlit overrides */
.stSelectbox label, .stMultiSelect label {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    color: var(--slate-700) !important;
}
div[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# HERO
# ===========================================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">NAMI 2024 State Legislation Issue Brief</div>
    <h1>Trends in 988 &<br><em>Reimagining Crisis<br>Response</em></h1>
    <p class="hero-sub">
        People in a mental health crisis deserve a compassionate and effective response.
        Here's how states are building the systems to deliver one.
    </p>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# BIG NUMBERS
# ===========================================================================
st.markdown("""
<div class="big-numbers">
    <div class="big-num-card">
        <div class="number">10<span class="unit">M+</span></div>
        <div class="desc">Contacts to 988</div>
        <div class="context">Calls, texts, and chats since the lifeline launched in July 2022</div>
    </div>
    <div class="big-num-card">
        <div class="number">12</div>
        <div class="desc">States with 988 Fees</div>
        <div class="context">Sustainable telecom fees modeled after the proven 911 funding approach</div>
    </div>
    <div class="big-num-card">
        <div class="number">75<span class="unit">%</span></div>
        <div class="desc">Public Support</div>
        <div class="context">Of Americans willing to pay a small monthly fee to fund 988 crisis services</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# DATA STORY: FEE COMPARISON
# ===========================================================================
st.markdown("""
<div class="section-header">
    <div class="eyebrow">The Funding Picture</div>
    <h2>How States Are Funding 988</h2>
    <p>A small monthly telecom fee on phone bills can generate millions in dedicated crisis funding. Here's what states are charging.</p>
</div>
""", unsafe_allow_html=True)

# Fee bar chart
fee_states = [
    ("Vermont", 0.72, "#2D6A4F"),
    ("Colorado", 0.50, "#40916C"),
    ("Nevada", 0.35, "#52B788"),
    ("Maryland", 0.25, "#74C69D"),
    ("Washington", 0.24, "#74C69D"),
    ("Connecticut", 0.20, "#95D5B2"),
    ("Alabama", 0.18, "#95D5B2"),
    ("Minnesota", 0.12, "#B7E4C7"),
    ("Virginia", 0.12, "#B7E4C7"),
    ("California", 0.08, "#D8F3DC"),
]

max_fee = 0.80
bars_html = ""
for state, fee, color in fee_states:
    pct = (fee / max_fee) * 100
    bars_html += f"""
    <div class="fee-bar-item">
        <div class="fee-bar-state">{state}</div>
        <div class="fee-bar-track">
            <div class="fee-bar-fill" style="width:{pct}%;background:{color};">
                ${fee:.2f}
            </div>
        </div>
    </div>"""

st.markdown(f'<div class="fee-bar-section">{bars_html}</div>', unsafe_allow_html=True)

# Big callout
st.markdown("""
<div class="data-callout">
    <div class="big-stat">3 in 4</div>
    <div class="big-label">Americans are willing to pay a monthly fee to fund 988 crisis services</div>
    <div class="big-context">With more than a third willing to pay a fee greater than the highest existing fee ($0.72), there is strong public mandate for states to act.</div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# TIMELINE
# ===========================================================================
st.markdown("""
<div class="section-header">
    <div class="eyebrow">The Journey</div>
    <h2>988: From Concept to Crisis Lifeline</h2>
    <p>A look at the key milestones in building America's mental health crisis response system.</p>
</div>
""", unsafe_allow_html=True)

timeline_html = '<div class="timeline-container">'
for item in TIMELINE:
    cls = "milestone" if item["type"] == "milestone" else ""
    timeline_html += f"""
    <div class="timeline-item {cls}">
        <div class="t-date">{item['date']}</div>
        <div class="t-title">{item['title']}</div>
        <div class="t-desc">{item['description']}</div>
    </div>"""
timeline_html += "</div>"
st.markdown(timeline_html, unsafe_allow_html=True)


# ===========================================================================
# ADVOCATE SPOTLIGHTS
# ===========================================================================
st.markdown("""
<div class="section-header">
    <div class="eyebrow">Voices</div>
    <h2>From the Field</h2>
    <p>Leaders shaping the future of crisis response in their own words.</p>
</div>
""", unsafe_allow_html=True)

for adv in ADVOCATES:
    st.markdown(f"""
    <div class="advocate-card">
        <div class="advocate-accent" style="background:{adv['accent']}"></div>
        <div class="aq-text">{adv['quote']}</div>
        <div class="aq-name">{adv['name']}</div>
        <div class="aq-role">{adv['role']}</div>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================================
# POLICY RECOMMENDATION CARDS
# ===========================================================================
st.markdown("""
<div class="section-header">
    <div class="eyebrow">Policy Playbook</div>
    <h2>Five Moves States Can Make</h2>
    <p>Concrete policy recommendations backed by what's already working across the country.</p>
</div>
""", unsafe_allow_html=True)

for card in POLICY_CARDS:
    states_tags = "".join(
        f'<span class="ls-tag">{escape(s)}</span>' for s in card["leading_states"]
    )
    st.markdown(f"""
    <details class="policy-disclosure">
        <summary>
            <div class="p-icon">{escape(card['icon'])}</div>
            <div class="p-title">{escape(card['title'])}</div>
            <div class="p-subtitle">{escape(card['subtitle'])}</div>
            <div class="p-desc">{escape(card['description'])}</div>
            <div class="policy-stat-badge">
                <span class="ps-num">{escape(card['stat'])}</span>
                <span class="ps-label">{escape(card['stat_label'])}</span>
            </div>
        </summary>
        <div class="policy-body">
            <div class="leading-states">
                <span style="font-size:11px;color:#64748B;font-weight:500;margin-right:4px;">Leading:</span>
                {states_tags}
            </div>
            <div class="rec-box">
                <div class="rec-label">NAMI Recommendation</div>
                <div class="rec-text">{escape(card['recommendation'])}</div>
            </div>
        </div>
    </details>
    """, unsafe_allow_html=True)


# ===========================================================================
# STATE COMPARISON TOOL
# ===========================================================================
st.markdown("""
<div class="section-header">
    <div class="eyebrow">Compare</div>
    <h2>State by State</h2>
    <p>See how states stack up on 988 funding and crisis service infrastructure.</p>
</div>
""", unsafe_allow_html=True)

state_names = list(STATE_DATA.keys())
compare_chip_states = ["Colorado", "Washington", "Maryland", "Ohio", "Virginia", "Minnesota"]
if "compare_states" not in st.session_state:
    st.session_state["compare_states"] = compare_chip_states.copy()

selected_states = [s for s in st.session_state["compare_states"] if s in compare_chip_states]
if not selected_states:
    selected_states = compare_chip_states.copy()
st.session_state["compare_states"] = selected_states

selected_set = set(selected_states)
left_pad, chip_col, right_pad = st.columns([0.04, 0.92, 0.04])
with chip_col:
    cols = st.columns(len(compare_chip_states), gap="small")
    for idx, state in enumerate(compare_chip_states):
        is_selected = state in selected_set
        with cols[idx]:
            if st.button(
                state,
                key=f"cmp_state_{state}",
                type="primary" if is_selected else "secondary",
            ):
                if is_selected and len(selected_states) > 1:
                    selected_states = [s for s in selected_states if s != state]
                elif not is_selected:
                    selected_states = selected_states + [state]
                st.session_state["compare_states"] = selected_states
                rerun_app()

if selected_states:
    # Build comparison table
    rows_html = ""
    for s in selected_states:
        d = STATE_DATA[s]
        check = '<span class="check">✓</span>'
        cross = '<span class="cross">—</span>'
        rows_html += f"""
        <tr>
            <td class="state-name">{s}</td>
            <td><strong>{d['fee']}</strong></td>
            <td>{d['fee_start']}</td>
            <td>{d['est_revenue']}</td>
            <td>{check if d['trust_fund'] else cross}</td>
            <td>{check if d['mobile_crisis'] else cross}</td>
            <td>{check if d['crisis_stabilization'] else cross}</td>
            <td>{check if d['youth_services'] else cross}</td>
        </tr>"""

    st.markdown(f"""
    <table class="compare-table">
        <thead>
            <tr>
                <th>State</th>
                <th>988 Fee</th>
                <th>Fee Start</th>
                <th>Est. Revenue</th>
                <th>Trust Fund</th>
                <th>Mobile Crisis</th>
                <th>Stabilization</th>
                <th>Youth</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # Show highlights for selected states
    for s in selected_states:
        d = STATE_DATA[s]
        st.markdown(f"""
        <div style="
            background:#FFFFFF;
            border-radius:12px;
            padding:20px 24px;
            margin-bottom:12px;
            border-left:4px solid var(--green-600);
            box-shadow:0 1px 6px rgba(0,0,0,0.03);
        ">
            <div style="font-family:'Source Sans 3',sans-serif;font-size:14px;font-weight:700;color:var(--slate-900);margin-bottom:4px;">
                {s} <span style="font-weight:400;color:var(--slate-500);">({d['key_bill']})</span>
            </div>
            <div style="font-family:'Source Sans 3',sans-serif;font-size:14px;color:var(--slate-700);line-height:1.6;">
                {d['highlights']}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Select states above to compare their 988 and crisis service infrastructure.")


# ===========================================================================
# FOOTER CTA
# ===========================================================================
st.markdown("""
<div class="footer-cta">
    <h3>Every crisis deserves a<br>compassionate response.</h3>
    <p>Your voice can shape the future of mental health crisis care. Contact your legislators and advocate for 988 funding in your state.</p>
    <div class="cta-buttons">
        <a class="cta-btn primary" href="https://reimaginecrisis.org/map/" target="_blank">Explore the Legislation Map →</a>
        <a class="cta-btn secondary" href="https://www.nami.org/advocacy/" target="_blank">Get Involved with NAMI</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Crisis line note
st.markdown("""
<div style="text-align:center;padding:12px 0 40px;font-family:'Source Sans 3',sans-serif;font-size:14px;color:#64748B;">
    If you or someone you know is in crisis, <strong>call or text 988</strong> for free, confidential support 24/7.
</div>
""", unsafe_allow_html=True)
