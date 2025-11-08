# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ACEestFitness/ .

# Expose the port your app runs on
EXPOSE 5000

# Run the application
CMD ["python", "-m", "ACEestFitness.app"]
