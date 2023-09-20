
from pyspark.sql import SparkSession
import sys
# Define the function for loading incremental data into Iceberg
def load_incremental(data_file_path, user_schema, delta_table_name, full_table_name, partition_key, sort_key=None):
    
    # Initialize Spark session with configurations specific to Iceberg
    spark = SparkSession.builder \
    .appName("Load Incremental Data to Iceberg") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.dev", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.dev.type", "hadoop") \
    .config("spark.sql.catalog.dev.warehouse", "s3://<YOUR-S3-BUCKET>/example-prefix/") \
    .getOrCreate()
    
    # Read JSON file into DataFrame
    df = spark.read.json(data_file_path)
    
    # Register DataFrame as temporary table for SQL operations
    df.createOrReplaceTempView("tmp_stage_table")
    
    # Build SQL query for transforming JSON structure based on user-provided schema
    queryDelta = ", ".join([f"NewImage.{col}.{type} as {col}" for col, type in user_schema.items()])
    keys_query = [f"Keys.{pk}.{user_schema[pk]} as Keys_{pk}" for pk in partition_key]
    
    # Handle sort keys if any
    if sort_key:
        for sk in sort_key:
            keys_query.append(f"Keys.{sk}.{user_schema[sk]} as Keys_{sk}")
    queryDelta = ', '.join(keys_query) + ", " + queryDelta
    
    # Run SQL query and show the result
    df_stg_result = spark.sql(f"SELECT {queryDelta} FROM tmp_stage_table")
    df_stg_result.show()
    
    # Write DataFrame to delta table in Iceberg
    df_stg_result.writeTo(f"dev.db.{delta_table_name}").using("iceberg").createOrReplace()
    
    # Merge logic for updating full table from delta table
    join_condition = ' AND '.join([f"target.{pk} = source.Keys_{pk}" for pk in partition_key])
    if sort_key:
        join_condition += ' AND ' + ' AND '.join([f"target.{sk} = source.Keys_{sk}" for sk in sort_key])
    delete_conditions = [f"source.Keys_{key} is null" for key in partition_key]
    if sort_key:
        delete_conditions += [f"source.Keys_{key} is null" for key in sort_key]
    delete_condition_str = ' AND '.join(delete_conditions)
    merge_query = f"""
    MERGE INTO dev.db.{full_table_name} AS target
    USING dev.db.{delta_table_name} AS source
    ON {join_condition}
    WHEN MATCHED AND {delete_condition_str} THEN DELETE
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
    """
    
    # Execute merge query
    spark.sql(merge_query)

# Entry point of the script
if __name__ == "__main__":
    
    # Get command-line arguments
    data_file_path = sys.argv[1]
    delta_table_name = sys.argv[2]
    full_table_name = sys.argv[3]
    
    # Define user schema
    user_schema = {
        "product_id": "S",
        "quantity": "N",
        "remaining_count": "N",
        "inventory_date": "S",
        "price": "S",
        "product_name": "S"
    }
    partition_key = ["product_id"] # replace with you pk
    sort_key = None  # Or pass a list like ["inv_date"]
    
    # Call function to load incremental data
    load_incremental(data_file_path, user_schema, delta_table_name, full_table_name, partition_key, sort_key)
