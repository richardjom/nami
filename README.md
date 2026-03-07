# 988 Issue Brief: Enhanced Interactive Experience

A Streamlit reimagining of NAMI's 2024 State Legislation Issue Brief on 988 and crisis response.

## Features

1. **Live Impact Counter** — Animated contact total in the hero section
2. **State Personalization** — Select your state and see tailored data throughout the page
3. **Before/After Comparison** — Side by side view of the old vs. new crisis response model
4. **Success Stories** — Rotating first-person accounts from 988 users
5. **Fee Data Story** — Visual bar chart of state fees with your state highlighted
6. **Revenue Calculator** — Project what a 988 fee would generate in states without one
7. **Timeline** — Key milestones from 988's creation to today
8. **Advocate Spotlights** — Featured quotes from NAMI leaders
9. **Policy Playbook** — Five actionable policy cards with share and email buttons
10. **State Scorecard** — Visual readiness scores for every tracked state
11. **State Comparison** — Side by side table for up to 5 states

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to share.streamlit.io
3. Connect your repo, point to `app.py`
4. Deploy

## Customization

All data lives in Python dictionaries at the top of `app.py`:

- `STATE_PROFILES` — Add or update state data
- `FEE_STATES` — Fee bar chart entries
- `POLICIES` — Policy recommendation cards
- `SUCCESS_STORIES` — Rotating story carousel
- `TIMELINE` — Timeline milestones
- `ADVOCATES` — Quote spotlights

Colors and fonts are controlled via CSS variables in the `<style>` block.
