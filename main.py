import boto3
import base64
import json
import uuid


# Initialize clients with your preferred region
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

BUCKET_NAME = 'sahil.k-bucket-store-generated-image-bedrock'

def generate_and_store_image(prompt):
    try:
        unique_id = uuid.uuid4().hex
        s3_key = f"generated-images/{unique_id}.jpg"
        # Use Amazon Titan Image Generator (cheaper alternative)
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