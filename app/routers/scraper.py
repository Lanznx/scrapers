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
    company_link: Optional[str]
    date: Optional[str]
    link: Optional[str]
    description: Optional[str]
    insights: Optional[dict]


class ScrapeResponse(BaseModel):
    jobs: List[JobInfo]
    total_jobs: int
    status: str


@router.post("/jobs/", response_model=ScrapeResponse)
async def scrape_jobs(
    locations: List[str] = ["United States", "Europe", "Asia"], limit: int = 100
):
    try:
        jobs = await scrape_linkedin_jobs(locations=locations, limit=limit)
        return ScrapeResponse(jobs=jobs, total_jobs=len(jobs), status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
