# Paragon [prof of concept]

## Overview
This project is a web application that allows users to upload JSON files to Firebase Storage, manage their accounts, and process uploaded files. The application is built using Streamlit and Firebase.

## Features
- User authentication (sign in, sign up, password reset)
- Upload JSON files to Firebase Storage with metadata
- List and process uploaded files
- User account management (sign out, delete account)

## Installation

### Prerequisites
- Python 3.8 or higher
- Firebase account and project setup

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables to the `.env` file:
        ```env
        PINECONE_API_KEY="your_pinecone_api_key"
        OPENAI_API_KEY="your_openai_api_key"
        FIREBASE_API_KEY="your_firebase_api_key"
        FIREBASE_AUTH_DOMAIN="your_firebase_auth_domain"
        FIREBASE_PROJECT_ID="your_firebase_project_id"
        FIREBASE_STORAGE_BUCKET="your_firebase_storage_bucket"
        FIREBASE_CLIENT_ID="your_firebase_client_id"
        FIREBASE_CLIENT_EMAIL="your_firebase_client_email"
        FIREBASE_PRIVATE_KEY_ID="your_firebase_private_key_id"
        FIREBASE_PRIVATE_KEY="your_firebase_private_key"
        FIREBASE_CLIENT_X509_CERT_URL="your_firebase_client_x509_cert_url"
        ```

## Usage
1. Run the Streamlit application:
    ```sh
    streamlit run app_new.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

## Project Structure
- `app_new.py`: Main application file.
- `utils/`: Directory containing utility functions.
  - `auth_functions.py`: Functions for user authentication.
  - `receipt_preprocess.py`: Functions for processing uploaded files.
- `config/`: Directory containing configuration files.
  - `config.py`: Configuration settings for Firebase and other services.
- `.env`: Environment variables file (not included in the repository).

## Dependencies
The project dependencies are listed in the `requirements.txt` file. Some of the key dependencies include:
- `streamlit`
- `firebase-admin`
- `requests`

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact
For any questions or inquiries, please contact sebastian.konicz@gmail.com.