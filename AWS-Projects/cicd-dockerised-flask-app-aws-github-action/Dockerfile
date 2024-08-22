# Use the official Python 3 base image from Docker Hub
FROM python:3

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the src directory of the host to the /app directory inside the container
COPY src/requirements.txt /app

# Install the Python dependencies listed in the requirements.txt file using pip
RUN pip install -r requirements.txt

# Copy all files from the src directory of the host to the /app directory inside the container
COPY src/* /app

# Expose port 5000 to allow external connections to the application
EXPOSE 5000

# Define the default command to run when the container starts
# This command starts the Python application by executing the app.py script
CMD ["python", "app.py"]
