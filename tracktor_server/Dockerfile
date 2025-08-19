# Base Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install build tools for Python packages like bcrypt
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency definition and install
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install .

# Copy all backend code
COPY . .

# SQLite persistence
RUN mkdir -p /app/data
VOLUME ["/app/data"]

# Expose Flask port
EXPOSE 8080

# Set PYTHONPATH so main.py can find modules
ENV PYTHONPATH=/app

# Run Flask app
CMD ["python", "main.py"]