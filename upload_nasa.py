import requests
import json
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Configurations
API_KEY = os.getenv("AZURE_STORAGE_KEY")
NASA_URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"

CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_RAW_CONTAINER")
BLOB_NAME = os.getenv( "AZURE_RAW_BLOB ")


def fetch_nasa_data():
    """Fetch data from NASA API"""
    response = requests.get(NASA_URL)
    response.raise_for_status()  # raise error if API fails
    return response.json()


def save_local(data, filename="apod.json"):
    """Save data locally as JSON"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[OK] NASA data saved locally as {filename}")


def upload_to_blob(filename="apod.json"):
    """Upload file to Azure Blob Storage"""
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

    with open(filename, "rb") as data_file:
        blob_client.upload_blob(data_file, overwrite=True)

    print(f"[OK] NASA data uploaded to Azure Blob Storage ({CONTAINER_NAME}/{BLOB_NAME})")


def main():
    try:
        data = fetch_nasa_data()
        save_local(data)
        upload_to_blob()
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
