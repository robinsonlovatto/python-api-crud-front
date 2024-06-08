# Dockerfile-backend

# Base image
FROM python:3.9

# defining workdir
WORKDIR /app

# Copy dependencies file and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the remaining files
COPY . /app

# Execute the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]