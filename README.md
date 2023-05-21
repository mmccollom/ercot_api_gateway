# ERCOT API Gateway
This repository contains multiple functions that are used to retrieve ERCOT data from S3. The Lambda Functions
are deployed as a serverless application via AWS SAM and are triggered by an API Gateway. Each Lambda Function 
responds with a dictionary containing the requested data.

### Getting Started
Adjust the s3 paths accordingly in the main.py script for each Lambda Function directory.

### Deploying
This project has been set up to be deployed as a serverless application via SAM. To deploy the application, run the following command (AWS account and AWS SAM CLI required):
```
sam build
sam deploy --guided
```

### License
This project is licensed under the MIT License