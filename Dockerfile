# Use a lightweight Python image
FROM python:3.10-slim
 
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
# Set working directory
WORKDIR /app
 
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy project files
COPY . .
 
# Expose the port Cloud Run expects
EXPOSE 8080
 
# Use Gunicorn as WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]