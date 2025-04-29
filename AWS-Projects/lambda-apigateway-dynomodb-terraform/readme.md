


# Get the API URL from Terraform output
API_URL=$(terraform output -raw api_gateway_url)

# Create a short URL
curl -X POST $API_URL/urls \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

# The response will include a shortId - use it to test the redirect
# Visit in browser: $API_URL/{shortId}

# List all URLs
curl $API_URL/urls