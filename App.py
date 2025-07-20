import boto3
import pymysql
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import gradio as gr
import os

# AWS S3 Configuration
BUCKET_NAME = "bertfinalproject"
MODEL_S3_FOLDER = "fine_tuned_distilbert/"
LOCAL_MODEL_DIR = "/home/ec2-user/fine_tuned_distilbert/"

# RDS Configuration
RDS_HOST = "database-2.crqqsumuy6iy.ap-south-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "ArchanaRuban"
RDS_DB = "user_logs"

def download_model_from_s3():
    try:
        session = boto3.Session()
        s3 = session.client("s3")

        # Debugging: Check if session credentials are None
        credentials = session.get_credentials()
        if credentials is None:
            raise Exception("No credentials found. Ensure IAM role is properly attached and has the necessary permissions.")
        else:
            print("Session credentials are available.")

        response = s3.list_buckets()
        print("Buckets:", [bucket['Name'] for bucket in response['Buckets']])

        if not os.path.exists(LOCAL_MODEL_DIR):
            os.makedirs(LOCAL_MODEL_DIR)

        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=MODEL_S3_FOLDER)
        if 'Contents' not in response:
            raise Exception(f"No files found in S3 folder: {MODEL_S3_FOLDER}")

        for obj in response['Contents']:
            s3_file_path = obj['Key']
            file_name = os.path.basename(s3_file_path)
            local_file_path = os.path.join(LOCAL_MODEL_DIR, file_name)

            if not file_name:
                continue

            s3.download_file(BUCKET_NAME, s3_file_path, local_file_path)
            print(f"Downloaded: {file_name} to {local_file_path}")
    except Exception as e:
        print(f"Error downloading model from S3: {e}")
        raise

# Download and organize model files
download_model_from_s3()

# Load the pre-trained model and tokenizer
MODEL_PATH = LOCAL_MODEL_DIR
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, trust_remote_code=True)
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    raise

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"Error connecting to RDS: {e}")
        raise

def log_prediction_to_rds(text, predicted_class, negative, neutral, positive, ip_address):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO APP_USER_LOGS (Text, Predicted_class, Negative, Neutral, Positive, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (text, predicted_class, negative, neutral, positive, ip_address))
    except Exception as e:
        print(f"Error logging to RDS: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def predict_sentiment(text, request: gr.Request):
    try:
        ip_address = request.client.host
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs, dim=1).item() + 1
        neutral, positive, negative = probs[0].tolist()
        result = {
            "Predicted Class": predicted_class,
            "Negative": round(negative, 4),
            "Neutral": round(neutral, 4),
            "Positive": round(positive, 4),
        }
        log_prediction_to_rds(text, predicted_class, negative, neutral, positive, ip_address)
        return result
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": str(e)}

iface = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(lines=2, placeholder="Enter tweets here..."),
    outputs=gr.JSON(),
    title="Twitter Tweets Sentiment Analysis",
    description="Enter Tweets and get the predicted sentiment class and probabilities.",
)

iface.launch(share=True)
