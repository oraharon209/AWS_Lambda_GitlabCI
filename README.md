# AWS Lambda with GitLab CI

## Overview

This repository contains a collection of AWS Lambda functions, each managed using GitLab CI for continuous integration and deployment. The project is structured to automate the testing, deployment, and updating of AWS Lambda functions, ensuring a streamlined and efficient CI/CD process. Additionally, you can host the index.html file in the webpage folder to trigger each function via a web interface.

## Features

- **Automated CI/CD**: Each Lambda function is integrated with GitLab CI, enabling automated testing and deployment.
- **Modular Design**: Each folder represents a standalone Lambda function, making it easy to manage and deploy individual functions.

## Prerequisites

Before you begin, ensure you have the following installed:

- **AWS CLI**: For managing AWS services from the command line.
- **GitLab CI/CD**: Set up in your GitLab repository to handle CI/CD pipelines.
- **Python 3.x**: Required for running locally.
- **Docker**: For containerizing the Lambda functions, if needed.

## Folder Structure

Each folder (except `webpage`) contains a distinct AWS Lambda function. Below is a brief description of each:

### 1. **create_gitlab_user** 

This Lambda function is responsible for creating Gitlab users from a google spreadsheet. Format your spreadsheet with 4 rows for `email, username, password, name`.

### 2. **new_project**

This function is designed to create a new project in Gitlab. Given a project name and a file extension.

### 3. **discord_notification**

This function is used to send a discord message. 

### 4. **csv_to_xlsx**

This function is used for converting CSV to XLSX(excel)

### 5. **get_info**

This Lambda function retrives information from Wikipedia and downloads the information to your device.

## CI/CD Pipeline

Each Lambda function in this repository is equipped with a `.gitlab-ci.yml` file that defines the CI/CD pipeline. The pipeline typically includes the following stages:

1. **Build**: The Lambda function is built and dependencies are installed.
2. **Test**: The function is tested to ensure it performs as expected.
3. **Deploy**: The function is deployed to AWS Lambda using the AWS CLI.

## Installation
1. **Clone the repository**:

    ```bash
    git clone https://github.com/oraharon209/AWS_Lambda_GitlabCI.git
    cd AWS_Lambda_GitlabCI
    ```

2. **Navigate to the desired Lambda function folder**:

    ```bash
    cd folder_name
    ```

3. **Deploy the Lambda function using GitLab CI**:

   - Push changes to the repository and GitLab CI will automatically trigger the pipeline.
   - Monitor the pipeline progress via the GitLab CI/CD interface.

## Setting Up the Web Interface

To trigger each Lambda function via a web interface, you can host the `index.html` file located in the `webpage` folder. Here’s how to do it:

- **Hosting on S3**:
  1. Upload the `index.html` file to an S3 bucket.
  2. Make the file publicly accessible.
  3. Enable static website hosting on the S3 bucket.
  4. Use the S3 bucket URL to access the web interface.

- **Hosting Locally**:
  1. Ensure your local environment can access AWS services.
  2. Serve the `index.html` file using a simple HTTP server (e.g., Python's `http.server` module).
  3. Open the file in your browser.

After hosting the file, update the API Gateway domain names in the `index.html` file to point to the correct Lambda functions.

## Environment Variables

Some of the Lambda functions may require environment variables to function correctly. You can set these in the AWS Lambda console under the "Configuration" tab for each function.
### 1. **create_gitlab_user** 
- **`GITLAB_SERVER`**: IP of your Gitlab server
- **`PRIVATE_TOKEN`**: Gitlab token

### 2. **new_project**
- **`GITLAB_SERVER`**: IP of your Gitlab server
- **`PRIVATE_TOKEN`**: Gitlab token

### 3. **discord_notification**
- **`DISCORD_URL`**: Discord webhook URL