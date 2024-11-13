from config.config import FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL
import firebase_admin
from firebase_admin import auth, credentials
from streamlit import session_state as st_state

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

# Sprawdzenie, czy aplikacja już istnieje
if not firebase_admin._apps:
    firebase_admin.initialize_app(firebase_cred)

def github_login():
    """Handles GitHub login and sets user data in session state."""
    try:
        # Get the GitHub provider
        provider = auth.GithubAuthProvider.PROVIDER_ID

        # Redirect to GitHub for authentication
        redirect_uri = auth.generate_login_link(
            provider,
            return_to="http://localhost:8501/",  # Replace with your Streamlit app's URL
            state="some_state",
        )

        print(redirect_uri)
        st_state.redirect_url = redirect_uri
        st_state.login_status = "redirecting"

    except Exception as e:
        st_state.login_status = f"Error: {e}"

def handle_github_callback():
    """Handles the GitHub callback and sets user data in session state."""
    try:
        # Get the ID token from the URL
        id_token = st_state.redirect_url.split("?")[1].split("=")[1]

        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Get user data from Firebase
        user = auth.get_user(uid)
        st_state.user_data = {
            "uid": uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
        }
        st_state.login_status = "success"

    except Exception as e:
        st_state.login_status = f"Error: {e}"

if __name__ == "__main__":
    github_login()