# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

run apt-get update
RUN apt-get -y install gcc libpq-dev python3-dev

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

RUN mkdir -p tmp

# Expose a port for Gunicorn (replace 8000 with your desired port)
EXPOSE 8022

# Define the command to run Gunicorn with your Flask application
CMD ["gunicorn", "-b", "0.0.0.0:8022", "wsgi:app"]
