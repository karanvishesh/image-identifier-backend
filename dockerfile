# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y espeak
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS /app/tia-ai.json

# Run the Python script
CMD ["python", "main.py"]
