
# DynamoDB Incremental Exports EMR Spark Iceberg Utility

## Summary

Utility scripts for ingesting data into Iceberg tables via PySpark and AWS S3 are provided in this package. It contains three key scripts to facilitate the ingestion of incremental exports from DynamoDB on S3 into Iceberg tables hosted on AWS Glue or Hive Metastore, utilizing Amazon EMR.

a. The first script (`load_iceberg_full_table.py`) initializes your Iceberg data lake table on S3 with a full data export from DynamoDB.

b. The second script generates a list of data files from DynamoDB's manifest files for incremental exports. This list aids in updating the table created by the first script.

c. The third script (`load_iceberg_incremental_data.py`) executes incremental updates on your target Iceberg data lake table and sets the stage for future updates.
Together, these scripts offer a comprehensive solution for managing full and incremental data loads into Iceberg tables.

## Description
Scripts to perform full table and incremental data loads from DynamoDB extracts.

## Usage
### Full Table Load
```bash
spark-submit load_full_table.py [full_data_file_path] [full_iceberg_table_name]
```
### Incremental Load
```bash
spark-submit load_incremental.py [incremental_data_file_path] [delta_iceberg_table_name] [full_iceberg_table_name]
```

## Dependencies
AWS CLI
PySpark (Iceberg enabled Spark Cluster)

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

## Scripts Details
### How Full Table Load Works (`load_full_table.py`)
Details about how the full table load script functions.
#### Code Snippet
```python
# (Insert the Python code for load_full_table.py)
```

### How Incremental Table Load Works (`load_incremental.py`)
Details about how the incremental table load script functions.
#### Code Snippet
```python
# (Insert the Python code for load_incremental.py)
```

## Full End-to-End Testing
### Usage
Save the script as `run_ingest.py` and make it executable.


Install AWS CLI and configure credentials.
```bash
aws configure
```

Run the script.
```bash
python3 run_ingest.py
```
### Test Script
```python
# (Insert the Python code for the test script)
```

## Note
Ensure your PySpark environment is set up properly, and spark-submit is available in the terminal.
