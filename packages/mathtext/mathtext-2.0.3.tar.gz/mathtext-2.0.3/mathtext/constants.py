import boto3
import json
import os

from dotenv import load_dotenv
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()  # run the .env file that contains environment variable definitions

try:
    DATA_DIR = Path(__file__).parent / "data"
except NameError:
    DATA_DIR = Path.cwd() / "mathtext" / "data"

try:
    assert DATA_DIR.is_dir()
except AssertionError:
    DATA_DIR.mkdir()


TOKENS2INT_ERROR_INT = 32202

# Current model information
CURRENT_MODEL_VERSION = os.environ.get("CURRENT_MODEL_VERSION")
CURRENT_MODEL_FILENAME = os.environ.get("CURRENT_MODEL_FILENAME")
CURRENT_MODEL_LINK = f"{CURRENT_MODEL_VERSION}/{CURRENT_MODEL_FILENAME}"

# Public Google Sheet Id for model training data
CSV_GOOGLE_SHEET_ID = os.environ.get("CSV_GOOGLE_SHEET_ID")
GOOGLE_SHEET_LINK = (
    f"https://docs.google.com/spreadsheets/d/{CSV_GOOGLE_SHEET_ID}/export?format=csv"
)


# Object storage information
def set_client_session(creds_json):
    session = boto3.session.Session()

    # Create a connection to the Space
    client = session.client(
        "s3",
        endpoint_url=creds_json["endpoint_url"],
        region_name=creds_json["region_name"],
        aws_access_key_id=creds_json["aws_access_key_id"],
        aws_secret_access_key=creds_json["aws_secret_access_key"],
    )
    return client


OBJECT_STORAGE_CLIENT = ""
OBJECT_STORAGE_PROVIDER = os.environ.get("OBJECT_STORAGE_PROVIDER")
OBJECT_STORAGE_NAME = os.environ.get("OBJECT_STORAGE_NAME")

if OBJECT_STORAGE_PROVIDER == "gcs":
    GOOGLE_APPLICATION_CREDENTIALS_JSON = json.loads(
        os.environ.get("GOOGLE_CLOUD_MODEL_SERVICE_AGENT_CREDENTIALS_JSON", "")
    )
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_APPLICATION_CREDENTIALS_JSON
    )
    OBJECT_STORAGE_CLIENT = storage.Client(credentials=credentials)

elif OBJECT_STORAGE_PROVIDER == "s3":
    DIGITAL_OCEAN_OBJECT_STORAGE_CREDENTIALS_JSON = json.loads(
        os.environ.get("DIGITAL_OCEAN_OBJECT_STORAGE_CREDENTIALS_JSON")
    )
    OBJECT_STORAGE_CLIENT = set_client_session(
        DIGITAL_OCEAN_OBJECT_STORAGE_CREDENTIALS_JSON
    )
