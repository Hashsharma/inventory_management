# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY /requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run Uvicorn server
# Command to run mi# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY /requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run Uvicorn server
# Command to run migrations and then the Uvicorn server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && uvicorn inventory_mgmt.asgi:application --host 0.0.0.0 --port 8000"]
