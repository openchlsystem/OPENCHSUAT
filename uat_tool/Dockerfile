# Use official Python image as base. 3.13.2
FROM python:3.13.2

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Copy the entire backend project
COPY . .

# Expose port
EXPOSE 8005

# Run migrations and start the server
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8005 uat_tool.wsgi:application
