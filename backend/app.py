from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AWS S3 Configuration
AWS_ACCESS_KEY = "AKIAXBZV5WXIOTQ6BNVX" 
AWS_SECRET_KEY = "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"  
AWS_BUCKET_NAME = "dart-detect-images"  
AWS_REGION = "eu-north-1"

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Endpoint to generate a pre-signed URL
@app.route("/get_presigned_url", methods=["GET"])
def get_presigned_url():
    try:
        # Get the filename from the query parameters
        filename = request.args.get("filename", "default.jpg")

        # Generate the pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": AWS_BUCKET_NAME,
                "Key": filename,
                "ContentType": "image/jpeg",
            },
            ExpiresIn=3600,  # URL expires in 1 hour
        )

        return jsonify({"url": presigned_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



   # Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)