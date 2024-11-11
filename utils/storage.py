from config.config import FIREBASE_STORAGE_BUCKET
from firebase_admin import storage

# Inicjalizacja Firebase Storage
bucket_name = FIREBASE_STORAGE_BUCKET
bucket = storage.bucket(bucket_name)

def upload_file_to_storage(file, user_id):
    file_path = f"{user_id}/{file.name}"
    blob = bucket.blob(file_path)

    # Przesyłanie pliku do Firebase Storage
    blob.upload_from_file(file)

    # Uzyskanie publicznego URL pliku
    file_url = blob.public_url
    return file_url