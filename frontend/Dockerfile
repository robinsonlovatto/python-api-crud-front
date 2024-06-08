# Dockerfile-frontend

# Base image
FROM python:3.9

# defining workdir in the container
WORKDIR /app

# Copy dependencies file and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the remaining files
COPY . /app

# Execute the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]