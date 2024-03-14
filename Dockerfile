# Use the official Python image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies including the LinkedIn API from GitHub
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install git+https://github.com/tomquirk/linkedin-api.git

# Copy the application code into the container
COPY . .

# Expose port 3000
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
