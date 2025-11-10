# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire ACEestFitness folder into the container's /app folder
COPY ACEestFitness /app/ACEestFitness

# Expose the port your Flask app runs on
EXPOSE 5000

# Set the working directory to ACEestFitness where app.py is
WORKDIR /app/ACEestFitness

# Run the app
CMD ["python", "app.py"]
