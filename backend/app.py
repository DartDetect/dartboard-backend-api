from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from PIL import Image
import io
import torch
from backend.models.dart_score import calculate_dart_score
from backend.models.load_model import load_yolov5_model # Import the load_yolov5_model function

from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

#Load Model on Server Startup
model = load_yolov5_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "dart-detect-images")
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")


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
        content_type = request.args.get("content_type", "image/jpeg")  # Default to image/jpeg

        # Generate the pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": AWS_BUCKET_NAME,
                "Key": filename,
                "ContentType": content_type,
            },
            ExpiresIn=3600,  # URL expires in 1 hour
        )

        return jsonify({"url": presigned_url}), 200 # Return error message with status code 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 # Return error message with status code 500

    # Endpoint to retrieve and process the image from S3
@app.route("/process_image", methods=["POST"])
def process_image():
    try:
        # Get the filename from the JSON payload
        data = request.get_json()
        filename = data.get("filename")

        if not filename:
            return jsonify({"error": "Filename is required"}), 400

        # Retrieve the image from S3
        s3_object = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=filename)
        image_data = s3_object["Body"].read()

        # Process the image (PIL format)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Run YOLOv5 inference 
        results = model(image)

        # Extract detectiopn results
        detections= results.pandas().xyxy[0].to_dict(orient='records')
        print("🔍 Full Detections:", detections)  # Print full detections for debugging

         # Identify Dart, Dartboard, and Bull
        dartboard = None
        bull = None
        darts = []

        for obj in detections:
            if obj["name"] == "Dartboard":
                dartboard = obj
            elif obj["name"] == "Bull":
                bull = obj
            elif obj["name"] == "Dart":
                darts.append(obj)

         # Ensure dartboard is detected before calculating score
        if not dartboard:
            return jsonify({"error": "Dartboard not detected, cannot calculate score"}), 400
        
        # Calculate score for each dart
        scores = []
        for dart in darts:
            score = calculate_dart_score(dartboard, dart, bull)
            scores.append({"dart": dart, "score": score})


       
        # Yolo model will be used it
        ##calculated_score = 100  # Placeholder score for mock demo

        # Respond with detected objects
        return jsonify({
            "message": "Image received and processed successfully.",
            "filename": filename,
            "detections": detections,
            "scores": scores
        }), 200

        # # Respond to the client
        # return jsonify({
        #     "message": "Image received and processed successfully.",
        #     "filename": filename,
        #     "score": calculated_score  # Mock calulcated score
        # }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

   # Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)