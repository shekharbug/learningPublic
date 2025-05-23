# Use a lightweight official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to run the application using Gunicorn (production-ready WSGI server)
CMD ["python3", "/app/testApp.py"]
