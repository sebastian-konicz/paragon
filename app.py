import streamlit as st
from utils.auth import github_login, handle_github_callback
from config.config import FIREBASE_STORAGE_BUCKET
import os
import json
from firebase_admin import storage

# Initialize Firebase storage with the bucket name
bucket = storage.bucket(FIREBASE_STORAGE_BUCKET)

def upload_file_to_firebase(file, user_id):
    blob = bucket.blob(f"{user_id}/{file.name}")
    blob.upload_from_string(file.getvalue(), content_type="application/json")
    st.success(f"File {file.name} uploaded successfully!")

def main():
    st.title("Streamlit App with GitHub Login and Firebase Storage")

    query_params = st.experimental_get_query_params()

    if "page" in query_params and query_params["page"][0] == "upload":
        if "user_data" in st.session_state:
            st.write(f"Welcome, {st.session_state.user_data['display_name']}!")
            uploaded_files = st.file_uploader("Upload JSON files", type="json", accept_multiple_files=True)
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    upload_file_to_firebase(uploaded_file, st.session_state.user_data['uid'])
        else:
            st.error("You need to log in first.")
    else:
        if "login_status" not in st.session_state:
            st.session_state.login_status = None

        if st.session_state.login_status == "redirecting":
            st.write("Redirecting to GitHub for authentication...")
            st.markdown(f"[Click here to authenticate with GitHub]({st.session_state.redirect_url})")
            st.stop()

        if st.session_state.login_status == "success":
            st.experimental_set_query_params(page="upload")
            st.experimental_rerun()
        else:
            if st.button("Login with GitHub"):
                github_login()

        if st.session_state.login_status and "Error" in st.session_state.login_status:
            st.error(st.session_state.login_status)

        if "code" in query_params:
            code = query_params["code"][0]
            handle_github_callback(code)
            st.experimental_set_query_params(page="upload")
            st.experimental_rerun()

if __name__ == "__main__":
    main()