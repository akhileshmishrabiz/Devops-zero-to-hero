output "api_gateway_url" {
  description = "Base URL for API Gateway stage"
  value       = "${aws_api_gateway_deployment.url_shortener_deployment.invoke_url}"
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.url_shortener_table.name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.url_shortener_lambda.function_name
}