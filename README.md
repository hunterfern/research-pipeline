# AI Research Pipeline

A multi-agent AI system that automates user research — from conducting a realistic interview to extracting structured insights and generating a shareable report.

Built with CrewAI and Claude as a demo for exploring how agentic AI can augment the user research workflow.

## How It Works

Three specialized agents run sequentially:

1. **Moderator Agent** — Conducts a realistic user interview based on your research topic
2. **Analyst Agent** — Extracts themes, pain points, and key quotes from the transcript  
3. **Reporter Agent** — Writes a clean, shareable research report ready for your product team

## Demo

[Live Demo →](your-streamlit-url-here) ← update this after deployment

## Tech Stack

- [CrewAI](https://crewai.com) — multi-agent orchestration
- [Claude](https://anthropic.com) (claude-sonnet-4-5) — LLM backbone
- [Streamlit](https://streamlit.io) — UI and deployment

## Running Locally

1. Clone the repo
2. Create a virtual environment and install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file with your Anthropic API key: ANTHROPIC_API_KEY=your_key_here

4. Run the app:
```bash
   streamlit run app.py
```

## Motivation

Built as part of exploring how multi-agent systems can automate qualitative research workflows — specifically the gap between conducting research and getting insights into the hands of product teams.