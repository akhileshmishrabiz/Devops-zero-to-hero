#!/bin/bash

# Create a temporary directory
mkdir -p temp
cd temp

# Copy the application code
cp -r ../app/* .

# Install dependencies
pip install -r requirements.txt -t .

# Create the zip file
zip -r ../terraform/lambda.zip .

# Clean up
cd ..
rm -rf temp

echo "Lambda package created at terraform/lambda.zip"