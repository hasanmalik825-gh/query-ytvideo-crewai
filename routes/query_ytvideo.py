from fastapi import APIRouter, Query
from services.ytvideo_query_agent import get_ytquery_response_from_agent

query_ytvideo_router = APIRouter()


@query_ytvideo_router.post("/query_ytvideo")
async def query_ytvideo(
    query: str = Query(..., description="Query for the video"),
    ytchannel_identifier: str = Query(..., description="Channel identifier like '@bigbangtheory'."),
    ytvideo_topic: str = Query(..., description="Video topic like 'Sheldon Goes to a Job Recruiter'.")
):
    response=get_ytquery_response_from_agent(
        ytchannel_identifier=ytchannel_identifier,
        ytvideo_topic=ytvideo_topic,
        query=query
    )
    return response.model_dump()