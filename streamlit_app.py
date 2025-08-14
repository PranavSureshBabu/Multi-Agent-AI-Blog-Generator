import os
import time
import streamlit as st
from typing import Dict, Any, List
from dataclasses import dataclass
from dotenv import load_dotenv

# OpenAI SDK (>=1.0)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

load_dotenv()

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(page_title="Multi‑Agent AI Blog Generator", page_icon="🧩", layout="wide")

# Sidebar: API and Model settings
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Provide your API key via environment variable `OPENAI_API_KEY` or paste it below.")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    max_tokens = st.slider("Max tokens (per call)", 512, 4096, 1200, 64)
    show_steps = st.checkbox("Show intermediate agent outputs", value=True)
    st.divider()
    st.caption("Tip: set OPENAI_API_KEY in a .env file for convenience.")

# Guard
if OpenAI is None:
    st.error("OpenAI Python SDK is required. Add `openai>=1.51.0` to requirements and install.")
    st.stop()

# -----------------------------
# Utility: LLM Call
# -----------------------------
def call_llm(messages: List[Dict[str, str]], *, api_key: str, model: str, temperature: float, max_tokens: int) -> str:
    client = OpenAI(api_key=api_key if api_key else None)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content

# -----------------------------
# Agent Definitions
# -----------------------------
@dataclass
class AgentResult:
    role: str
    output: str

def research_agent(topic: str, audience: str, tone: str, keywords: List[str]) -> AgentResult:
    system = "You are a meticulous research analyst. You gather factual points, recent statistics (with source names), and 5-8 key references/links. Use bullet points."
    user = f"""
Topic: {topic}
Audience: {audience}
Tone: {tone}
Target keywords: {', '.join(keywords) if keywords else 'N/A'}

Return:
- 8-12 bullet points of facts with brief context
- A short list of recent stats (if relevant)
- 5-8 suggested sources/links (non-paywalled when possible)
Avoid fabricating URLs.
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.4, max_tokens=max_tokens
    )
    return AgentResult("Research Agent", out)

def outline_agent(topic: str, audience: str, tone: str, keywords: List[str], research: str, word_target: int) -> AgentResult:
    system = "You are a senior content strategist. Create a logical, SEO-friendly outline for a long-form blog post."
    user = f"""
Create an outline for a blog post on: "{topic}".
Audience: {audience}
Tone: {tone}
Target keywords: {', '.join(keywords) if keywords else 'N/A'}
Word target: ~{word_target} words.

Use the research below to inform structure (do not repeat it verbatim):
---
{research}
---

Return:
- Title ideas (3)
- H1
- H2/H3 outline with approximate word counts
- Notes on where to include stats, examples, or visuals
- Suggested internal/external links placement
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.5, max_tokens=max_tokens
    )
    return AgentResult("Outline Agent", out)

def writing_agent(topic: str, audience: str, tone: str, outline: str, research: str) -> AgentResult:
    system = "You are a staff content writer. Produce clear, engaging, well-structured markdown content following the outline. Cite sources inline when appropriate."
    user = f"""
Write the full draft in **markdown** for the topic "{topic}".
Audience: {audience}
Tone: {tone}

Follow this outline strictly:
---
{outline}
---

Incorporate relevant points from this research when helpful:
---
{research}
---

Guidelines:
- Use headings (#, ##, ###), short paragraphs, and occasional bullet lists.
- Add a table of contents placeholder.
- Keep claims grounded; when referencing a stat or specific figure, attribute it (e.g., "(Source: Organization, Year)").
- Avoid fabricating links; reference source names even if link unknown.
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.8, max_tokens=max_tokens
    )
    return AgentResult("Writing Agent", out)

def editing_agent(draft_md: str, audience: str, tone: str) -> AgentResult:
    system = "You are a seasoned editor focused on clarity, flow, and correctness. Keep the author's voice while tightening."
    user = f"""
Edit the following markdown draft for clarity, flow, correctness, and concision. Maintain the intended tone: {tone}. Preserve markdown structure.

---
{draft_md}
---

Return the revised **markdown** in full.
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.3, max_tokens=max_tokens
    )
    return AgentResult("Editing Agent", out)

def seo_agent(topic: str, audience: str, keywords: List[str], draft_md: str) -> AgentResult:
    system = "You are an SEO specialist. You craft metadata and on-page recommendations."
    user = f"""
Based on the markdown draft below, produce:
- Final SEO title (≤ 60 chars if possible)
- Meta description (≤ 155 chars)
- URL slug
- Primary keyword + 4-8 secondary keywords
- 5-7 FAQs (Q&A pairs) to append as an FAQ section
- Recommended internal link anchors (generic) and external link types

Draft:
---
{draft_md}
---
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.5, max_tokens=max_tokens
    )
    return AgentResult("SEO Agent", out)

def finalizer_agent(draft_md: str, seo: str) -> AgentResult:
    system = "You are a content packager. You assemble final deliverables."
    user = f"""
Combine the edited markdown with the SEO pack. Append an **FAQ** section if provided by SEO. Ensure a clean Table of Contents placeholder after the H1. Return final markdown only.

Edited Draft:
---
{draft_md}
---

SEO Pack:
---
{seo}
---
"""
    out = call_llm(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key=api_key, model=model, temperature=0.2, max_tokens=max_tokens
    )
    return AgentResult("Finalizer", out)

# -----------------------------
# UI: Inputs
# -----------------------------
st.title("🧩 Multi‑Agent AI Blog Generator")
st.caption("Research → Outline → Writing → Editing → SEO → Finalize")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Blog topic / working title", placeholder="e.g., How Multi‑Agent AI Systems Transform Content Creation")
    audience = st.text_input("Target audience", placeholder="e.g., Content marketers at tech startups")
with col2:
    tone = st.selectbox("Tone", ["Professional", "Casual", "Educational", "Persuasive", "Playful"], index=0)
    word_target = st.number_input("Target word count", 600, 4000, 1500, 100)

keywords = st.text_input("Target keywords (comma‑separated)", placeholder="multi‑agent systems, AI content, workflow automation")
run_button = st.button("🚀 Generate Blog Post", use_container_width=True, type="primary")

# -----------------------------
# Orchestration
# -----------------------------
if run_button:
    if not api_key:
        st.error("Please provide an OpenAI API key in the sidebar.")
        st.stop()
    if not topic or not audience:
        st.error("Please fill in both Topic and Audience.")
        st.stop()

    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

    with st.spinner("Researching..."):
        r = research_agent(topic, audience, tone, kw_list)
        if show_steps:
            with st.expander("🔎 Research Agent Output", expanded=True):
                st.markdown(r.output)

    with st.spinner("Creating outline..."):
        o = outline_agent(topic, audience, tone, kw_list, r.output, int(word_target))
        if show_steps:
            with st.expander("🧭 Outline Agent Output", expanded=False):
                st.markdown(o.output)

    with st.spinner("Drafting content..."):
        w = writing_agent(topic, audience, tone, o.output, r.output)
        if show_steps:
            with st.expander("✍️ Writing Agent Output", expanded=False):
                st.markdown(w.output)

    with st.spinner("Editing draft..."):
        e = editing_agent(w.output, audience, tone)
        if show_steps:
            with st.expander("🧹 Editing Agent Output", expanded=False):
                st.markdown(e.output)

    with st.spinner("Preparing SEO pack..."):
        s = seo_agent(topic, audience, kw_list, e.output)
        if show_steps:
            with st.expander("🔍 SEO Agent Output", expanded=False):
                st.markdown(s.output)

    with st.spinner("Finalizing..."):
        f = finalizer_agent(e.output, s.output)

    st.success("✅ Blog post generated!")
    st.download_button(
        "📥 Download Markdown",
        data=f.output.encode("utf-8"),
        file_name=f"{topic.strip().lower().replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True
    )
    st.markdown("### 🧾 Final Output")
    st.markdown(f.output)
