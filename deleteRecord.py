from datetime import datetime
import pymongo

# MongoDB connection string
mongo_url = "mongodb+srv://akash9936:Tree9936@cluster0.f1wthph.mongodb.net/?retryWrites=true&w=majority"
# MongoDB database and collection names
client = pymongo.MongoClient(mongo_url)
db = client.test
collection_name = "nse50"  # Replace with your actual collection name

# Function to fetch records based on timestamp
def fetch_records_by_timestamp(client, database_name, collection_name, timestamp):
    # Select the database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Fetch records based on the timestamp
    result = collection.find({"timestamp": {"$eq": timestamp}})

    # Print the fetched records with timestamp
    count = collection.count_documents({"timestamp": {"$eq": timestamp}})
    print(f"Count of records with timestamp '{timestamp}': {count}")
    result = collection.delete_many({"timestamp": {"$eq": timestamp}})
    print(f"Deleted {result.deleted_count} records with timestamp '{timestamp}'")

        # Print other fields in the record if needed

# Specify the timestamp you want to use for fetching
timestamp_to_fetch = "25-Jan-2024 16:00:00"
database_name = "test"  # Replace with your actual database name

# Call the function to fetch records
fetch_records_by_timestamp(client, database_name, collection_name, timestamp_to_fetch)

# Close the MongoDB connection (optional if the script ends immediately after)
client.close()
