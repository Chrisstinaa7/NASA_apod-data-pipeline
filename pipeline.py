import subprocess
import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Daily log filename
log_filename = datetime.now().strftime("logs/pipeline_%Y-%m-%d.log")

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# List of ETL steps in order
scripts = [
    "upload_nasa.py",
    "process_nasa.py",
    "curate_nasa.py"
]

def run_pipeline():
    logging.info("Starting NASA ETL Pipeline...")

    for script in scripts:
        logging.info(f"Running {script} ...")
        try:
            result = subprocess.run(
                ["python", script],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(result.stdout.strip())  # Save script output
        except subprocess.CalledProcessError as e:
            logging.error(f"Error in {script}: {e.stderr.strip()}")
            break  # Stop pipeline if one step fails

    logging.info("Pipeline finished.")

if __name__ == "__main__":
    run_pipeline()
