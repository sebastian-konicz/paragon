# auth.py
from config.config import FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL, FIREBASE_STORAGE_BUCKET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
import firebase_admin
from firebase_admin import auth, credentials, storage
from streamlit import session_state as st_state
import requests

FIREBASE_PRIVATE_KEY_AMD = FIREBASE_PRIVATE_KEY.replace("\\n", "\n")

# Initialize Firebase with service account key and storage bucket
firebase_cred = credentials.Certificate({
    "type": "service_account",
    "project_id": FIREBASE_PROJECT_ID,
    "private_key": FIREBASE_PRIVATE_KEY_AMD,
    "client_email": FIREBASE_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token"
})

if not firebase_admin._apps:
    firebase_admin.initialize_app(firebase_cred, {
        'storageBucket': FIREBASE_STORAGE_BUCKET
    })

def github_login():
    """Redirects to GitHub for authentication."""
    redirect_uri = "http://localhost:8501/callback"  # Replace with your Streamlit app's callback URL
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=read:user"
    st_state.redirect_url = github_auth_url
    st_state.login_status = "redirecting"

def handle_github_callback(code):
    """Handles the GitHub callback and creates a Firebase custom token."""
    try:
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        }
        headers = {"Accept": "application/json"}
        token_response = requests.post(token_url, data=token_data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Get user info from GitHub
        user_info_url = "https://api.github.com/user"
        user_info_response = requests.get(user_info_url, headers={"Authorization": f"token {access_token}"})
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        # Create a custom token for Firebase
        uid = f"github:{user_info['id']}"
        custom_token = auth.create_custom_token(uid)

        # Verify the custom token and set user data in session state
        decoded_token = auth.verify_id_token(custom_token)
        st_state.user_data = {
            "uid": uid,
            "email": user_info.get("email"),
            "display_name": user_info.get("name"),
            "photo_url": user_info.get("avatar_url"),
        }
        st_state.login_status = "success"
    except Exception as e:
        st_state.login_status = f"Error: {e}"