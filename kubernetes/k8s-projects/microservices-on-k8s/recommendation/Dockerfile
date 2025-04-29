# Use the official Go image based on Alpine Linux
FROM golang:1.20.10-alpine3.18

# Set the working directory inside the container
WORKDIR /app

# Copy the Go application code into the container
COPY . .

# Build the Go application
RUN go build -o app

# Expose port 8080 for the application
EXPOSE 8080

# Define the command to run the Go application
CMD ["./app"]
