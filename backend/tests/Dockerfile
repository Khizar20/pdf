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

# Download and install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

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