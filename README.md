# LinkedIn Remote Job Scraper

A FastAPI service that scrapes remote job listings from LinkedIn.

## Prerequisites

- Python 3.7+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version)

## Quick Start

1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/lanznx/linkedin-remote-job-scraper.git
cd linkedin-remote-job-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies using `uv`:
```bash
uv pip install -r requirements.txt
```

5. Start the server:
```bash
uv venv run uvicorn app.main:app --reload
```

The service will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Basic Usage

Test the API using curl:
```bash
curl -X POST "http://localhost:8000/scraper/jobs/" \
     -H "Content-Type: application/json" \
     -d '{"locations": ["United States"], "limit": 10}'
```

## Development

For hot-reload during development:
```bash
uv venv run uvicorn app.main:app --reload --port 8000
```