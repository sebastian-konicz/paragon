import streamlit as st
from utils import auth_functions
import firebase_admin
from utils.receipt_preprocess import preprocess_receipts
from firebase_admin import credentials, storage
from config.config import FIREBASE_STORAGE_BUCKET
from config.config import (FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL,
                           FIREBASE_CLIENT_ID, FIREBASE_CLIENT_X509_CERT_URL, FIREBASE_STORAGE_BUCKET)

FIREBASE_PRIVATE_KEY_AMD = FIREBASE_PRIVATE_KEY.replace("\\n", "\n")

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": FIREBASE_PROJECT_ID,
        "private_key_id": FIREBASE_PRIVATE_KEY_ID,
        "private_key": FIREBASE_PRIVATE_KEY_AMD,
        "client_email": FIREBASE_CLIENT_EMAIL,
        "client_id": FIREBASE_CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": FIREBASE_CLIENT_X509_CERT_URL
    })
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE_BUCKET
    })

# Initialize Firebase storage with the bucket name
bucket = storage.bucket()

def upload_file_to_firebase(file, user_id):
    blob = bucket.blob(f"{user_id}/{file.name}")
    if blob.exists():
        st.warning(f"File {file.name} already exists and was not uploaded.")
    else:
        blob.upload_from_string(file.getvalue(), content_type="application/json")
        st.success(f"File {file.name} uploaded successfully!")

def list_user_files(user_id):
    blobs = bucket.list_blobs(prefix=f"{user_id}/")
    return [blob.name.split('/')[-1] for blob in blobs]

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?', options=('Yes', 'No', 'I forgot my password'))
    auth_form = col2.form(key='Authentication form', clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password', type='password') if do_you_have_an_account in {'Yes', 'No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email, password)

    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email, password)

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Show user information
    st.header('User information:')
    st.write(st.session_state.user_info)

    # File upload section
    st.header('Upload JSON files:')
    uploaded_files = st.file_uploader("Upload JSON files", type="json", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            upload_file_to_firebase(uploaded_file, st.session_state.user_info['localId'])

    # List all user files
    user_files = list_user_files(st.session_state.user_info['localId'])

    # File selection for processing
    st.header('Select files to process:')
    selected_files = st.multiselect("Select files to process", user_files)

    if st.button("Process Selected Files"):
        if selected_files:
            files_to_process = [bucket.blob(f"{st.session_state.user_info['localId']}/{file}").download_as_string().decode('utf-8') for file in selected_files]
            processed_data = preprocess_receipts(files_to_process)
            st.write(processed_data)
        else:
            st.warning("No files selected for processing.")

    # Sign out
    st.header('Sign out:')
    st.button(label='Sign Out', on_click=auth_functions.sign_out, type='primary')

    # Delete Account
    st.header('Delete account:')
    password = st.text_input(label='Confirm your password', type='password')
    st.button(label='Delete Account', on_click=auth_functions.delete_account, args=[password], type='primary')