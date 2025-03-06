# Image Generation & Storage with Amazon Bedrock and S3

This project demonstrates how to generate images using Amazon Bedrock's Titan Image Generator model, store the generated images in an Amazon S3 bucket, and return a publicly accessible URL for the uploaded image.

---

## 📋 Prerequisites

1. **AWS Account**: 
   - Access to the `amazon.titan-image-generator-v1` model in the `us-east-1` region.
   - **IAM User**: 
     - Permissions for Amazon Bedrock and S3 (full access recommended for testing).
     - Access key and secret key configured via AWS CLI.

2. **AWS CLI**: 
   - [Installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configured with `aws configure`.

3. **Python 3.7+**: 
   - Ensure Python and `venv` are installed.

---

## 🛠️ Setup Instructions

### 1. Configure S3 Bucket Permissions
- **Disable Block Public Access**:
  1. Navigate to your S3 bucket > **Permissions**.
  2. Uncheck all 4 options under **Block Public Access**.
- **Apply Bucket Policy**:
  Replace `YOUR_BUCKET_NAME` in the policy below and add it to your bucket:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "S3:GetObject",
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        }
    ]
  }

🚀 Run This Script

Follow these simple steps to get the project up and running locally.

🛠 Setup

1. Clone the Repository

git clone <repo-url>
cd <repo-folder>

2. Create a Virtual Environment

python -m venv venv

3. Activate the Virtual Environment

On Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt

▶️ Run the Script

python main.py

⚠️ Important: Update Your S3 Bucket Name

Before running the script, make sure to update the S3 bucket name in the code to match your actual bucket.

