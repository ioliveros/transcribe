FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    ffmpeg \
    portaudio19-dev

# Set up virtual environment
# RUN python3 -m venv /app/venv

# Activate virtual environment and install dependencies
# ENV PATH="/app/venv/bin:$PATH"
# WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# # Upgrade pip and install Python packages
# RUN pip install --upgrade pip setuptools && \
#     pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# COPY . /app

# Set the entry point
#ENTRYPOINT while true; do echo "Wait forever"; sleep 3600; done
