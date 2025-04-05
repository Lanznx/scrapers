FROM python:3.13-slim

WORKDIR /app

# Install dependencies for headless browser
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome and ChromeDriver with architecture detection
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Architecture: $(uname -m)" \
    && echo "Chromium binary: $(which chromium)" \
    && echo "ChromeDriver binary: $(which chromedriver)"

# Copy project files and install dependencies
COPY pyproject.toml uv.lock ./
COPY app ./app

# Install uv for package management
RUN pip install --no-cache-dir uv
RUN uv pip install --system --no-cache-dir -e .

# Set environment variables for headless browser
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LINKEDIN_SCRAPER_HEADLESS=true \
    LINKEDIN_SCRAPER_NO_BROWSER=false \
    PYTHONPATH="${PYTHONPATH}:/app" \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]