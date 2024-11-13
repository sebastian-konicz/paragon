from config.config import FIREBASE_STORAGE_BUCKET
from firebase_admin import storage

# Inicjalizacja Firebase Storage
bucket_name = FIREBASE_STORAGE_BUCKET
bucket = storage.bucket(bucket_name)

from google.cloud import storage

def upload_file(file, file_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(file.getvalue(), content_type=file.type)
    return f"File uploaded to gs://{bucket_name}/{file_name}"