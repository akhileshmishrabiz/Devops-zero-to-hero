# app.py
import os
import json
import boto3
import string
import random
from datetime import datetime
from flask import Flask, request, redirect, jsonify
from flask_lambda import FlaskLambda

# Initialize Flask application
app = FlaskLambda(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'url-shortener-table'))

# Generate a random short ID (you could use a library like nanoid instead)
def generate_short_id(length=7):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/urls', methods=['POST'])
def create_short_url():
    try:
        # Get the original URL from request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        # Generate a unique short ID
        short_id = generate_short_id()
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Store the mapping in DynamoDB
        table.put_item(
            Item={
                'shortId': short_id,
                'originalUrl': original_url,
                'createdAt': timestamp,
                'hits': 0
            }
        )
        
        # Build the short URL
        domain_name = request.headers.get('Host', 'localhost')
        stage = os.environ.get('STAGE', 'dev')
        short_url = f"https://{domain_name}/{stage}/{short_id}"
        
        return jsonify({
            'shortId': short_id,
            'shortUrl': short_url,
            'originalUrl': original_url
        }), 201
        
    except Exception as e:
        print(f"Error creating short URL: {str(e)}")
        return jsonify({'error': 'Could not create short URL'}), 500

@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    try:
        # Look up the original URL in DynamoDB
        response = table.get_item(
            Key={
                'shortId': short_id
            }
        )
        
        # Check if the URL exists
        if 'Item' not in response:
            return jsonify({'error': 'URL not found'}), 404
        
        original_url = response['Item']['originalUrl']
        
        # Update hit counter
        table.update_item(
            Key={
                'shortId': short_id
            },
            UpdateExpression='ADD hits :inc',
            ExpressionAttributeValues={
                ':inc': 1
            }
        )
        
        # Redirect to the original URL
        return redirect(original_url, code=302)
        
    except Exception as e:
        print(f"Error redirecting: {str(e)}")
        return jsonify({'error': 'Could not redirect to URL'}), 500

@app.route('/urls', methods=['GET'])
def list_urls():
    try:
        # Scan DynamoDB table for all URLs (with limit)
        response = table.scan(
            Limit=50
        )
        
        return jsonify(response.get('Items', [])), 200
        
    except Exception as e:
        print(f"Error listing URLs: {str(e)}")
        return jsonify({'error': 'Could not list URLs'}), 500

# Lambda handler
if __name__ == '__main__':
    app.run(debug=True)