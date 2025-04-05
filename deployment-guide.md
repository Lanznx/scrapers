# Deployment Guide for LinkedIn Job Scraper

This guide explains how to deploy the LinkedIn Job Scraper application using Docker and Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your server
- Nginx Proxy Manager or similar reverse proxy (already set up with `nginx-proxy-manager_proxy-network`)
- A domain or subdomain pointing to your server (e.g., `scraper.cerana.tech`)

## Deployment Steps

1. Clone the repository on your server:
   ```bash
   git clone https://github.com/yourusername/scraper.git
   cd scraper
   ```

2. Configure environment variables (optional):
   ```bash
   # Create a .env file in the project root
   touch .env
   ```

3. Build and start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Check the logs to make sure everything is working:
   ```bash
   docker-compose logs -f
   ```

5. Configure your Nginx Proxy Manager to create a proxy host:
   - Domain: `scraper.cerana.tech`
   - Scheme: `http`
   - Forward Hostname/IP: `linkedin-scraper`
   - Forward Port: `8000`
   - Enable SSL with Let's Encrypt

## Docker Commands Reference

Build and start the application:
```bash
docker-compose up -d --build
```

Start the application (if already built):
```bash
docker-compose up -d
```

Stop the application:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

Restart the application:
```bash
docker-compose restart
```

## Manual Docker Command (Alternative to Docker Compose)

If you prefer to run without Docker Compose, you can use this command:

```bash
# First build the image
docker build -t linkedin-scraper .

# Then run it
docker run -d \
  --name linkedin-scraper \
  -p 8000:8000 \
  -v scraper_data:/app/data \
  --network nginx-proxy-manager_proxy-network \
  --restart unless-stopped \
  linkedin-scraper
```

## Accessing the API

Once deployed, you can access the API at:

- API Documentation: `https://scraper.cerana.tech/docs`
- API Endpoint: `https://scraper.cerana.tech/scraper/jobs/`