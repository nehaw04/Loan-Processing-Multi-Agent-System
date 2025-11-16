# Start with a clean Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install all the frontend libraries
RUN pip install -r requirements.txt

# Copy all the frontend code into the container
COPY . .

# Tell Docker the container will listen on port 8501
EXPOSE 8501

# The command to run when the container starts
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]