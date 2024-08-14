#!/bin/bash

# Define the payload1
payload=$(echo -n '{  "project_name": "lambda_test", "keyfile_extension2": "txt"}' | base64)

# Invoke the Lambda function
response=$(aws lambda invoke --function-name new_project --payload "$payload" output.txt)

# Check if the function executed successfully
if grep -q "FunctionError" <<< "$response"; then
  echo "Test failed: Function error"
  exit 1
fi

# Read the response from the output file
result=$(cat output.txt)

# Expected result
expected_result='{"statusCode": 200, "body": "Project created successfully", '

# Check if the result matches the expected result
if [[ $result == $expected_result* ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed: Unexpected response"
  exit 1
fi
