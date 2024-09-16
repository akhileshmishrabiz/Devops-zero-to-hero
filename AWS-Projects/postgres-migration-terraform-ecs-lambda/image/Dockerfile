FROM ubuntu:22.04

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        wget \
        ca-certificates \
        ruby-dev \
        libpq-dev \
        build-essential \
        postgresql-client 

# Install pgsync gem
RUN gem install pgsync

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python application code into the container
COPY main.py main.py

# Set the command to run the Python application
CMD ["python3", "main.py"]
