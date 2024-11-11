# app.py
import streamlit as st
from utils import auth

# Streamlit app
st.title("Firebase Authentication with Streamlit")

# Display the GitHub login button
sign_in_url = auth.github_auth(st.session_state)
st.write(f"Click here to sign in with GitHub: <a href='{sign_in_url}'>Sign In</a>", unsafe_allow_html=True)

# Handle the callback
if 'code' in st.session_state:
    uid = auth.handle_callback(st.session_state)
    st.write(f"Welcome, you are logged in as {uid}!")

    # Allow user to upload a JSON file
    uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])
    if uploaded_file is not None:
        try:
            # Upload the file to Firebase Storage
            message = auth.upload_json(uid, uploaded_file)
            st.success(message)
        except Exception as e:
            st.error(f"Error uploading file: {e}")

# Display a logout button
if 'uid' in st.session_state:
    if st.button("Logout"):
        del st.session_state['uid']
        st.write("Logged out successfully.")