# What is it?
Generating an image using Amazon Bedrock, storing it in S3, and returning the URL of the uploaded image for access.

## Requirements
AWS account with access to bedrock models (amazon.titan-image-generator-v1) in us-east-1

IAM user with appropriate permissions to access models and S3 

The IAM user access key and secret key to configure the AWS CLI and permissions

AWS CLI installed and configured

## Overview 
Generate image using Amazon bedrock model.

Convert image into binary format. 

Model gives us image in base64 while s3 requires binary format.

Make your s3 available to public reads by giving appropriate access.

## Important
Change your s3 bucket policy 
Uncheck all 4 public access to s3
Add this policy after 
```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "S3:GetObject",
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        }
    ]
}
```

# Steps/Actions

## Creat a python file
create  python file named main.py or any other name

## Creating virtual environment in python

Use virtual environment to maintain packages across different projects

```bash
python -m venv venv
```

Activate virtual Enviroment

```bash
venv\Script\activate
```

## Installation of Boto3

Installing boto3 on our virtual environment

```bash
pip install boto3
```

## Code

```python
import boto3
import base64
import json
import uuid

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

BUCKET_NAME = 'YOUR_BUCKET_NAME'

def generate_and_store_image(prompt):
    try:
        unique_id = uuid.uuid4().hex
        s3_key = f"generated-images/{unique_id}.jpg"
        # Use Amazon Titan Image Generator 
        response = bedrock.invoke_model(
            modelId='amazon.titan-image-generator-v1',
            body=json.dumps({
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt,
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "quality": "standard",  # 'premium' for higher quality
                    "width": 1024,
                    "height": 1024,
                    "cfgScale": 8.0,
                    "seed": 42
                }
            }),
            contentType="application/json",
            accept="application/json"
        )

        # Parse Titan response
        response_body = json.loads(response['body'].read())
        base64_image = response_body['images'][0]

        # Convert and upload
        image_bytes = base64.b64decode(base64_image)
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )

        print(f"https://s3.us-east-1.amazonaws.com/{BUCKET_NAME}/{s3_key}")
        return f"https://s3.us-east-1.amazonaws.com/{BUCKET_NAME}/{s3_key}"

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

# Usage example
generate_and_store_image(
    prompt="picture of a Husky"
)
```

## Run File 

```bash
python [NAME_OF_FILE].py
```

## OUTPUT
```bash
https://s3.us-east-1.amazonaws.com/sahil.k-bucket-store-generated-image-bedrock/generated-images/3f36af6482704821aee49b9715097456.jpg
```
## Steps




