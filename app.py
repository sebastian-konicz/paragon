import streamlit as st
from utils.auth import github_login
from utils.storage import upload_file


# Tytuł aplikacji
st.title("GitHub Authentication and File Upload")

# Inicjalizacja stanu sesji
if "login_status" not in st.session_state:
    st.session_state.login_status = "not_logged_in"

# Obsługa procesu logowania przez GitHub
if st.session_state.login_status == "not_logged_in":
    if st.button("Login with GitHub"):
        # Przekierowanie do logowania GitHub
        github_login()
        st.session_state.login_status = "redirecting"  # Ustawienie statusu przekierowania

elif st.session_state.login_status == "redirecting":
    st.write("Redirecting to GitHub...")

elif st.session_state.login_status == "success":
    # Powitanie użytkownika po udanym logowaniu
    st.write(f"Welcome, {st.session_state.user_data['display_name']}!")

    # Sekcja przesyłania pliku
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    if uploaded_file is not None:
        try:
            # Nazwa pliku i zasobnika
            file_name = uploaded_file.name

            # Wysłanie pliku do zasobnika
            result = storage.upload_file(uploaded_file, file_name)
            st.success(f"File '{file_name}' successfully uploaded.")
        except Exception as e:
            st.error(f"Error uploading file: {e}")

# Obsługa błędów logowania
if st.session_state.login_status.startswith("Error"):
    st.error(f"Login failed: {st.session_state.login_status}")