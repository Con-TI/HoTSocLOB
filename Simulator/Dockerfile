# Use an official Python runtime as base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput
# Expose the static directory
EXPOSE 8080

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi"]
