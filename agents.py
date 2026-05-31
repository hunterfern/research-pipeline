import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="claude-sonnet-4-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Agents

moderator = Agent(
    role="User Research Moderator",
    goal="Conduct a realistic user interview on the given research topic",
    backstory="""You are an experienced UX researcher who conducts user interviews
                 for SaaS companies. You are probing, open-ended questions and capture 
                 realistic user responses. You create authentic-feeling interview transcripts.""",
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Research Analyst",
    goal="Extract structured insights from a user interview transcript",
    backstory="""You are a senior UX researcher who specializes in qualitative analysis.
                 You identify themes, pain points, key quotes, and surprising findings from
                 raw interview transcripts.""",
    llm=llm,
    verbose=True
)

reporter = Agent(
    role="Research Reporter",
    goal="Write a concise, shareable research report based on the extracted insights",
    backstory="""You are a skilled writer who creates clear and engaging research reports.
                 You synthesize complex insights into actionable recommendations for product teams.""",
    llm=llm,
    verbose=True
)

# Tasks

def create_tasks(topic):
    interview_task = Task(
        description=f"""Conduct a realistic user interview about: {topic}

        Create a full transcript with a mdoerator asking 5-7 questions and 
        a realistic user persona responding. the user should have real frustrations,
        workflows, and opinions. Format it clearly as a back-and-forth conversation.""",
        
        expected_output="A realistic interview transcript with moderator questions and user responses",
        agent=moderator
        
    )

    analysis_task = Task(
        description="""Analyze the interview transcript and extract:
        - 3-5 key themes
        - Top pain points (with supporting quotes)
        - Surprising or unexpected findings
        - One clear opportunity for improvement
        
        Be specific and reference actual quotes from the transcript.""",

        expected_output="Structured insights with themes, pain points, quotes, and opportunities",
        agent=analyst,
        context=[interview_task]
    )
    
    report_task = Task(
        description="""Write a clean research summary report based on the insights.
        
        Format it as something a PM or designer would actually read and share with 
        their team. Include: executive summary, key findings, notable quotes, 
        and recommended next steps.""",

        expected_output="A polished, shareable research report in markdown format",
        agent=reporter,
        context=[analysis_task]
    )

    return interview_task, analysis_task, report_task

# Crew

def run_pipeline_streaming(stage, topic, previous_output=None):
    
    if stage == "interview":
        task = Task(
            description=f"""Conduct a realistic user interview about: {topic}
            
            Create a full transcript with a moderator asking 5-7 questions and 
            a realistic user persona responding. The user should have real frustrations, 
            workflows, and opinions. Format it clearly as a back-and-forth conversation.""",
            expected_output="A realistic interview transcript with moderator questions and user responses",
            agent=moderator
        )
        crew = Crew(agents=[moderator], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        return task.output.raw

    elif stage == "analysis":
        task = Task(
            description=f"""Analyze this interview transcript and extract:
            - 3-5 key themes
            - Top pain points with supporting quotes
            - Surprising or unexpected findings
            - One clear opportunity for improvement
            
            Transcript:
            {previous_output}""",
            expected_output="Structured insights with themes, pain points, quotes, and opportunities",
            agent=analyst
        )
        crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        return task.output.raw

    elif stage == "report":
        task = Task(
            description=f"""Write a clean research summary report based on these insights.
            
            Format it as something a PM or designer would actually read and share with 
            their team. Include: executive summary, key findings, notable quotes, 
            and recommended next steps.
            
            Insights:
            {previous_output}""",
            expected_output="A polished, shareable research report in markdown format",
            agent=reporter
        )
        crew = Crew(agents=[reporter], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        return task.output.raw
