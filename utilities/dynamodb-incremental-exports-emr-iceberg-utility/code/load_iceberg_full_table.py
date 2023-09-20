
from pyspark.sql import SparkSession
import sys
# Define the function to load the full table into Iceberg
def load_full_table(full_file_path, user_schema, full_table_name):
    # Initialize Spark session with necessary configurations for Iceberg
    spark = SparkSession.builder \
    .appName("Load Full Table to Iceberg") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.dev", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.dev.type", "hadoop") \
    .config("spark.sql.catalog.dev.warehouse", "s3://<YOUR-BUCKET>/example-prefix/") \
    .getOrCreate()
    
    # Read JSON file into a DataFrame
    df_full = spark.read.json(full_file_path)
    
    # Register the DataFrame as a temporary table for SQL operations
    df_full.createOrReplaceTempView("tmp_full_table")
    
    # Create SQL query to transform JSON structure into a flat table
    queryFull = ", ".join([f"Item.{col}.{type} as {col}" for col, type in user_schema.items()])
    
    # Execute SQL query and create a new DataFrame
    df_full_result = spark.sql(f"SELECT {queryFull} FROM tmp_full_table")
    df_full_result.show()
    
    # Write the resulting DataFrame to an Iceberg table
    df_full_result.writeTo(f"dev.db.{full_table_name}").using("iceberg").createOrReplace()

# Entry point of the script
if __name__ == "__main__":
    
    # Get command-line arguments
    full_file_path = sys.argv[1]
    full_table_name = sys.argv[2]
    
    # Define the schema for the DataFrame based on user input
    user_schema = {
    "product_id": "S",
    "quantity": "N",
    # ... other columns
    }
    
    # Call the function to perform the full table load
    load_full_table(full_file_path, user_schema, full_table_name)
