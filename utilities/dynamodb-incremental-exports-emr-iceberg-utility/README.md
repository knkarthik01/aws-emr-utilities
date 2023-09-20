
# DynamoDB Incremental Exports EMR Spark Iceberg Utility

## Summary

Utility scripts for data ingestion into Iceberg tables using PySpark and AWS S3. Includes scripts for full table loads (`load_iceberg_full_table.py`) and incremental data updates (`load_iceberg_incremental_table.py`).
---
## Description
Scripts to perform full table and incremental data loads from DynamoDB extracts.
---
## Usage
### Full Table Load
```bash
spark-submit load_full_table.py [full_data_file_path] [full_iceberg_table_name]
```
### Incremental Load
```bash
spark-submit load_incremental.py [incremental_data_file_path] [delta_iceberg_table_name] [full_iceberg_table_name]
```
---
## Dependencies
AWS CLI
PySpark (Iceberg enabled Spark Cluster)
---
## User Schema Definition
Define the `user_schema` dictionary in each script to specify the schema of the data.
### Example Schema
```python
user_schema = {
    "product_id": "S",
    "quantity": "N",
    "remaining_count": "N",
    "inventory_date": "S",
    "price": "S",
    "product_name": "S"
}
```
---
## Scripts Details
### How Full Table Load Works (`load_full_table.py`)
Details about how the full table load script functions.
#### Code Snippet
```python
# (Insert the Python code for load_full_table.py)
```
---
### How Incremental Table Load Works (`load_incremental.py`)
Details about how the incremental table load script functions.
#### Code Snippet
```python
# (Insert the Python code for load_incremental.py)
```
---
## Full End-to-End Testing
### Usage
Save the script as `run_ingest.sh` and make it executable.
```bash
chmod +x run_ingest.sh
```

Install AWS CLI and configure credentials.
```bash
aws configure
```

Run the script.
```bash
./run_ingest.sh
```
### Test Script
```python
# (Insert the Python code for the test script)
```
---
## Note
Ensure your PySpark environment is set up properly, and spark-submit is available in the terminal.
