from crewai import Agent, Task, Crew, Process
from crewai_tools import YoutubeChannelSearchTool


def get_ytquery_response_from_agent(
        ytchannel_identifier: str='@bigbangtheory',
        ytvideo_topic: str='Sheldon Goes to a Job Recruiter',
        query: str='What is emphasis of this video?'

    ) :

    yt_tool = YoutubeChannelSearchTool(youtube_channel_handle=ytchannel_identifier)

    # Agents
    # By default using model specified in env variable OPENAI_MODEL_NAME or 'gpt-4'
    topic_researcher = Agent(
        role='Topic Researcher from Youtube Videos',
        goal='Research and extract comprehensive information from YouTube videos',
        #verbose=True,
        memory=True,
        backstory="Expert in analyzing video content and creating detailed research summaries",
        tools=[yt_tool],
        allow_delegation=True # keeping true so that it works sequentially not parallelly
    )

    topic_answerer = Agent(
        role='Topic answerer',
        goal='Create focused answers using research provided by the Topic Researcher',
        #verbose=True,
        memory=True,
        backstory=(
            "Expert at synthesizing research and creating clear, focused answers. "
            "Skilled at extracting relevant information and presenting it in an accessible way."
        ),
        tools=[],  # empty because this agent should work with researcher's findings
        allow_delegation=False
    )

    # Tasks
    research_task = Task(
        description=(
            "Research the video about {topic}. "
            "Create a detailed summary of the video content including key points, "
            "main arguments, named entities, and important details. "
            "This research will be used by the topic answerer."
        ),
        expected_output=(
            "A comprehensive research document containing:\n"
            "1. Main points from the video\n"
            "2. Important details and context\n"
            "3. Any relevant quotes or specific information"
        ),
        tools=[yt_tool],
        agent=topic_researcher
    )

    answer_task = Task(
        description=(
            "Using the research provided by the topic researcher about {topic}, "
            "concise answer the following query: {query}"
        ),
        expected_output="A concise answer to the query based on the provided research",
        tools=[],
        agent=topic_answerer,
        context=[research_task]  # This connects the previous and enables data passing
    )

    # Crew configuration
    crew = Crew(
        agents=[topic_researcher, topic_answerer],
        tasks=[research_task, answer_task],
        process=Process.sequential,
        memory=True,
        share_crew=True
    )

    #Execute tasks
    return crew.kickoff(
        inputs={
            'topic': ytvideo_topic,
            'query': query
        }
    )

