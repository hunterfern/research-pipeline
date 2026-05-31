import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_agent(system_prompt, user_prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return message.content[0].text

def run_pipeline_streaming(stage, topic, previous_output=None):

    if stage == "interview":
        return run_agent(
            system_prompt="""You are an experienced UX researcher who conducts user interviews 
            for SaaS companies. You ask probing, open-ended questions and capture realistic 
            user responses. You create authentic-feeling interview transcripts.""",
            user_prompt=f"""Conduct a realistic user interview about: {topic}
            
            Create a full transcript with a moderator asking 5-7 questions and 
            a realistic user persona responding. The user should have real frustrations, 
            workflows, and opinions. Format it clearly as a back-and-forth conversation."""
        )

    elif stage == "analysis":
        return run_agent(
            system_prompt="""You are a senior UX researcher who specializes in qualitative 
            analysis. You identify themes, pain points, key quotes, and surprising findings 
            from raw interview transcripts.""",
            user_prompt=f"""Analyze this interview transcript and extract:
            - 3-5 key themes
            - Top pain points with supporting quotes
            - Surprising or unexpected findings
            - One clear opportunity for improvement
            
            Transcript:
            {previous_output}"""
        )

    elif stage == "report":
        return run_agent(
            system_prompt="""You write clear, concise research reports for product teams. 
            Your reports are actionable, well-structured, and easy for PMs and designers 
            to act on.""",
            user_prompt=f"""Write a clean research summary report based on these insights.
            
            Format it as something a PM or designer would actually read and share with 
            their team. Include: executive summary, key findings, notable quotes, 
            and recommended next steps.
            
            Insights:
            {previous_output}"""
        )