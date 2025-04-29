# Use the official Node.js image based on Alpine Linux
FROM node:latest as build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the application (if necessary)
# RUN npm run build

# ----------------------------------------------
# Second Stage: Create a smaller image for production
# ----------------------------------------------

# Use a smaller base image (Alpine Linux)
FROM node:alpine

# Set a non-root user for better security
RUN adduser -D appuser
USER appuser

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files from the previous build stage
COPY --from=build /app .

# Expose the port your application will run on
EXPOSE 3000

# Set default environment variables (if needed)
# ENV NODE_ENV=production

# Add a health check (modify as per your app's needs)
# HEALTHCHECK --interval=30s --timeout=30s CMD curl -f http://localhost:3000 || exit 1

# Define the command to run your application
CMD ["node", "app.js"]

