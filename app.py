import streamlit as st
import json
import urllib.parse

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
    {"icon": "💰", "title": "Sustainable Funding", "subtitle": "The foundation of effective crisis care", "desc": "Telecom fees mirror the proven 911 funding model and provide predictable revenue without relying on annual budget fights.", "states": ["Colorado", "Washington", "California"], "stat": "12", "stat_label": "states with 988 fees", "rec": "Enact a monthly telecom fee dedicated to 988 and crisis services, protected by a trust fund.", "share": "12 states have enacted 988 telecom fees to fund mental health crisis services. Your state should be next."},
    {"icon": "🚐", "title": "Mobile Crisis Teams", "subtitle": "Someone to respond", "desc": "Mobile crisis teams bring licensed professionals to the person in distress as an alternative to law enforcement response.", "states": ["Virginia", "Ohio", "Minnesota"], "stat": "18", "stat_label": "states expanded mobile crisis in 2024", "rec": "Deploy mobile crisis teams statewide with a 60-minute response target.", "share": "18 states expanded mobile crisis teams in 2024. Mental health crises deserve mental health responses."},
    {"icon": "🏥", "title": "Crisis Stabilization", "subtitle": "A safe place for help", "desc": "Short-term crisis facilities offer an alternative to ERs and jails with up to 23 hours of observation and treatment.", "states": ["Washington", "Ohio", "Connecticut"], "stat": "14", "stat_label": "states funded new stabilization centers", "rec": "Invest in crisis stabilization units so every community has a therapeutic alternative to ERs.", "share": "14 states funded new crisis stabilization centers in 2024. No one in crisis should end up in an ER or a jail."},
    {"icon": "🧒", "title": "Youth Crisis Services", "subtitle": "Meeting young people where they are", "desc": "Specialized crisis services for children and adolescents include school-based teams, youth-specific hotlines, and age-appropriate programs.", "states": ["Washington", "Maryland", "Minnesota"], "stat": "11", "stat_label": "states passed youth crisis legislation", "rec": "Establish youth-specific crisis protocols and specialized training for crisis workers.", "share": "11 states passed youth crisis legislation in 2024. Young people deserve crisis care designed for them."},
    {"icon": "🛡️", "title": "Trust Fund Protections", "subtitle": "Ensuring funds reach crisis services", "desc": "Without dedicated trust funds, 988 fee revenue can be diverted to unrelated budget items.", "states": ["Colorado", "Nevada", "Ohio"], "stat": "10", "stat_label": "states with 988 trust funds", "rec": "Establish a dedicated 988 trust fund with statutory protections preventing diversion.", "share": "10 states protect 988 fee revenue with trust funds. Every dollar should go to crisis services."},
]

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
def score_bar_html(score, max_score=5, variant="default"):
    if variant == "hero":
        bar_w, bar_h, txt_size, txt_weight, gap = 36, 10, 17, 600, 7
    else:
        bar_w, bar_h, txt_size, txt_weight, gap = 24, 8, 12, 500, 4

    bars = ""
    for i in range(max_score):
        color = "#2D6A4F" if i < score else "#E5E7EB"
        bars += f'<div style="width:{bar_w}px;height:{bar_h}px;border-radius:999px;background:{color};display:inline-block;margin-right:{gap}px"></div>'
    score_color = "#2D6A4F" if score >= 4 else "#E8590C" if score >= 2 else "#EF4444"
    bars += f'<span style="font-family:JetBrains Mono,monospace;font-size:{txt_size}px;font-weight:{txt_weight};color:{score_color};margin-left:8px">{score}/{max_score}</span>'
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
.block-container { padding-top: 0 !important; max-width: 1100px !important; }
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

/* STATE CARD */
div[data-testid="stVerticalBlockBorderWrapper"] {
    margin-top: -52px !important;
    margin-bottom: 30px !important;
    position: relative !important;
    z-index: 10 !important;
    border-radius: 24px !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06) !important;
    background: #FFF !important;
    padding: 30px 34px 32px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    padding: 0 !important;
}
.state-head-label { font-family:'Source Sans 3',sans-serif; font-size:15px; font-weight:700; color:var(--s900); padding-top:8px; }
div[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] > div {
    background:var(--g50) !important;
    border:2px solid var(--g200) !important;
    border-radius:14px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] span {
    color:var(--g700) !important;
    font-weight:700 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] svg {
    fill:var(--g700) !important;
}
.state-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin-top:20px; }
.sg-item { padding:16px; border-radius:10px; min-height:154px; display:flex; flex-direction:column; justify-content:space-between; }
.sg-label { font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700; color:var(--s500);
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:4px; }
.sg-val { font-family:'Playfair Display',serif; font-size:56px; font-weight:900; line-height:1; }
.sg-status { font-family:'Source Sans 3',sans-serif; font-size:18px; font-weight:700; }

@media (max-width: 980px) {
    .state-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media (max-width: 700px) {
    div[data-testid="stVerticalBlockBorderWrapper"] {
        margin-top:-36px !important;
        padding:20px 18px !important;
    }
}
@media (max-width: 520px) {
    .state-grid { grid-template-columns:1fr; }
}

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
.tl-container { position:relative; padding:20px 0 20px 40px; margin:20px 0; }
.tl-container::before { content:''; position:absolute; left:18px; top:0; bottom:0; width:2px;
    background:linear-gradient(to bottom,var(--g200),var(--g600),var(--g200)); }
.tl-item { position:relative; padding:0 0 32px 36px; }
.tl-dot { position:absolute; top:6px; border-radius:50%; z-index:2; }
.tl-dot.normal { left:-30px; width:14px; height:14px; background:#FFF; border:3px solid var(--g600); }
.tl-dot.milestone { left:-31px; width:16px; height:16px; background:var(--g600); box-shadow:0 0 0 4px var(--g200); }
.tl-date { font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:500; color:var(--g600);
    letter-spacing:0.04em; margin-bottom:4px; }
.tl-title { font-family:'Playfair Display',serif; font-size:18px; font-weight:700; color:var(--s900);
    margin-bottom:6px; line-height:1.3; }
.tl-desc { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s500); line-height:1.6; max-width:520px; }

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

/* POLICY CARD */
.pol-card { background:#FFF; border-radius:16px; padding:32px; margin-bottom:16px;
    border:1px solid rgba(0,0,0,0.04); box-shadow:0 2px 12px rgba(0,0,0,0.03);
    transition:all 0.3s; }
.pol-card:hover { box-shadow:0 8px 30px rgba(0,0,0,0.06); transform:translateY(-2px); }
.pol-icon { font-size:28px; margin-bottom:10px; }
.pol-title { font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:var(--s900); margin-bottom:4px; }
.pol-sub { font-family:'Source Sans 3',sans-serif; font-size:13px; font-weight:500; color:var(--g600);
    letter-spacing:0.04em; text-transform:uppercase; margin-bottom:14px; }
.pol-desc { font-family:'Source Sans 3',sans-serif; font-size:15px; color:var(--s700); line-height:1.65; margin-bottom:16px; }
.pol-stat { display:inline-flex; align-items:baseline; gap:6px; background:var(--g50);
    border:1px solid var(--g200); border-radius:10px; padding:10px 18px; margin-bottom:12px; }
.pol-stat-num { font-family:'Playfair Display',serif; font-size:28px; font-weight:900; color:var(--g700); line-height:1; }
.pol-stat-label { font-family:'Source Sans 3',sans-serif; font-size:13px; font-weight:500; color:var(--g700); }
.pol-states { display:flex; gap:6px; flex-wrap:wrap; margin:12px 0 16px; }
.pol-state-tag { font-family:'Source Sans 3',sans-serif; font-size:11px; font-weight:600; color:var(--g700);
    background:var(--g100); padding:4px 12px; border-radius:20px; }
.rec-box { background:var(--s100); border-radius:10px; padding:16px 20px; border-left:3px solid var(--g600); }
.rec-label { font-family:'Source Sans 3',sans-serif; font-size:10px; font-weight:700; color:var(--g700);
    letter-spacing:0.12em; text-transform:uppercase; margin-bottom:6px; }
.rec-text { font-family:'Source Sans 3',sans-serif; font-size:14px; color:var(--s700); line-height:1.6; }

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
.cta-primary, .cta-primary:visited { color:var(--g900) !important; text-decoration:none !important; }
.cta-secondary, .cta-secondary:visited { color:#FFF !important; text-decoration:none !important; }

/* WIDGET THEMING */
[data-baseweb="select"] > div,
[data-baseweb="select"] > div:hover {
    background:#FFFFFF !important;
    border:1.5px solid #CBD5E1 !important;
    box-shadow:none !important;
}
[data-baseweb="select"] span {
    color:var(--s900) !important;
    font-family:'Source Sans 3',sans-serif !important;
    font-weight:600 !important;
}
[data-baseweb="select"] svg {
    fill:var(--s700) !important;
}
div[role="listbox"] {
    background:#FFFFFF !important;
    border:1px solid #CBD5E1 !important;
    box-shadow:0 10px 24px rgba(15,23,42,0.12) !important;
}
div[role="option"] {
    color:var(--s700) !important;
    background:#FFFFFF !important;
}
div[role="option"][aria-selected="true"] {
    color:var(--g700) !important;
    background:var(--g50) !important;
}
[data-baseweb="tag"] {
    background:var(--g50) !important;
    border:1px solid var(--g200) !important;
}
[data-baseweb="tag"] * {
    color:var(--g700) !important;
}

div[data-testid="stSlider"] [role="slider"] {
    background:var(--g700) !important;
    border:2px solid var(--g700) !important;
    box-shadow:none !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
    background:var(--g700) !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}
div[data-testid="stRadio"] div[role="radiogroup"] label {
    margin:0;
    border:1px solid #CBD5E1;
    border-radius:999px;
    background:#FFFFFF;
    padding:7px 14px;
    min-height:36px;
}
div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
    display:none !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label p {
    margin:0 !important;
    color:var(--s700) !important;
    font-size:13px !important;
    font-weight:600 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    border-color:var(--g700);
    background:var(--g50);
}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
    color:var(--g700) !important;
}
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
    col_label, col_select, col_score = st.columns([1, 2, 2])
    with col_label:
        st.markdown('<p class="state-head-label">Your state:</p>', unsafe_allow_html=True)
    with col_select:
        selected_state = st.selectbox("Pick your state", sorted(STATE_PROFILES.keys()), index=sorted(STATE_PROFILES.keys()).index("Maryland"), label_visibility="collapsed")

    user_state = STATE_PROFILES[selected_state]

    with col_score:
        st.markdown(f'<div style="padding-top:8px">{score_bar_html(user_state["score"], variant="hero")}</div>', unsafe_allow_html=True)

    # Grid
    fee_bg = "var(--g50)" if user_state["has_fee"] else "#FEF2F2"
    fee_border = "var(--g200)" if user_state["has_fee"] else "#FECACA"
    fee_color = "var(--g700)" if user_state["has_fee"] else "#EF4444"

    items_html_parts = [
        '<div class="state-grid">',
        f'<div class="sg-item" style="background:{fee_bg};border:1px solid {fee_border}"><div class="sg-label">988 Fee</div><div class="sg-val" style="color:{fee_color}">{user_state["fee"]}</div></div>',
        f'<div class="sg-item" style="background:var(--s100)"><div class="sg-label">Est. Revenue</div><div class="sg-val" style="color:var(--s900)">{user_state["revenue"]}</div></div>',
    ]
    for label, key in [("Trust Fund", "trust"), ("Mobile Crisis", "mobile"), ("Stabilization", "stab"), ("Youth Services", "youth")]:
        val = user_state[key]
        bg = "var(--g50)" if val else "var(--s100)"
        bdr = "border:1px solid var(--g200);" if val else ""
        color = "var(--g700)" if val else "var(--s300)"
        text = "✓ Active" if val else "— None"
        items_html_parts.append(
            f'<div class="sg-item" style="background:{bg};{bdr}"><div class="sg-label">{label}</div><div class="sg-status" style="color:{color}">{text}</div></div>'
        )
    items_html_parts.append("</div>")
    st.markdown("".join(items_html_parts), unsafe_allow_html=True)


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
# 4. SUCCESS STORIES
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Real Impact</div>
<h2>988 Changed Their Story</h2>
<p>Behind the numbers are real people who found help when they needed it most.</p></div>
""", unsafe_allow_html=True)

story_choice = st.radio("Select a story", [s["tag"] for s in SUCCESS_STORIES], horizontal=True, label_visibility="collapsed")
story = next(s for s in SUCCESS_STORIES if s["tag"] == story_choice)

st.markdown(f"""
<div class="story-card">
    <div class="story-tag">{story["tag"]}</div>
    <p class="story-text">{story["text"]}</p>
    <div class="story-attr">{story["attribution"]}</div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 5. FEE DATA STORY
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

share_3in4 = share_button_html("3 in 4 Americans support a monthly phone fee to fund 988 crisis services. It's time for every state to act.", "Share this stat")
st.markdown(f"""
<div class="data-callout">
    <div class="dc-stat">3 in 4</div>
    <div class="dc-label">Americans are willing to pay a monthly fee to fund 988 crisis services</div>
    <div class="dc-ctx">With more than a third willing to pay more than the highest existing fee ($0.72), the public mandate is clear.</div>
    <div style="margin-top:20px;position:relative">{share_3in4}</div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 6. REVENUE CALCULATOR
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">What If</div>
<h2>Revenue Calculator</h2>
<p>See what a 988 fee could generate in states that haven't enacted one yet.</p></div>
""", unsafe_allow_html=True)

no_fee_states = sorted([s for s, d in STATE_PROFILES.items() if not d["has_fee"]])
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
# 8. ADVOCATES
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Voices</div>
<h2>From the Field</h2>
<p>Leaders shaping the future of crisis response.</p></div>
""", unsafe_allow_html=True)

for adv in ADVOCATES:
    share_q = share_button_html(f'"{adv["quote"]}" — {adv["name"]}', "Share quote")
    st.markdown(f"""
    <div class="adv-card">
        <div class="adv-accent" style="background:{adv['accent']}"></div>
        <div class="adv-text" style="color:{adv['accent']}">{adv["quote"]}</div>
        <div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px">
            <div><div class="adv-name">{adv["name"]}</div><div class="adv-role">{adv["role"]}</div></div>
            {share_q}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================================
# 9. POLICY CARDS
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Policy Playbook</div>
<h2>Five Moves States Can Make</h2>
<p>Concrete recommendations backed by what's already working.</p></div>
""", unsafe_allow_html=True)

for pol in POLICIES:
    states_tags = "".join(f'<span class="pol-state-tag">{s}</span>' for s in pol["states"])
    share_p = share_button_html(pol["share"], "Share stat")
    email_p = email_button_html(
        f"Support {pol['title']} for 988 Crisis Services",
        f"{pol['share']}\n\nI'm writing to ask you to support legislation that would {pol['rec'].lower()}\n\nLearn more: https://reimaginecrisis.org/map/",
    )
    st.markdown(f"""
    <div class="pol-card">
        <div class="pol-icon">{pol["icon"]}</div>
        <div class="pol-title">{pol["title"]}</div>
        <div class="pol-sub">{pol["subtitle"]}</div>
        <div class="pol-desc">{pol["desc"]}</div>
        <div class="pol-stat"><span class="pol-stat-num">{pol["stat"]}</span><span class="pol-stat-label">{pol["stat_label"]}</span></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">{share_p} {email_p}</div>
        <div class="pol-states"><span style="font-size:11px;color:#64748B;font-weight:500;margin-right:4px">Leading:</span>{states_tags}</div>
        <div class="rec-box"><div class="rec-label">NAMI Recommendation</div><div class="rec-text">{pol["rec"]}</div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"Details: {pol['title']}", expanded=False):
        st.write("")  # keeps expander functional


# ===========================================================================
# 10. SCORECARD
# ===========================================================================
st.markdown("""
<div class="sh"><div class="ey">Scorecard</div>
<h2>Crisis System Readiness</h2>
<p>5 criteria: fee, trust fund, mobile crisis, stabilization, youth services.</p></div>
""", unsafe_allow_html=True)

sorted_states = sorted(STATE_PROFILES.keys(), key=lambda s: STATE_PROFILES[s]["score"], reverse=True)
sc_html = '<div class="sc-grid">'
for s in sorted_states:
    d = STATE_PROFILES[s]
    is_user = s == selected_state
    cls = " you" if is_user else ""
    badge = '<span class="sc-you-badge">YOU</span>' if is_user else ""
    fee_text = f"Fee: {d['fee']}" if d["has_fee"] else "No fee enacted"
    sc_html += f'''
    <div class="sc-card{cls}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <span class="sc-name">{s}</span>{badge}
        </div>
        {score_bar_html(d["score"])}
        <div class="sc-fee">{fee_text}</div>
    </div>'''
sc_html += "</div>"
st.markdown(sc_html, unsafe_allow_html=True)


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
# 12. FOOTER CTA
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
