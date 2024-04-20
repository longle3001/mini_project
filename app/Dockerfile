# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory to /code
WORKDIR /app

# Copy the requirements.txt file into the container at /code
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
