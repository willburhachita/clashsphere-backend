FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Set MySQL client environment variables
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Create and activate virtual environment
RUN python -m venv --copies /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static directories if they don't exist
RUN mkdir -p static static_files

# Make startup script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run the startup script
CMD ["./start.sh"] 