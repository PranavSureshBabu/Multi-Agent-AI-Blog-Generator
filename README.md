# Multi‑Agent AI Blog Generator (Streamlit)

This app orchestrates multiple "agents" to produce a high‑quality, SEO‑ready blog post:
1) **Research Agent** – gathers facts and sources
2) **Outline Agent** – structures the post
3) **Writing Agent** – drafts the article in markdown
4) **Editing Agent** – polishes tone and clarity
5) **SEO Agent** – crafts metadata, keywords, FAQs
6) **Finalizer** – assembles the final markdown

## Quickstart
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Set your OpenAI API key
# Option A: environment variable
export OPENAI_API_KEY=sk-...
# Option B: put it in a .env file
cp .env.example .env
# then edit .env and add your key

# 4) Run the app
streamlit run streamlit_app.py
```

## Configuration
- **Model**: choose from sidebar (defaults to `gpt-4o-mini`).
- **Temperature**: creative variance per call.
- **Max tokens**: upper bound per API call (each agent call).

## Notes
- The app uses the official OpenAI Python SDK (>=1.0) and does **not** require the `swarm` package.
- For portfolio use, add screenshots and sample outputs to your README and link to your GitHub.
