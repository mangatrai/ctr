import json
import os
from dotenv import load_dotenv
from astrapy.db import AstraDB
from tqdm import tqdm  # For progress bar
import argparse
# Load environment variables
load_dotenv()

# Get Astra DB credentials from environment variables
ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_TOKEN')
ASTRA_DB_API_ENDPOINT = os.getenv('ASTRA_API_ENDPOINT')
COLLECTION_NAME = os.getenv('ASTRA_COLLECTION')
BATCH_SIZE = int(os.getenv('ASTRA_BATCH_SIZE'))


def initialize_astra_client():
    try:
        # New way to create Astra client
        db = AstraDB(
            token=ASTRA_DB_APPLICATION_TOKEN,
            api_endpoint=ASTRA_DB_API_ENDPOINT
        )
        
        # New way to create collection
        collection = db.create_collection(COLLECTION_NAME)
        
        return collection
    except Exception as e:
        print(f"Error initializing Astra client: {str(e)}")
        raise

def read_json_file(file_path):
    """Read transactions from JSON file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        raise

def insert_batch(collection, batch):
    """Insert a single batch of transactions"""
    successful = 0
    failed = 0
    
    try:
        # Extract the transaction data from the nested structure
        processed_batch = []
        for doc in batch:
            transaction_data = doc["transaction"]
            # Add _id field for document identification
            transaction_data["_id"] = transaction_data["transactionId"]
            processed_batch.append(transaction_data)
            
        # Use AstraPy's batch insert method with flattened structure
        result = collection.insert_many(processed_batch)
        successful = len(result['status']['insertedIds']) if isinstance(result, dict) else len(result)
    except Exception as e:
        print(f"\nError inserting batch: {str(e)}")
        failed = len(batch)
        
    return successful, failed

def batch_insert_transactions(collection, transactions):
    """Insert transactions in batches"""
    total_transactions = len(transactions)
    successful_inserts = 0
    failed_inserts = 0
    
    # Create progress bar
    progress_bar = tqdm(total=total_transactions, desc="Inserting transactions")
    
    current_batch = []
    
    try:
        for transaction in transactions:
            current_batch.append(transaction)
            
            # When batch size is reached, insert the batch
            if len(current_batch) >= BATCH_SIZE:
                success, failed = insert_batch(collection, current_batch)
                successful_inserts += success
                failed_inserts += failed
                progress_bar.update(len(current_batch))
                current_batch = []
        
        # Insert any remaining transactions
        if current_batch:
            success, failed = insert_batch(collection, current_batch)
            successful_inserts += success
            failed_inserts += failed
            progress_bar.update(len(current_batch))
            
    except Exception as e:
        print(f"\nError during batch insertion: {str(e)}")
    finally:
        progress_bar.close()
        
    print(f"\nInsertion complete:")
    print(f"Successfully inserted: {successful_inserts}")
    print(f"Failed insertions: {failed_inserts}")

def verify_insertion(collection):
    """Verify the number of documents inserted"""
    try:
        result = collection.count_documents({})
        count = result['status']['count'] if isinstance(result, dict) else result
        print(f"\nVerification: Found {count} documents in collection")
        return count
    except Exception as e:
        print(f"Error verifying insertion: {str(e)}")
        return None

def clean_collection(collection):
    """Delete all documents from the collection"""
    try:
        print("Cleaning collection...")
        result = collection.delete_many({})
        deleted_count = result['status']['count'] if isinstance(result, dict) else result
        print(f"Successfully deleted {deleted_count} documents from collection")
        return deleted_count
    except Exception as e:
        print(f"Error cleaning collection: {str(e)}")
        return None

def main():
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='AstraDB Transaction Data Management')
    parser.add_argument('--action', choices=['insert', 'delete'], default='insert',
                      help='Action to perform: insert (default) or delete')
    args = parser.parse_args()

    # Initialize Astra DB client
    print("Initializing Astra DB connection...")
    collection = initialize_astra_client()
    
    if args.action == 'delete':
        clean_collection(collection)
        return

    # Original insert logic
    print("Reading JSON file...")
    file_path = os.getenv('SAMPLE_DATA_FILE')
    transactions = read_json_file(file_path)
    
    print(f"Found {len(transactions)} transactions to insert")
    
    print("Starting batch insertion...")
    batch_insert_transactions(collection, transactions)

    print("Verifying insertion...")
    verify_insertion(collection)

if __name__ == "__main__":
    main()
