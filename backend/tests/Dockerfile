# Use Python 3.10 base image
FROM python:3.10-slim

# Install system dependencies including Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    # Add Google Chrome repository
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and install ChromeDriver using Chrome for Testing API
RUN CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | cut -d "." -f1-3) \
    && echo "Chrome version: $CHROME_VERSION" \
    && CHROMEDRIVER_VERSION=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") \
    && echo "ChromeDriver version: $CHROMEDRIVER_VERSION" \
    && wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && /usr/local/bin/chromedriver --version

# Copy test files
COPY . .

# Set environment variables for headless operation
ENV DISPLAY=:99
# Default URL - will be overridden by Jenkins with EC2 IP
ENV TEST_BASE_URL=http://localhost:80

# Create test reports directory
RUN mkdir -p test_reports

# Run tests by default
CMD ["python", "-m", "pytest", "test_simplified.py", "-v", "--tb=short", "--html=test_reports/test_report.html", "--self-contained-html"] 