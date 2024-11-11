from config.config import FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin import storage

FIREBASE_PRIVATE_KEY_AMD = FIREBASE_PRIVATE_KEY.replace("\\n", "\n")

# Inicjalizacja Firebase z kluczem usługi
firebase_cred = credentials.Certificate({
    "type": "service_account",
    "project_id": FIREBASE_PROJECT_ID,
    "private_key": FIREBASE_PRIVATE_KEY_AMD,
    "client_email": FIREBASE_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token"
})

firebase_admin.initialize_app(firebase_cred)

# Function to handle GitHub authentication
def github_auth(request):
    # Get the GitHub OAuth provider
    github_provider = auth.GithubAuthProvider()
    # Generate a sign-in URL
    sign_in_url = github_provider.get_sign_in_url(callback_url='http://localhost:8501/callback')  # Replace with your callback URL
    return sign_in_url

# Function to handle the callback
def handle_callback(request):
    # Exchange the code for an ID token
    id_token = auth.GithubAuthProvider().get_credential(request.args.get('code')).id_token
    # Verify the ID token
    decoded_token = auth.verify_id_token(id_token)
    # Get the user's UID
    uid = decoded_token['uid']
    # Return the UID
    return uid

# Function to upload a JSON file to Firebase Storage
def upload_json(uid, file):
    # Get the Firebase Storage bucket
    bucket = storage.bucket()
    # Create a blob object
    blob = bucket.blob(f'{uid}/uploaded_file.json')
    # Upload the file
    blob.upload_from_string(file.read(), content_type='application/json')
    # Return a success message
    return 'File uploaded successfully!'