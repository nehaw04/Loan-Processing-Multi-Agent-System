# Start with a clean Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install all the backend libraries
RUN pip install -r requirements.txt

# Copy all the backend code into the container
COPY . .

# Tell Docker the container will listen on port 8000
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]