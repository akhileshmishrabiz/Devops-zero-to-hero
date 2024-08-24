#!/bin/bash

# Define the S3 bucket name
S3_BUCKET="inbound-bucket-custome"

# Create 10 files with the format filename-randomnumber-yyyy-mm-dd
for i in {1..10}; do
    RANDOM_NUMBER=$((1 + RANDOM % 1000))
    FILENAME="filename-$RANDOM_NUMBER-$(date +%Y-%m-%d).txt"
    echo "This is file number $i" > $FILENAME
    aws s3 cp $FILENAME s3://$S3_BUCKET/incoming/
done