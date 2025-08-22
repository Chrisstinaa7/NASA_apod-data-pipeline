import json
import csv
import io
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# ---- Config ----
CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
PROCESSED_CONTAINER = os.getenv("AZURE_PROCESSED_CONTAINER")
CURATED_CONTAINER = os.getenv("AZURE_CURATED_CONTAINER")
PROCESSED_BLOB = os.getenv("AZURE_PROCESSED_BLOB")
CURATED_BLOB = os.getenv("AZURE_CURATED_BLOB")

def curate_nasa_data():
    # ---- Connect to Azure ----
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Make sure curated container exists
    container_client = blob_service_client.get_container_client(CURATED_CONTAINER)
    try:
        container_client.create_container()
        print(f"[OK] Container '{CURATED_CONTAINER}' created.")
    except:
        print(f"[OK] Container '{CURATED_CONTAINER}' already exists.")

    # Download processed JSON
    try:
        processed_blob_client = blob_service_client.get_blob_client(container=PROCESSED_CONTAINER, blob=PROCESSED_BLOB)
        processed_data = processed_blob_client.download_blob().readall()
        apod = json.loads(processed_data)
    except Exception as e:
        print(f"[ERROR] Downloading processed JSON: {e}")
        return

    # Download existing curated CSV from Blob (if it exists)
    existing_rows = []
    try:
        curated_blob_client = blob_service_client.get_blob_client(container=CURATED_CONTAINER, blob=CURATED_BLOB)
        csv_data = curated_blob_client.download_blob().readall().decode('utf-8')
        reader = csv.DictReader(io.StringIO(csv_data))
        existing_rows = list(reader)
        print(f"[OK] Existing curated CSV loaded with {len(existing_rows)} rows")
    except Exception as e:
        print(f"[INFO] No existing CSV found. Creating new one.")

    # Check if today's APOD is already in CSV (avoid duplicates)
    if any(row["date"] == apod["date"] for row in existing_rows):
        print(f"[INFO] Today's APOD already exists in curated CSV")
    else:
        existing_rows.append(apod)

    # Write updated CSV locally
    try:
        with open("apod_curated.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "date", "explanation", "url"])
            writer.writeheader()
            writer.writerows(existing_rows)
        print(f"[OK] Curated CSV saved locally with {len(existing_rows)} rows")
    except Exception as e:
        print(f"[ERROR] Writing CSV: {e}")
        return

    # Upload curated CSV back to Blob
    try:
        with open("apod_curated.csv", "rb") as f:
            curated_blob_client.upload_blob(f, overwrite=True)
        print(f"[OK] Curated CSV uploaded to Azure Blob Storage ({CURATED_CONTAINER}/{CURATED_BLOB})")
    except Exception as e:
        print(f"[ERROR] Uploading CSV: {e}")

if __name__ == "__main__":
    curate_nasa_data()
