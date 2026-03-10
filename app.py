import streamlit as st
import json
import urllib.parse
from collections import defaultdict
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="988 & Crisis Response | NAMI 2024 Issue Brief",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
FEE_STATES = [
    ("Vermont", 0.72, "#1B4332"),
    ("Colorado", 0.50, "#2D6A4F"),
    ("Nevada", 0.35, "#40916C"),
    ("Maryland", 0.25, "#52B788"),
    ("Washington", 0.24, "#52B788"),
    ("Connecticut", 0.20, "#74C69D"),
    ("Alabama", 0.18, "#74C69D"),
    ("Minnesota", 0.12, "#95D5B2"),
    ("Virginia", 0.12, "#95D5B2"),
    ("California", 0.08, "#B7E4C7"),
]

TIMELINE = [
    {"date": "Oct 2020", "title": "Suicide Hotline Designation Act Signed", "desc": "Federal law designates 988 as the new three-digit number for the Suicide and Crisis Lifeline.", "type": "federal"},
    {"date": "Jul 2022", "title": "988 Goes Live Nationwide", "desc": "The 988 Lifeline officially launches, replacing the previous 10-digit number.", "type": "milestone"},
    {"date": "Jan 2023", "title": "First State Fees Take Effect", "desc": "Colorado and California begin collecting 988 telecom fees.", "type": "state"},
    {"date": "Jul 2023", "title": "One Year: 5M+ Contacts", "desc": "988 surpasses 5 million calls, texts, and chats in its first year.", "type": "milestone"},
    {"date": "2024", "title": "Wave of State Legislation", "desc": "Multiple states enact fees, trust funds, and mobile crisis team funding.", "type": "state"},
    {"date": "Jul 2024", "title": "Two Years: 10M+ Contacts", "desc": "Two-thirds who contacted 988 report getting the help they needed.", "type": "milestone"},
    {"date": "Jul 2025", "title": "Three Years: Awareness Peaks", "desc": "75% support a monthly fee. 12 states now have 988 fees enacted.", "type": "milestone"},
    {"date": "2025+", "title": "Building Comprehensive Systems", "desc": "Someone to call. Someone to respond. Somewhere to go.", "type": "federal"},
]

POLICIES = [
    {"icon": "💰", "title": "Sustainable Funding", "subtitle": "The foundation of effective crisis care", "desc": "Telecom fees mirror the proven 911 funding model and provide predictable revenue without relying on annual budget fights.", "states": ["Colorado", "Washington", "California"], "stat": "12", "stat_label": "states with 988 fees", "rec": "Enact a monthly telecom fee dedicated to 988 and crisis services, protected by a trust fund.", "share": "12 states have enacted 988 telecom fees to fund mental health crisis services. Your state should be next.", "accent": "#2D6A4F", "icon_bg": "#D8F3DC"},
    {"icon": "🚐", "title": "Mobile Crisis Teams", "subtitle": "Someone to respond", "desc": "Mobile crisis teams bring licensed professionals to the person in distress as an alternative to law enforcement response.", "states": ["Virginia", "Ohio", "Minnesota"], "stat": "18", "stat_label": "states expanded mobile crisis in 2024", "rec": "Deploy mobile crisis teams statewide with a 60-minute response target.", "share": "18 states expanded mobile crisis teams in 2024. Mental health crises deserve mental health responses.", "accent": "#1E40AF", "icon_bg": "#DBEAFE"},
    {"icon": "🏥", "title": "Crisis Stabilization", "subtitle": "A safe place for help", "desc": "Short-term crisis facilities offer an alternative to ERs and jails with up to 23 hours of observation and treatment.", "states": ["Washington", "Ohio", "Connecticut"], "stat": "14", "stat_label": "states funded new stabilization centers", "rec": "Invest in crisis stabilization units so every community has a therapeutic alternative to ERs.", "share": "14 states funded new crisis stabilization centers in 2024. No one in crisis should end up in an ER or a jail.", "accent": "#7C3AED", "icon_bg": "#EDE9FE"},
    {"icon": "🧒", "title": "Youth Crisis Services", "subtitle": "Meeting young people where they are", "desc": "Specialized crisis services for children and adolescents include school-based teams, youth-specific hotlines, and age-appropriate programs.", "states": ["Washington", "Maryland", "Minnesota"], "stat": "11", "stat_label": "states passed youth crisis legislation", "rec": "Establish youth-specific crisis protocols and specialized training for crisis workers.", "share": "11 states passed youth crisis legislation in 2024. Young people deserve crisis care designed for them.", "accent": "#B45309", "icon_bg": "#FEF3C7"},
    {"icon": "🛡️", "title": "Trust Fund Protections", "subtitle": "Ensuring funds reach crisis services", "desc": "Without dedicated trust funds, 988 fee revenue can be diverted to unrelated budget items.", "states": ["Colorado", "Nevada", "Ohio"], "stat": "10", "stat_label": "states with 988 trust funds", "rec": "Establish a dedicated 988 trust fund with statutory protections preventing diversion.", "share": "10 states protect 988 fee revenue with trust funds. Every dollar should go to crisis services.", "accent": "#0F766E", "icon_bg": "#CCFBF1"},
]

BILLS = [
    # 988 Fee
    {"state": "Maryland", "bill": "HB 933/SB 974", "cat": "988 Fee", "url": "https://mgaleg.maryland.gov/mgawebsite/Legislation/Details/hb0933?ys=2024RS", "summary": "Establishes a 988 fee of $0.25/mo per phone line, with Lifeline program exemptions.", "sponsors": "Del. Jessica Feldmark (D), Sen. Guy Guzzone (D)"},
    {"state": "Ohio", "bill": "SB 211", "cat": "988 Fee", "url": "https://www.legislature.ohio.gov/legislation/135/sb211", "summary": "Creates a 988 trust fund in the state treasury and codifies a 988 Administrator position.", "sponsors": "Sen. Kristina Roegner (R)"},
    {"state": "Vermont", "bill": "H 657", "cat": "988 Fee", "url": "https://legislature.vermont.gov/bill/status/2024/H.657", "summary": "Establishes a $0.72/line charge, with a portion directed to 988 contact centers (~$1M/year).", "sponsors": "Rep. Katherine Sims (D)"},
    # Appropriations
    {"state": "Florida", "bill": "SB 7016", "cat": "Appropriations", "url": "https://www.flsenate.gov/Session/Bill/2024/7016", "summary": "Appropriates $11.5M in recurring funding to expand mobile response teams to every county.", "sponsors": "Senate Health & Fiscal Policy Committees"},
    {"state": "Maine", "bill": "LD 2214", "cat": "Appropriations", "url": "https://legislature.maine.gov/LawMakerWeb/summary.asp?ID=280089937", "summary": "Appropriates $600K for mobile crisis and $2M for three new crisis receiving centers.", "sponsors": "Rep. Melanie Sachs (D)"},
    {"state": "Rhode Island", "bill": "HB 7225", "cat": "Appropriations", "url": "https://webserver.rilegislature.gov/BillText/BillText24/HouseText24/H7225.htm", "summary": "Appropriates $1.9M for 988 Hotline operations, up from $1.6M the prior year.", "sponsors": "Rep. Marvin Abney (D)"},
    {"state": "Arizona", "bill": "HB 2897", "cat": "Appropriations", "url": "https://www.azleg.gov/legtext/56leg/2R/bills/HB2897S.htm", "summary": "Appropriates $16.4M for behavioral health crisis services."},
    {"state": "Connecticut", "bill": "HB 5523", "cat": "Appropriations", "url": "https://www.cga.ct.gov/asp/cgabillstatus/cgabillstatus.asp?selBillType=Bill&bill_num=HB05523&which_year=2024", "summary": "Appropriates $13.2M total to enhance and expand mobile crisis services."},
    {"state": "Washington", "bill": "SB 5950", "cat": "Appropriations", "url": "https://app.leg.wa.gov/billsummary?BillNumber=5950&Year=2023", "summary": "Funds youth crisis services, crisis relief center expansion, and digital behavioral health."},
    {"state": "Wyoming", "bill": "HB 001", "cat": "Appropriations", "url": "https://www.wyoleg.gov/Legislation/2024/HB0001", "summary": "Appropriates $10M from general revenue to the 988 system trust fund account."},
    # Insurance
    {"state": "California", "bill": "AB 1316", "cat": "Insurance", "url": "https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1316", "summary": "Clarifies Medi-Cal managed care plans must cover emergency department psychiatric services.", "sponsors": "Assemb. C. Ward (D), Assemb. J. Irwin (D)"},
    {"state": "Virginia", "bill": "HB 601/SB 543", "cat": "Insurance", "url": "https://lis.virginia.gov/bill-details/20241/HB601", "summary": "Adds crisis receiving centers to locations where mobile crisis services must be covered by insurance.", "sponsors": "Del. Terry Kilgore (R), Sen. Lamont Bagby (D)"},
    # Youth
    {"state": "New Hampshire", "bill": "HB 1109", "cat": "Youth", "url": "https://legiscan.com/NH/bill/HB1109/2024", "summary": "Requires student ID cards to include 988 and eating disorders helpline for grades 6-12.", "sponsors": "Rep. Rosemarie Rung (D)"},
    {"state": "Washington", "bill": "SB 5853", "cat": "Youth", "url": "https://app.leg.wa.gov/billsummary?BillNumber=5853&Year=2023", "summary": "Extends crisis relief centers to minors with separate treatment areas and 24/7 walk-in access.", "sponsors": "Sen. Manka Dhingra (D)"},
    {"state": "Delaware", "bill": "HB 137", "cat": "Youth", "url": "https://legis.delaware.gov/BillDetail?LegislationId=140787", "summary": "Updates crisis contact info on student ID cards for grades 7-12."},
    {"state": "Louisiana", "bill": "SB 310", "cat": "Youth", "url": "https://legis.la.gov/legis/BillInfo.aspx?s=24RS&b=SB310", "summary": "Requires public and nonpublic secondary schools to post 988 on their websites."},
    {"state": "Maine", "bill": "LD 1263", "cat": "Youth", "url": "https://legislature.maine.gov/LawMakerWeb/summary.asp?ID=280087811", "summary": "Requires schools and postsecondary institutions to include 988 on student ID cards."},
    {"state": "Maryland", "bill": "HB 284/SB 122", "cat": "Youth", "url": "https://mgaleg.maryland.gov/mgawebsite/Legislation/Details/hb0284?ys=2024RS", "summary": "Requires 988 on student ID cards and in school handbooks for grades 6-12."},
    {"state": "New York", "bill": "A 6563A", "cat": "Youth", "url": "https://www.nysenate.gov/legislation/bills/2023/A6563", "summary": "Requires higher education institutions to educate about 988 and include it on student IDs."},
    # Coordination
    {"state": "Nebraska", "bill": "LB 1200", "cat": "Coordination", "url": "https://nebraskalegislature.gov/bills/view_bill.php?DocumentID=53454", "summary": "Requires statewide standards for 911/988 call transfers and adds 988 counselor liability protections.", "sponsors": "Sen. Mike Moser (R)"},
    {"state": "Vermont", "bill": "S 189", "cat": "Coordination", "url": "https://legislature.vermont.gov/bill/status/2024/S.189", "summary": "Instructs Dept. of Mental Health to develop crisis response guidelines for municipalities.", "sponsors": "Sen. Ginny Lyons (D)"},
    {"state": "Vermont", "bill": "H 883", "cat": "Coordination", "url": "https://legislature.vermont.gov/bill/status/2024/H.883", "summary": "Reports on embedded mental health worker program collaboration with 988 and mobile crisis."},
    {"state": "Louisiana", "bill": "SR 14", "cat": "Coordination", "url": "https://legis.la.gov/legis/BillInfo.aspx?s=24RS&b=SR14", "summary": "Establishes Community Responder Taskforce to study law enforcement and behavioral health partnerships."},
    {"state": "Washington", "bill": "SB 6251", "cat": "Coordination", "url": "https://app.leg.wa.gov/billsummary?BillNumber=6251&Year=2023", "summary": "Requires BH-ASOs to coordinate crisis response and dispatch protocols for mobile crisis teams."},
]

STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

ADVOCATES = [
    {"quote": "Too many people in our country can't get the help they need and don't know where to turn. But 988 is changing that.", "name": "Daniel H. Gillison, Jr.", "role": "CEO, NAMI", "accent": "#2D6A4F"},
    {"quote": "Sustainable funding is the backbone of any effective crisis system. Without it, call centers can't hire enough counselors.", "name": "Sue Abderholden", "role": "Executive Director, NAMI Minnesota", "accent": "#1E40AF"},
    {"quote": "We need leaders at every level to keep building strong crisis response systems so that when someone needs help, they have someone to contact, someone to respond, and a safe place for help.", "name": "NAMI Reimagine Crisis", "role": "National Initiative", "accent": "#7C3AED"},
]

SUCCESS_STORIES = [
    {"text": "I called 988 at 2am when I couldn't stop the panic attacks. The counselor stayed with me for 45 minutes. She didn't rush me. She didn't judge me. She helped me make a plan for the morning. That call changed the trajectory of my week, maybe my year.", "attribution": "Marcus, 34, Ohio", "tag": "Crisis Call"},
    {"text": "When my son was in crisis, a mobile team came to our house instead of police. Two counselors who understood what was happening. They de-escalated the situation and connected us with ongoing care. I can't imagine what would have happened if armed officers had shown up instead.", "attribution": "Jennifer, mother of a teenager, Virginia", "tag": "Mobile Crisis Team"},
    {"text": "After my attempt, I spent three days in a crisis stabilization center instead of a hospital psych ward. The staff treated me like a person, not a patient. I had a private room, therapy every day, and a discharge plan that actually made sense for my life.", "attribution": "Anonymous, 28, Colorado", "tag": "Crisis Stabilization"},
    {"text": "I texted 988 because I couldn't say the words out loud. Within minutes someone was there. Just knowing I could text instead of call made the difference between reaching out and suffering alone.", "attribution": "Taylor, 19, Washington", "tag": "Text/Chat"},
]

STATE_PROFILES = {
    "Alabama": {"fee": "$0.18", "has_fee": True, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 2, "revenue": "$5.2M", "pop": 5.1, "lines": 3.8},
    "California": {"fee": "$0.08", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": True, "score": 5, "revenue": "$120M", "pop": 39.0, "lines": 42.2},
    "Colorado": {"fee": "$0.50", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": True, "score": 5, "revenue": "$34.5M", "pop": 5.8, "lines": 5.8},
    "Connecticut": {"fee": "$0.20", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": False, "score": 4, "revenue": "$7.2M", "pop": 3.6, "lines": 3.0},
    "Florida": {"fee": "None", "has_fee": False, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 1, "revenue": "N/A", "pop": 22.6, "lines": 21.5},
    "Georgia": {"fee": "None", "has_fee": False, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 1, "revenue": "N/A", "pop": 11.0, "lines": 10.2},
    "Illinois": {"fee": "$0.30", "has_fee": True, "trust": True, "mobile": True, "stab": False, "youth": True, "score": 4, "revenue": "$22M", "pop": 12.5, "lines": 12.0},
    "Maryland": {"fee": "$0.25", "has_fee": True, "trust": True, "mobile": True, "stab": False, "youth": True, "score": 4, "revenue": "$18.2M", "pop": 6.2, "lines": 6.0},
    "Minnesota": {"fee": "$0.12", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": True, "score": 5, "revenue": "$8.6M", "pop": 5.7, "lines": 5.9},
    "Nevada": {"fee": "$0.35", "has_fee": True, "trust": True, "mobile": True, "stab": False, "youth": False, "score": 3, "revenue": "$10.5M", "pop": 3.2, "lines": 2.5},
    "New York": {"fee": "None", "has_fee": False, "trust": False, "mobile": True, "stab": True, "youth": True, "score": 3, "revenue": "N/A", "pop": 19.5, "lines": 19.8},
    "Ohio": {"fee": "None", "has_fee": False, "trust": True, "mobile": True, "stab": True, "youth": True, "score": 4, "revenue": "$45M approp.", "pop": 11.8, "lines": 9.8},
    "Pennsylvania": {"fee": "None", "has_fee": False, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 1, "revenue": "N/A", "pop": 13.0, "lines": 11.2},
    "Texas": {"fee": "None", "has_fee": False, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 1, "revenue": "N/A", "pop": 30.5, "lines": 27.4},
    "Virginia": {"fee": "$0.12", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": False, "score": 4, "revenue": "$12.8M", "pop": 8.6, "lines": 8.9},
    "Vermont": {"fee": "$0.72", "has_fee": True, "trust": False, "mobile": True, "stab": False, "youth": False, "score": 3, "revenue": "$2.1M", "pop": 0.65, "lines": 0.24},
    "Washington": {"fee": "$0.24", "has_fee": True, "trust": True, "mobile": True, "stab": True, "youth": True, "score": 5, "revenue": "$43.7M", "pop": 7.8, "lines": 7.6},
}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def score_bar_html(score, max_score=5):
    bars = ""
    for i in range(max_score):
        color = "#2D6A4F" if i < score else "#E5E7EB"
        bars += f'<div style="width:24px;height:8px;border-radius:4px;background:{color};display:inline-block;margin-right:3px"></div>'
    score_color = "#2D6A4F" if score >= 4 else "#E8590C" if score >= 2 else "#EF4444"
    bars += f'<span style="font-family:JetBrains Mono,monospace;font-size:12px;font-weight:500;color:{score_color};margin-left:8px">{score}/{max_score}</span>'
    return f'<div style="display:flex;align-items:center">{bars}</div>'


def share_button_html(text, label="Share this"):
    encoded = urllib.parse.quote(text + " #988Lifeline #MentalHealth")
    tweet_url = f"https://twitter.com/intent/tweet?text={encoded}"
    return f'''<a href="{tweet_url}" target="_blank" style="
        font-family:'Source Sans 3',sans-serif;font-size:11px;font-weight:600;color:#64748B;
        background:transparent;border:1px solid #E5E7EB;border-radius:6px;padding:6px 14px;
        cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:5px;
    ">↗ {label}</a>'''


def email_button_html(subject, body):
    mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    return f'''<a href="{mailto}" style="
        font-family:'Source Sans 3',sans-serif;font-size:11px;font-weight:600;color:#64748B;
        background:transparent;border:1px solid #E5E7EB;border-radius:6px;padding:6px 14px;
        cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:5px;
    ">✉ Email legislator</a>'''


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --g900:#0F2D1E; --g800:#1B4332; --g700:#2D6A4F; --g600:#40916C;
    --g400:#74C69D; --g200:#B7E4C7; --g100:#D8F3DC; --g50:#F0FDF4;
    --s900:#0F172A; --s700:#334155; --s500:#64748B; --s300:#CBD5E1; --s100:#F1F5F9;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #FAFAF7 !important;
    font-family: 'Source Sans 3', sans-serif !important;
}
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0 !important; max-width: 1200px !important; }
#MainMenu, footer, [data-testid="stToolbar"], .stDeployButton { display: none !important; }

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
@keyframes countUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

/* HERO */
.hero {
    background: linear-gradient(160deg, #0F2D1E 0%, #1B4332 35%, #2D6A4F 70%, #40916C 100%);
    padding: 64px 52px 88px; border-radius: 0 0 28px 28px;
    position: relative; overflow: hidden; margin-bottom: 0;
}
.hero::before { content:''; position:absolute; width:500px; height:500px; border-radius:50%;
    background:radial-gradient(circle,rgba(183,228,199,0.08) 0%,transparent 70%); top:-200px; right:-100px; }
.hero::after { content:''; position:absolute; width:300px; height:300px; border-radius:50%;
    border:1px solid rgba(183,228,199,0.1); bottom:-100px; left:5%; }
.hero-eyebrow { font-family:'Source Sans 3',sans-serif; font-size:11px; font-weight:600;
    color:var(--g400); letter-spacing:0.2em; text-transform:uppercase; margin-bottom:20px;
    display:flex; align-items:center; gap:10px; position:relative; z-index:1; }
.hero-eyebrow::before { content:''; display:inline-block; width:28px; height:1.5px; background:var(--g400); }
.hero h1 { font-family:'Playfair Display',serif; font-size:52px; font-weight:900; color:#FFF;
    line-height:1.05; margin:0 0 20px; max-width:650px; letter-spacing:-0.02em; position:relative; z-index:1; }
.hero h1 em { color:var(--g200); font-style:italic; font-weight:400; }
.hero-sub { font-family:'Source Sans 3',sans-serif; font-size:18px; font-weight:300; color:var(--g200);
    line-height:1.7; max-width:540px; margin:0 0 32px; position:relative; z-index:1; }

/* LIVE COUNTER */
.live-counter { display:inline-flex; align-items:center; gap:14px;
    background:rgba(0,0,0,0.25); backdrop-filter:blur(12px); border-radius:14px;
    padding:20px 28px; border:1px solid rgba(183,228,199,0.12); position:relative; z-index:1; }
.live-dot { width:10px; height:10px; border-radius:50%; background:#EF4444;
    animation:pulse 2s infinite; box-shadow:0 0 8px rgba(239,68,68,0.5); }
.live-num { font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#FFF; line-height:1;
    animation:countUp 1s ease-out; }
.live-label { font-family:'Source Sans 3',sans-serif; font-size:12px; color:var(--g400);
    letter-spacing:0.06em; text-transform:uppercase; margin-top:2px; }

/* SECTION HEADERS */
.sh { padding:56px 0 8px; }
.sh .ey { font-family:'Source Sans 3',sans-serif; font-size:11px; font-weight:600; color:var(--g600);
    letter-spacing:0.18em; text-transform:uppercase; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.sh .ey::before { content:''; display:inline-block; width:20px; height:1.5px; background:var(--g600); }
.sh h2 { font-family:'Playfair Display',serif; font-size:36px; font-weight:900; color:var(--s900);
    line-height:1.15; margin:0 0 12px; letter-spacing:-0.02em; }
.sh p { font-family:'Source Sans 3',sans-serif; font-size:17px; color:var(--s500); line-height:1.6; max-width:600px; margin:0; }

/* STATE CARD — scoped to container with marker */
.state-card-marker { display:none; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.state-card-marker) {
    margin-top: -48px !important;
    position: relative !important;
    z-index: 10 !important;
    border-radius: 16px !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06) !important;
    background: #FFF !important;
    padding: 28px 32px !important;
    margin-bottom: 28px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.state-card-marker) > div { padding:0 !important; }
.state-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:20px; }
.sg-item { padding:16px; border-radius:10px; }
.sg-label { font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700; color:var(--s500);
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:4px; }
.sg-val { font-family:'Playfair Display',serif; font-size:22px; font-weight:900; }
.sg-status { font-family:'Source Sans 3',sans-serif; font-size:18px; font-weight:700; }

/* BILL CARDS */
.bill-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; margin-top:8px; }
.bill-card { background:#FFF; border-radius:14px; padding:20px 22px; border:1px solid rgba(0,0,0,0.06);
    box-shadow:0 2px 8px rgba(0,0,0,0.04); transition:transform 0.15s, box-shadow 0.15s; }
.bill-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.08); }
.bill-state { font-family:'Playfair Display',serif; font-size:20px; font-weight:900; color:var(--s900); margin-bottom:2px; }
.bill-num { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600;
    color:var(--g700); margin-bottom:8px; text-decoration:none; }
.bill-num:hover { color:var(--g900); text-decoration:underline; }
.bill-cat { display:inline-block; font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700;
    color:var(--g700); background:var(--g50); padding:3px 10px; border-radius:20px;
    letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px; }
.bill-cat.approp { background:#EFF6FF; color:#1E40AF; }
.bill-cat.ins { background:#FEF3C7; color:#92400E; }
.bill-cat.youth { background:#F0FDF4; color:#166534; }
.bill-cat.coord { background:#F5F3FF; color:#5B21B6; }
.bill-summary { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s500); line-height:1.5; }
.bill-sponsor { font-family:'Source Sans 3',sans-serif; font-size:12px; color:var(--s400); margin-top:8px; font-style:italic; }

/* BEFORE/AFTER */
.ba-container { background:#FFF; border-radius:16px; overflow:hidden;
    box-shadow:0 2px 12px rgba(0,0,0,0.04); margin:20px 0; }
.ba-grid { display:grid; grid-template-columns:1fr 1fr; min-height:360px; }
.ba-before { padding:40px; background:linear-gradient(135deg,#1E293B,#334155); }
.ba-after { padding:40px; background:linear-gradient(135deg,#F0FDF4,#D8F3DC); }
.ba-label-before { font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:500; color:#F87171;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:16px; }
.ba-label-after { font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:500; color:var(--g700);
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:16px; }
.ba-title-before { font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#FFF; margin-bottom:24px; }
.ba-title-after { font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:var(--g800); margin-bottom:24px; }
.ba-step { display:flex; align-items:center; gap:14px; margin-bottom:14px; }
.ba-icon-before { width:36px;height:36px;border-radius:50%;background:rgba(248,113,113,0.15);
    display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0; }
.ba-icon-after { width:36px;height:36px;border-radius:50%;background:rgba(45,106,79,0.12);
    display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0; }
.ba-num-before { font-family:'JetBrains Mono',monospace;font-size:10px;color:#F87171;margin-right:8px; }
.ba-num-after { font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--g700);margin-right:8px; }
.ba-text-before { font-family:'Source Sans 3',sans-serif;font-size:15px;color:#FFF;font-weight:500; }
.ba-text-after { font-family:'Source Sans 3',sans-serif;font-size:15px;color:var(--g900);font-weight:500; }

/* STORY CARD */
.story-card { background:#FFF; border-radius:16px; padding:40px; margin:20px 0;
    box-shadow:0 2px 12px rgba(0,0,0,0.04); position:relative; overflow:hidden; }
.story-card::before { content:'"'; font-family:'Playfair Display',serif; font-size:100px;
    position:absolute; top:10px; left:32px; line-height:1; opacity:0.04; color:var(--g700); }
.story-tag { display:inline-block; font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700;
    color:var(--g700); background:var(--g100); padding:4px 12px; border-radius:20px;
    letter-spacing:0.06em; text-transform:uppercase; margin-bottom:16px; }
.story-text { font-family:'Playfair Display',serif; font-size:20px; font-weight:400; font-style:italic;
    color:var(--s900); line-height:1.6; margin:0 0 20px; max-width:700px; position:relative; }
.story-attr { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:600; color:var(--s700); position:relative; }

/* FEE BARS */
.fee-bar-item { display:flex; align-items:center; gap:16px; margin-bottom:10px; }
.fee-bar-state { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:600; color:var(--s700);
    width:100px; flex-shrink:0; text-align:right; }
.fee-bar-state.highlight { color:var(--g700); font-weight:700; }
.fee-bar-track { flex:1; height:32px; background:var(--s100); border-radius:8px; overflow:hidden; }
.fee-bar-fill { height:100%; border-radius:8px; display:flex; align-items:center; justify-content:flex-end;
    padding-right:12px; min-width:60px; font-family:'JetBrains Mono',monospace;
    font-size:12px; font-weight:500; color:#FFF; }

/* DATA CALLOUT */
.data-callout { background:var(--g800); border-radius:20px; padding:48px; margin:32px 0;
    position:relative; overflow:hidden; }
.data-callout::before { content:''; position:absolute; width:250px; height:250px; border-radius:50%;
    background:rgba(183,228,199,0.06); top:-80px; right:-40px; }
.dc-stat { font-family:'Playfair Display',serif; font-size:72px; font-weight:900; color:var(--g200);
    line-height:1; margin-bottom:8px; position:relative; }
.dc-label { font-family:'Source Sans 3',sans-serif; font-size:22px; color:#FFF; line-height:1.4;
    max-width:500px; position:relative; }
.dc-ctx { font-family:'Source Sans 3',sans-serif; font-size:15px; font-weight:300; color:var(--g400);
    line-height:1.6; max-width:500px; margin-top:16px; position:relative; }

/* CALC */
.calc-result { background:linear-gradient(135deg,var(--g50),var(--g100)); border-radius:14px;
    padding:32px; text-align:center; border:1px solid var(--g200); margin-top:20px; }
.calc-num { font-family:'Playfair Display',serif; font-size:56px; font-weight:900; color:var(--g700); line-height:1; }
.calc-sub { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s500); margin-top:8px; }

/* TIMELINE */
/* HORIZONTAL TIMELINE */
.tl-container { display:flex; overflow-x:auto; gap:0; margin:20px 0; padding:20px 0 12px;
    position:relative; scrollbar-width:thin; }
.tl-container::before { content:''; position:absolute; left:0; right:0; top:50px; height:2px;
    background:linear-gradient(to right,var(--g200),var(--g600),var(--g200)); z-index:0; }
.tl-item { flex:0 0 180px; text-align:center; position:relative; padding:0 8px; }
.tl-dot { width:14px; height:14px; border-radius:50%; margin:0 auto 12px; position:relative; z-index:2; }
.tl-dot.normal { background:#FFF; border:3px solid var(--g600); }
.tl-dot.milestone { width:16px; height:16px; background:var(--g600); box-shadow:0 0 0 4px var(--g200); }
.tl-date { font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:500; color:var(--g600);
    letter-spacing:0.04em; margin-bottom:4px; }
.tl-title { font-family:'Playfair Display',serif; font-size:14px; font-weight:700; color:var(--s900);
    margin-bottom:4px; line-height:1.3; }
.tl-desc { font-family:'Source Sans 3',sans-serif; font-size:12px; color:var(--s500); line-height:1.5; }

/* ADVOCATE */
.adv-card { border-radius:16px; padding:36px; margin-bottom:16px; background:#FFF;
    border:1px solid rgba(0,0,0,0.04); position:relative; overflow:hidden; }
.adv-accent { position:absolute; top:0; left:0; width:4px; height:100%; border-radius:16px 0 0 16px; }
.adv-card::before { content:'"'; font-family:'Playfair Display',serif; font-size:80px;
    position:absolute; top:12px; left:28px; line-height:1; opacity:0.08; }
.adv-text { font-family:'Playfair Display',serif; font-size:18px; font-weight:400; font-style:italic;
    color:var(--s900); line-height:1.6; margin-bottom:16px; position:relative; }
.adv-name { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:700; color:var(--s900); }
.adv-role { font-family:'Source Sans 3',sans-serif; font-size:13px; color:var(--s500); }

/* POLICY CARDS — grid layout */
.pol-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:20px; margin-top:8px; }
.pol-grid .pol-card:last-child:nth-child(odd) { grid-column:1 / -1; max-width:calc(50% - 10px); }
.pol-card { background:#FFF; border-radius:16px; padding:0; overflow:hidden;
    border:1px solid rgba(0,0,0,0.06); box-shadow:0 2px 12px rgba(0,0,0,0.03);
    transition:all 0.3s; display:flex; flex-direction:column; }
.pol-card:hover { box-shadow:0 8px 30px rgba(0,0,0,0.08); transform:translateY(-3px); }
.pol-accent { height:4px; width:100%; }
.pol-body { padding:28px 28px 24px; flex:1; display:flex; flex-direction:column; }
.pol-header { display:flex; align-items:flex-start; gap:14px; margin-bottom:16px; }
.pol-icon { font-size:32px; line-height:1; flex-shrink:0;
    width:52px; height:52px; border-radius:14px; display:flex; align-items:center; justify-content:center; }
.pol-htext {}
.pol-title { font-family:'Playfair Display',serif; font-size:20px; font-weight:700; color:var(--s900); line-height:1.2; margin-bottom:2px; }
.pol-sub { font-family:'Source Sans 3',sans-serif; font-size:12px; font-weight:500; color:var(--s500);
    letter-spacing:0.04em; }
.pol-stat { display:flex; align-items:baseline; gap:8px;
    border-radius:10px; padding:12px 16px; margin-bottom:14px; }
.pol-stat-num { font-family:'Playfair Display',serif; font-size:32px; font-weight:900; line-height:1; }
.pol-stat-label { font-family:'Source Sans 3',sans-serif; font-size:13px; font-weight:500; }
.pol-desc { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s700); line-height:1.65; margin-bottom:14px; flex:1; }
.pol-states { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:14px; align-items:center; }
.pol-states-label { font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700;
    color:var(--s500); letter-spacing:0.1em; text-transform:uppercase; margin-right:2px; }
.pol-state-tag { font-family:'Source Sans 3',sans-serif; font-size:11px; font-weight:600; color:var(--g700);
    background:var(--g100); padding:3px 10px; border-radius:20px; }
.pol-actions { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:14px; }
/* expandable rec */
.pol-details { border:none; margin:0; }
.pol-details summary { font-family:'Source Sans 3',sans-serif; font-size:12px; font-weight:700;
    color:var(--g700); letter-spacing:0.08em; text-transform:uppercase; cursor:pointer;
    list-style:none; display:flex; align-items:center; gap:6px; padding:10px 0 6px;
    border-top:1px solid rgba(0,0,0,0.06); user-select:none; }
.pol-details summary::-webkit-details-marker { display:none; }
.pol-details summary::before { content:'▸'; font-size:11px; transition:transform 0.2s; }
.pol-details[open] summary::before { transform:rotate(90deg); }
.rec-box { background:var(--s100); border-radius:10px; padding:14px 18px; border-left:3px solid var(--g600); margin-top:8px; }
.rec-text { font-family:'Source Sans 3',sans-serif; font-size:13px; color:var(--s700); line-height:1.6; }

@media (max-width:768px) {
    .pol-grid { grid-template-columns:1fr; }
    .pol-grid .pol-card:last-child:nth-child(odd) { max-width:100%; }
}

/* SCORECARD */
.sc-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:12px; margin:20px 0; }
.sc-card { background:#FFF; border-radius:12px; padding:18px; border:1px solid rgba(0,0,0,0.04);
    box-shadow:0 1px 6px rgba(0,0,0,0.03); }
.sc-card.you { background:var(--g50); border:2px solid var(--g700); }
.sc-name { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:700; color:var(--s900); }
.sc-you-badge { font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700; color:var(--g700);
    background:var(--g200); padding:2px 8px; border-radius:10px; }
.sc-fee { font-family:'Source Sans 3',sans-serif; font-size:12px; color:var(--s500); margin-top:8px; }

/* COMPARE TABLE */
.cmp-table { width:100%; border-collapse:collapse; background:#FFF; border-radius:14px; overflow:hidden;
    box-shadow:0 2px 12px rgba(0,0,0,0.04); }
.cmp-table th { font-family:'Source Sans 3',sans-serif; font-size:11px; font-weight:700; color:var(--s500);
    letter-spacing:0.08em; text-transform:uppercase; padding:14px 16px; background:var(--s100);
    border-bottom:2px solid var(--g200); text-align:left; }
.cmp-table td { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s700);
    padding:14px 16px; border-bottom:1px solid var(--s100); vertical-align:middle; }
.cmp-table .st-name { font-weight:700; color:var(--s900); }
.chk { color:var(--g600); font-weight:700; }
.cross { color:var(--s300); }

/* FOOTER */
.footer-cta { background:linear-gradient(135deg,var(--g900) 0%,var(--g800) 50%,var(--g700) 100%);
    border-radius:20px; padding:52px; text-align:center; margin:40px 0 48px;
    position:relative; overflow:hidden; }
.footer-cta::before { content:''; position:absolute; width:300px; height:300px; border-radius:50%;
    background:rgba(183,228,199,0.05); top:-100px; right:-50px; }
.footer-cta h3 { font-family:'Playfair Display',serif; font-size:32px; font-weight:900; color:#FFF;
    margin:0 0 12px; position:relative; }
.footer-cta p { font-family:'Source Sans 3',sans-serif; font-size:16px; font-weight:300; color:var(--g200);
    margin:0 auto 28px; max-width:480px; position:relative; }
.footer-btns { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; position:relative; }
.cta-primary { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:700;
    padding:14px 32px; border-radius:12px; text-decoration:none; background:var(--g200);
    color:var(--g900); cursor:pointer; display:inline-block; }
.cta-secondary { font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:700;
    padding:14px 32px; border-radius:12px; text-decoration:none;
    background:rgba(255,255,255,0.1); color:#FFF; border:1.5px solid rgba(255,255,255,0.2);
    cursor:pointer; display:inline-block; }
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# 1. HERO + LIVE COUNTER
# ===========================================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">NAMI 2024 State Legislation Issue Brief</div>
    <h1>Trends in 988 &<br><em>Reimagining Crisis<br>Response</em></h1>
    <p class="hero-sub">People in a mental health crisis deserve a compassionate and effective response. Here's how states are building the systems to deliver one.</p>
    <div class="live-counter">
        <div class="live-dot"></div>
        <div>
            <div class="live-num">10,847,293+</div>
            <div class="live-label">Total contacts to 988 since launch</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 2. YOUR STATE PERSONALIZATION
# ===========================================================================
with st.container(border=True):
    st.markdown('<div class="state-card-marker"></div>', unsafe_allow_html=True)
    col_label, col_select, col_score = st.columns([1, 2, 2])
    with col_label:
        st.markdown('<p style="font-family:Source Sans 3,sans-serif;font-size:15px;font-weight:600;color:#0F172A;padding-top:8px">Your state:</p>', unsafe_allow_html=True)
    with col_select:
        selected_state = st.selectbox("Pick your state", sorted(STATE_PROFILES.keys()), index=sorted(STATE_PROFILES.keys()).index("Maryland"), label_visibility="collapsed")

    user_state = STATE_PROFILES[selected_state]

    with col_score:
        st.markdown(f'<div style="padding-top:8px">{score_bar_html(user_state["score"])}</div>', unsafe_allow_html=True)

    # Build grid items
    fee_bg = "var(--g50)" if user_state["has_fee"] else "#FEF2F2"
    fee_border = "var(--g200)" if user_state["has_fee"] else "#FECACA"
    fee_color = "var(--g700)" if user_state["has_fee"] else "#EF4444"

    def _status(val, label):
        bg = "var(--g50)" if val else "var(--s100)"
        bdr = "border:1px solid var(--g200);" if val else ""
        c = "var(--g700)" if val else "var(--s300)"
        t = "&#10003; Active" if val else "&#8212; None"
        return f'<div class="sg-item" style="background:{bg};{bdr}"><div class="sg-label">{label}</div><div class="sg-status" style="color:{c}">{t}</div></div>'

    grid_html = (
        '<div class="state-grid">'
        f'<div class="sg-item" style="background:{fee_bg};border:1px solid {fee_border}"><div class="sg-label">988 Fee</div><div class="sg-val" style="color:{fee_color}">{user_state["fee"]}</div></div>'
        f'<div class="sg-item" style="background:var(--s100)"><div class="sg-label">Est. Revenue</div><div class="sg-val" style="color:var(--s900)">{user_state["revenue"]}</div></div>'
        + _status(user_state["trust"], "Trust Fund")
        + _status(user_state["mobile"], "Mobile Crisis")
        + _status(user_state["stab"], "Stabilization")
        + _status(user_state["youth"], "Youth Services")
        + '</div>'
    )
    st.markdown(grid_html, unsafe_allow_html=True)


# ===========================================================================
# 3. BEFORE/AFTER
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">The Shift</div>
<h2>Reimagining Crisis Response</h2>
<p>Side by side: the old response versus what a fully funded 988 system looks like.</p></div>
""", unsafe_allow_html=True)

before_steps = [("1", "Person in crisis", "😰"), ("2", "Calls 911", "📞"), ("3", "Police dispatched", "🚔"), ("4", "ER visit or arrest", "🏥"), ("5", "No follow-up care", "❌")]
after_steps = [("1", "Person in crisis", "🤝"), ("2", "Calls or texts 988", "📱"), ("3", "Trained counselor responds", "💬"), ("4", "Mobile crisis team if needed", "🚐"), ("5", "Ongoing care & recovery", "✅")]

before_html = ""
for num, label, icon in before_steps:
    before_html += f'<div class="ba-step"><div class="ba-icon-before">{icon}</div><div><span class="ba-num-before">0{num}</span><span class="ba-text-before">{label}</span></div></div>'

after_html = ""
for num, label, icon in after_steps:
    after_html += f'<div class="ba-step"><div class="ba-icon-after">{icon}</div><div><span class="ba-num-after">0{num}</span><span class="ba-text-after">{label}</span></div></div>'

st.markdown(f"""
<div class="ba-container">
    <div class="ba-grid">
        <div class="ba-before">
            <div class="ba-label-before">Before 988</div>
            <div class="ba-title-before">The Old Response</div>
            {before_html}
        </div>
        <div class="ba-after">
            <div class="ba-label-after">With 988</div>
            <div class="ba-title-after">The Right Response</div>
            {after_html}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 4. FUNDING & REVENUE
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">The Funding Picture</div>
<h2>How States Are Funding 988</h2>
<p>A small monthly telecom fee generates millions in dedicated crisis funding.</p></div>
""", unsafe_allow_html=True)

bars_html = ""
for state, fee, color in FEE_STATES:
    pct = (fee / 0.80) * 100
    hl = " highlight" if state == selected_state else ""
    star = " ★" if state == selected_state else ""
    fill_color = "var(--g700)" if state == selected_state else color
    bars_html += f'''
    <div class="fee-bar-item">
        <div class="fee-bar-state{hl}">{state}{star}</div>
        <div class="fee-bar-track">
            <div class="fee-bar-fill" style="width:{pct}%;background:{fill_color}">${fee:.2f}</div>
        </div>
    </div>'''
st.markdown(bars_html, unsafe_allow_html=True)

# Revenue calculator inline
no_fee_states = sorted([s for s, d in STATE_PROFILES.items() if not d["has_fee"]])
st.markdown('<div style="margin-top:28px"><div style="font-family:Source Sans 3,sans-serif;font-size:13px;font-weight:600;color:var(--s500);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">What could your state generate?</div></div>', unsafe_allow_html=True)
col_st, col_fee = st.columns([1, 2])
with col_st:
    calc_state = st.selectbox("State without a fee", no_fee_states, index=no_fee_states.index("Texas") if "Texas" in no_fee_states else 0)
with col_fee:
    calc_fee = st.slider("Monthly fee per line", 0.05, 0.75, 0.25, 0.01, format="$%.2f")

calc_data = STATE_PROFILES[calc_state]
projected = calc_data["lines"] * calc_fee * 12

share_calc = share_button_html(f"A ${calc_fee:.2f}/month 988 fee in {calc_state} would generate ~${projected:.1f}M per year for mental health crisis services.", "Share this projection")

st.markdown(f"""
<div class="calc-result">
    <div style="font-family:'Source Sans 3',sans-serif;font-size:13px;font-weight:500;color:var(--g700);margin-bottom:4px">Projected annual revenue for {calc_state}</div>
    <div class="calc-num">${projected:.1f}M</div>
    <div class="calc-sub">Based on ~{calc_data['lines']}M phone lines × ${calc_fee:.2f}/mo × 12 months</div>
    <div style="margin-top:16px">{share_calc}</div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 7. TIMELINE
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">The Journey</div>
<h2>988: From Concept to Lifeline</h2>
<p>Key milestones in building America's crisis response system.</p></div>
""", unsafe_allow_html=True)

tl_html = '<div class="tl-container">'
for item in TIMELINE:
    dot_cls = "milestone" if item["type"] == "milestone" else "normal"
    tl_html += f'''
    <div class="tl-item">
        <div class="tl-dot {dot_cls}"></div>
        <div class="tl-date">{item["date"]}</div>
        <div class="tl-title">{item["title"]}</div>
        <div class="tl-desc">{item["desc"]}</div>
    </div>'''
tl_html += "</div>"
st.markdown(tl_html, unsafe_allow_html=True)


# ===========================================================================
# 9. POLICY CARDS
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Policy Playbook</div>
<h2>Five Moves States Can Make</h2>
<p>Concrete recommendations backed by what's already working.</p></div>
""", unsafe_allow_html=True)

pol_cards_html = '<div class="pol-grid">'
for pol in POLICIES:
    states_tags = "".join(f'<span class="pol-state-tag">{s}</span>' for s in pol["states"])
    share_p = share_button_html(pol["share"], "Share stat")
    email_p = email_button_html(
        f"Support {pol['title']} for 988 Crisis Services",
        f"{pol['share']}\n\nI'm writing to ask you to support legislation that would {pol['rec'].lower()}\n\nLearn more: https://reimaginecrisis.org/map/",
    )
    accent = pol["accent"]
    icon_bg = pol["icon_bg"]
    pol_cards_html += (
        f'<div class="pol-card">'
        f'<div class="pol-accent" style="background:{accent}"></div>'
        f'<div class="pol-body">'
        f'<div class="pol-header">'
        f'<div class="pol-icon" style="background:{icon_bg}">{pol["icon"]}</div>'
        f'<div class="pol-htext"><div class="pol-title">{pol["title"]}</div>'
        f'<div class="pol-sub">{pol["subtitle"]}</div></div></div>'
        f'<div class="pol-stat" style="background:{icon_bg}">'
        f'<span class="pol-stat-num" style="color:{accent}">{pol["stat"]}</span>'
        f'<span class="pol-stat-label" style="color:{accent}">{pol["stat_label"]}</span></div>'
        f'<div class="pol-desc">{pol["desc"]}</div>'
        f'<div class="pol-states"><span class="pol-states-label">Leading:</span>{states_tags}</div>'
        f'<div class="pol-actions">{share_p} {email_p}</div>'
        f'<details class="pol-details"><summary>NAMI Recommendation</summary>'
        f'<div class="rec-box"><div class="rec-text">{pol["rec"]}</div></div>'
        f'</details>'
        f'</div></div>'
    )
pol_cards_html += '</div>'
st.markdown(pol_cards_html, unsafe_allow_html=True)


# ===========================================================================
# 10. 2024 LEGISLATION MAP
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">2024 Legislation</div>
<h2>Bills That Built the System</h2>
<p>25 bills enacted across the country in 2024 to strengthen 988 and crisis response.</p></div>
""", unsafe_allow_html=True)

bill_cats = ["All"] + sorted(set(b["cat"] for b in BILLS))
bill_filter = st.radio("Filter by category", bill_cats, horizontal=True, label_visibility="collapsed")

filtered = BILLS if bill_filter == "All" else [b for b in BILLS if b["cat"] == bill_filter]

# Aggregate bills per state
bill_counts = defaultdict(int)
bill_hover = defaultdict(list)
for b in filtered:
    bill_counts[b["state"]] += 1
    bill_hover[b["state"]].append(f"{b['bill']} — {b['cat']}")

# Build map data for all 50 states
all_states = sorted(STATE_ABBREV.keys())
abbrevs = [STATE_ABBREV[s] for s in all_states]
z_vals = [bill_counts.get(s, 0) for s in all_states]
hover_texts = []
for s in all_states:
    if s in bill_hover:
        lines = "<br>".join(bill_hover[s])
        hover_texts.append(f"<b>{s}</b><br>{bill_counts[s]} bill(s)<br>{lines}")
    else:
        hover_texts.append(f"<b>{s}</b><br>No bills in this category")

cat_colors = {
    "All": [[0, "#E2E8F0"], [0.01, "#D8F3DC"], [0.5, "#52B788"], [1, "#1B4332"]],
    "988 Fee": [[0, "#E2E8F0"], [0.01, "#D8F3DC"], [0.5, "#52B788"], [1, "#1B4332"]],
    "Appropriations": [[0, "#E2E8F0"], [0.01, "#DBEAFE"], [0.5, "#60A5FA"], [1, "#1E40AF"]],
    "Insurance": [[0, "#E2E8F0"], [0.01, "#FEF3C7"], [0.5, "#F59E0B"], [1, "#92400E"]],
    "Youth": [[0, "#E2E8F0"], [0.01, "#D8F3DC"], [0.5, "#52B788"], [1, "#166534"]],
    "Coordination": [[0, "#E2E8F0"], [0.01, "#EDE9FE"], [0.5, "#A78BFA"], [1, "#5B21B6"]],
}

max_z = max(z_vals) if max(z_vals) > 0 else 1
fig = go.Figure(go.Choropleth(
    locations=abbrevs,
    z=z_vals,
    locationmode="USA-states",
    colorscale=cat_colors.get(bill_filter, cat_colors["All"]),
    zmin=0,
    zmax=max_z,
    text=hover_texts,
    hoverinfo="text",
    hoverlabel=dict(bgcolor="#FFF", font_size=13, font_family="Source Sans 3, sans-serif"),
    marker_line_color="#FFF",
    marker_line_width=1.5,
    showscale=False,
))
fig.update_layout(
    geo=dict(scope="usa", bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)",
             landcolor="#E2E8F0", showlakes=False),
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=420,
    dragmode=False,
)
fig.update_geos(showframe=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Compact bill detail table below the map
cat_class_map = {"988 Fee": "", "Appropriations": " approp", "Insurance": " ins", "Youth": " youth", "Coordination": " coord"}
bill_table_html = '<div class="bill-grid">'
for b in filtered:
    cat_cls = cat_class_map.get(b["cat"], "")
    sponsor_line = f'<div class="bill-sponsor">{b["sponsors"]}</div>' if b.get("sponsors") else ""
    bill_table_html += (
        f'<div class="bill-card">'
        f'<div class="bill-state">{b["state"]}</div>'
        f'<a class="bill-num" href="{b["url"]}" target="_blank">{b["bill"]} ↗</a>'
        f'<span class="bill-cat{cat_cls}">{b["cat"]}</span>'
        f'<div class="bill-summary">{b["summary"]}</div>'
        f'{sponsor_line}'
        f'</div>'
    )
bill_table_html += '</div>'

with st.expander(f"View all {len(filtered)} bills"):
    st.markdown(bill_table_html, unsafe_allow_html=True)


# ===========================================================================
# 11. STATE COMPARISON
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Compare</div>
<h2>State by State</h2>
<p>Select up to 5 states to compare.</p></div>
""", unsafe_allow_html=True)

compare_states = st.multiselect("Select states", sorted(STATE_PROFILES.keys()), default=["Colorado", "Washington", "Maryland"], max_selections=5, label_visibility="collapsed")

if compare_states:
    chk = '<span class="chk">✓</span>'
    x = '<span class="cross">—</span>'
    rows = ""
    for s in compare_states:
        d = STATE_PROFILES[s]
        fee_color = "var(--g700)" if d["has_fee"] else "#EF4444"
        rows += f'''
        <tr>
            <td class="st-name">{s}</td>
            <td style="font-family:'JetBrains Mono',monospace;font-weight:600;color:{fee_color}">{d["fee"]}</td>
            <td>{chk if d["trust"] else x}</td>
            <td>{chk if d["mobile"] else x}</td>
            <td>{chk if d["stab"] else x}</td>
            <td>{chk if d["youth"] else x}</td>
            <td>{score_bar_html(d["score"])}</td>
        </tr>'''

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:14px;margin:16px 0">
    <table class="cmp-table">
        <thead><tr>
            <th>State</th><th>Fee</th><th>Trust Fund</th><th>Mobile Crisis</th><th>Stabilization</th><th>Youth</th><th>Score</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table></div>
    """, unsafe_allow_html=True)


# ===========================================================================
# 13. FOOTER CTA
# ===========================================================================
st.markdown("""
<div class="footer-cta">
    <h3>Every crisis deserves a<br>compassionate response.</h3>
    <p>Your voice can shape the future of mental health crisis care. Advocate for 988 funding in your state.</p>
    <div class="footer-btns">
        <a class="cta-primary" href="https://reimaginecrisis.org/map/" target="_blank">Explore the Legislation Map →</a>
        <a class="cta-secondary" href="https://www.nami.org/advocacy/" target="_blank">Get Involved with NAMI</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:12px 0 48px;font-family:'Source Sans 3',sans-serif;font-size:14px;color:#64748B">
    If you or someone you know is in crisis, <strong>call or text 988</strong> for free, confidential support 24/7.
</div>
""", unsafe_allow_html=True)
