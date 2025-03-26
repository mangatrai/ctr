import json
import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch, helpers
from tqdm import tqdm
import urllib3
import ssl
import argparse

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# OpenSearch configuration
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_USERNAME = os.getenv('OPENSEARCH_USERNAME')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')
OPENSEARCH_INDEX = os.getenv('OPENSEARCH_INDEX')
OPENSEARCH_BATCH_SIZE = int(os.getenv('OPENSEARCH_BATCH_SIZE', 100))
OPENSEARCH_VERIFY_SSL = os.getenv('OPENSEARCH_VERIFY_SSL', 'false').lower() == 'true'

def initialize_opensearch_client():
    """Initialize OpenSearch client with security settings"""
    try:
        client = OpenSearch(
            hosts=[OPENSEARCH_HOST],
            http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
            verify_certs=OPENSEARCH_VERIFY_SSL,
            ssl_show_warn=False
        )
        return client
    except Exception as e:
        print(f"Error initializing OpenSearch client: {str(e)}")
        raise

def read_json_file(file_path):
    """Read transactions from JSON file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        raise

def generate_bulk_data(transactions):
    """Generate bulk data for OpenSearch insertion"""
    for transaction in transactions:
        yield {
            "_index": OPENSEARCH_INDEX,
            "_source": transaction
        }

def insert_batch(client, transactions):
    """Insert a batch of transactions using bulk API"""
    try:
        success, failed = helpers.bulk(
            client,
            generate_bulk_data(transactions),
            chunk_size=OPENSEARCH_BATCH_SIZE,
            raise_on_error=False
        )
        # failed is a list of failed items, so we need to count them
        failed_count = len(failed) if failed else 0
        return success, failed_count
    except Exception as e:
        print(f"\nError inserting batch: {str(e)}")
        return 0, len(transactions)

def batch_insert_transactions(client, transactions):
    """Insert transactions in batches"""
    total_transactions = len(transactions)
    successful_inserts = 0
    failed_inserts = 0
    
    # Create progress bar
    progress_bar = tqdm(total=total_transactions, desc="Inserting transactions")
    
    # Process in batches
    for i in range(0, total_transactions, OPENSEARCH_BATCH_SIZE):
        batch = transactions[i:i + OPENSEARCH_BATCH_SIZE]
        success, failed = insert_batch(client, batch)
        successful_inserts += success
        failed_inserts += failed
        progress_bar.update(len(batch))
    
    progress_bar.close()
    
    print(f"\nInsertion complete:")
    print(f"Successfully inserted: {successful_inserts}")
    print(f"Failed insertions: {failed_inserts}")

def verify_insertion(client):
    """Verify the number of documents inserted"""
    try:
        result = client.count(index=OPENSEARCH_INDEX)
        count = result['count']
        print(f"\nVerification: Found {count} documents in index")
        return count
    except Exception as e:
        print(f"Error verifying insertion: {str(e)}")
        return None

def clean_index(client):
    """Delete all documents from the index"""
    try:
        print(f"Cleaning index {OPENSEARCH_INDEX}...")
        result = client.delete_by_query(
            index=OPENSEARCH_INDEX,
            body={"query": {"match_all": {}}},
            refresh=True
        )
        deleted_count = result.get('deleted', 0)
        print(f"Successfully deleted {deleted_count} documents from index")
        return deleted_count
    except Exception as e:
        print(f"Error cleaning index: {str(e)}")
        return None

def main():
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='OpenSearch Transaction Data Management')
    parser.add_argument('--action', choices=['insert', 'delete'], default='insert',
                      help='Action to perform: insert (default) or delete')
    args = parser.parse_args()

    # Initialize OpenSearch client
    print("Initializing OpenSearch connection...")
    client = initialize_opensearch_client()
    
    if args.action == 'delete':
        clean_index(client)
        return

    # Original insert logic
    print("Reading JSON file...")
    file_path = os.getenv('SAMPLE_DATA_FILE')
    transactions = read_json_file(file_path)
    
    print(f"Found {len(transactions)} transactions to insert")
    
    print("Starting batch insertion...")
    batch_insert_transactions(client, transactions)

    print("Verifying insertion...")
    verify_insertion(client)

if __name__ == "__main__":
    main() 