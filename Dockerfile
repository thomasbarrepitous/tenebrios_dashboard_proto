# Use official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY tenebrios_dashboard_proto/requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY tenebrios_dashboard_proto/ .

# Run the Dash app
CMD gunicorn -b 0.0.0.0:80 app:server

# CMD ["python", "app.py"]
