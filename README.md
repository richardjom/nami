# Mental Health Bill Tracker

A Streamlit dashboard for tracking mental health legislation.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and point to `app.py`
4. Deploy

## Customizing Bills

Edit the `BILLS` list at the top of `app.py` to add, remove, or update tracked bills. Each bill object supports these fields:

- `id` — Bill identifier (e.g. HR-4321)
- `title` — Full bill name
- `status` — Current status label
- `status_step` — 1 through 5 matching the progress track
- `chamber` — "House" or "Senate"
- `introduced` — Date string
- `sponsors` — Number of co-sponsors
- `lead_sponsor` — Name and party of lead sponsor
- `summary` — Plain English summary
- `impact` — "Why this matters" section
- `provisions` — List of key provisions (4 recommended)
- `tags` — List of topic tags
- `urgency` — "high", "medium", or "low"
