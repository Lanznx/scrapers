# app/main.py
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import scraper
from .internal.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LinkedIn Job Scraper API",
    description="API for scraping remote jobs from LinkedIn",
    version="1.0.0",
)

# 添加 CORS 支持，允許所有來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源的跨域請求
    allow_credentials=False,  # 設置為 False 以避免與 allow_origins=["*"] 衝突
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有標頭
)

app.include_router(scraper.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LinkedIn Job Scraper API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    # Log environment information
    import os
    logger.info(f"Starting application with Chrome binary: {os.environ.get('CHROME_BIN', 'Not set')}")
    logger.info(f"ChromeDriver path: {os.environ.get('CHROMEDRIVER_PATH', 'Not set')}")
    logger.info(f"Debug mode: {settings.debug}")


# The application can be run directly with: 
# uvicorn app.main:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )
