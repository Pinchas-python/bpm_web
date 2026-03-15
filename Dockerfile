# Use Playwright Docker image
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Install additional system dependencies (if needed)
RUN apt-get update && apt-get install -y xvfb && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the default command to run tests with Playwright
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

CMD ["bash", "-lc", "Xvfb :99 -screen 0 1280x720x24 & pytest -vv --alluredir=/app/allure-results --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure"]

