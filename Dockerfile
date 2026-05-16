FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY config.py .
COPY database.py .
COPY models.py .
COPY auth.py .
COPY utils.py .
COPY routes/ ./routes/

# Create routes __init__.py
RUN echo "" > routes/__init__.py

# Create .env file with defaults if not exists
RUN touch .env

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]