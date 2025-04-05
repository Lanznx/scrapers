# app/main.py
from fastapi import FastAPI
from .routers import scraper

app = FastAPI(
    title="LinkedIn Job Scraper API",
    description="API for scraping remote jobs from LinkedIn",
    version="1.0.0",
)

app.include_router(scraper.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LinkedIn Job Scraper API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
