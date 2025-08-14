# Multi‑Agent AI Blog Generator 
<img width="318" height="159" alt="image" src="https://github.com/user-attachments/assets/5c2d3313-53ba-4966-8ae1-3e23b76da1ad" />


## OVERVIEW

The Multi-Agent AI Blog Generator is a Streamlit web application that uses a multi-agent architecture to automatically create high-quality, SEO-optimized blog posts.
Each AI agent plays a specialized role — from research to final content packaging — to ensure the final output is factual, well-structured, engaging, and ready to publish.
This project leverages the OpenAI API and the official Python SDK to orchestrate different "agents" in sequence, automating the end-to-end blog creation workflow.


## Goal / Objective

- Automate the process of researching, outlining, writing, editing, and optimizing blog posts.

- Ensure SEO best practices are followed for better search rankings.

- Provide a user-friendly interface for anyone to create professional content without technical expertise.

- Showcase multi-agent AI coordination as a real-world, portfolio-ready AI project.

## How It Works 🛠

Agent Workflow

Research Agent
Gathers factual bullet points, statistics, and credible sources for the given topic.

Outline Agent
Structures the blog post with an SEO-friendly H1, H2, and H3 headings, plus content placement notes.

Writing Agent
Drafts the complete blog in markdown, incorporating the research findings.

Editing Agent
Polishes clarity, grammar, tone, and readability while preserving style.

SEO Agent
Suggests meta titles, descriptions, keywords, and FAQ sections for better ranking.

Finalizer Agent
Combines the edited draft and SEO pack into a final markdown file for download.


## Implementation Details

- Frontend: Streamlit

- Backend: OpenAI GPT models (gpt-4o-mini, gpt-4o, gpt-4.1-mini)

- Language: Python

 Dependencies:

 - streamlit

 - openai

 - python-dotenv


## Results

✅ Fully functional multi-agent content generation pipeline.
✅ Produces ready-to-publish blog posts in markdown format.
✅ Customizable for different topics, audiences, and tones.
✅ Demonstrates AI workflow orchestration for portfolio and real-world use.


## Deployment (Streamlit App Pipeline)

User Input → Research Agent → Outline Agent → Writing Agent → Editing Agent → SEO Agent → Finalizer → Downloadable Blog
<img width="1918" height="1020" alt="image" src="https://github.com/user-attachments/assets/f2d9a5d9-0b67-4c3f-892d-35c30730e035" />
