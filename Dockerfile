FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first for better caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY ACEestFitness /app/ACEestFitness

# Work from inside the package and run the script directly
WORKDIR /app/ACEestFitness
EXPOSE 5000
CMD ["python", "app.py"]
