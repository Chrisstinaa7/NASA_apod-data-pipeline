import json
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# ---- Config ----
CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
RAW_CONTAINER = os.getenv("AZURE_RAW_CONTAINER")
PROCESSED_CONTAINER = os.getenv("AZURE_PROCESSED_CONTAINER")
RAW_BLOB = os.getenv( "AZURE_RAW_BLOB ")
PROCESSED_BLOB = os.getenv("AZURE_PROCESSED_BLOB")

def process_nasa_data():
    """Download raw NASA APOD JSON, transform it, and upload processed JSON."""
    
    # ---- Connect to Azure ----
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Make sure processed container exists
    try:
        blob_service_client.create_container(PROCESSED_CONTAINER)
        print(f"[OK] Container '{PROCESSED_CONTAINER}' created.")
    except Exception:
        print(f"[OK] Container '{PROCESSED_CONTAINER}' already exists.")

    # Download raw JSON from blob
    raw_blob_client = blob_service_client.get_blob_client(container=RAW_CONTAINER, blob=RAW_BLOB)
    raw_data = raw_blob_client.download_blob().readall()
    apod = json.loads(raw_data)

    # Transform data (keep only important fields)
    processed_data = {
        "title": apod.get("title"),
        "date": apod.get("date"),
        "explanation": apod.get("explanation"),
        "url": apod.get("url")
    }

    # Save locally
    with open("apod_processed.json", "w") as f:
        json.dump(processed_data, f, indent=4)

    print("[OK] Processed data saved locally as apod_processed.json")

    # Upload processed JSON to another container
    processed_blob_client = blob_service_client.get_blob_client(
        container=PROCESSED_CONTAINER,
        blob=PROCESSED_BLOB
    )
    with open("apod_processed.json", "rb") as f:
        processed_blob_client.upload_blob(f, overwrite=True)

    print(f"[OK] Processed data uploaded to Azure Blob Storage ({PROCESSED_CONTAINER}/{PROCESSED_BLOB})")


if __name__ == "__main__":
    process_nasa_data()
