# 🚀 NASA APOD Data Pipeline

This project demonstrates an **end-to-end ETL pipeline** built around NASA’s Astronomy Picture of the Day (APOD) API.  
The pipeline automates data collection, cleaning, and storage, and powers a **Power BI dashboard** for insights.

---

## 🛠 Tech Stack
- **Python** → ETL scripting
- **Azure Blob Storage** → Cloud storage for processed data
- **Windows Task Scheduler** → Automation
- **Power BI** → Visualization
  
---

## ⚙️ How It Works
1. Raw data is curated daily from NASA APOD API  
2. Data is cleaned, structured 
3. Final dataset is converted to CSV and uploaded to Azure Blob Storage  
4. Power BI consumes the cleaned dataset for visualization  

---

## 📊 Output 
- **Dashboard Preview:**  

![Power BI Dashboard](https://github.com/Chrisstinaa7/NASA_apod-data-pipeline/blob/main/dashboard/Screenshot%202025-08-22%20033848.png)

---

## 📂 Project Structure
- nasa-apod-data-pipeline/
- │── etl_pipeline/
- │   ├── upload_nasa.py        # Uploads processed data to Azure Blob
- │   ├── process_nasa.py       # Cleans/transforms raw JSON
- │   ├── curate_nasa.py        # Fetches NASA APOD data (curates raw JSON)
- │   └── run_nasa_pipeline.bat # Orchestrates the ETL scripts

---

## 🚀 Run the Pipeline
```bash
# Run manually
python curate_nasa.py
python process_nasa.py
python upload_nasa.py

# Or run the full pipeline with the batch script
run_nasa_pipeline.bat
