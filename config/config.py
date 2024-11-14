import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z .env
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USDA_API_KEY = os.getenv("USDA_API_KEY")

FIREBASE_API_KEY= os.getenv("FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN= os.getenv("FIREBASE_AUTH_DOMAIN")
FIREBASE_PROJECT_ID= os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_STORAGE_BUCKET= os.getenv("FIREBASE_STORAGE_BUCKET")
FIREBASE_CLIENT_EMAIL= os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_CLIENT_ID= os.getenv("FIREBASE_CLIENT_ID")
FIREBASE_PRIVATE_KEY_ID= os.getenv("FIREBASE_PRIVATE_KEY_ID")
FIREBASE_PRIVATE_KEY= os.getenv("FIREBASE_PRIVATE_KEY")
FIREBASE_CLIENT_X509_CERT_URL=os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# Opcjonalnie: Rzucaj wyjątkiem, jeśli klucz nie jest ustawiony
if not all([OPENAI_API_KEY]):
    raise ValueError("Brakuje danych uwierzytelniających do OpenAI. Sprawdź plik .env.")