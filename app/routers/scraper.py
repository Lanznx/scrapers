# app/routers/scraper.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..internal.scraper_service import scrape_linkedin_jobs

router = APIRouter(
    prefix="/scraper",
    tags=["scraper"],
    responses={404: {"description": "Not found"}},
)


class JobInfo(BaseModel):
    title: str
    company: str
    company_link: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    insights: Optional[dict] = {}


class ScrapeResponse(BaseModel):
    jobs: List[JobInfo]
    total_jobs: int
    status: str


@router.post("/jobs/", response_model=ScrapeResponse)
async def scrape_jobs(
    locations: List[str] = ["United States", "Europe", "Asia"],
    limit: int = 100,
    job_title: str = "",
):
    try:
        jobs = await scrape_linkedin_jobs(
            locations=locations, limit=limit, job_title=job_title
        )
        return ScrapeResponse(jobs=jobs, total_jobs=len(jobs), status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
