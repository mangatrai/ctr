# Sephora CTR Project

This project demonstrates the implementation of OpenSearch queries for transaction analysis, based on SOLR reference queries.

## Project Structure

- `insert_to_astra.py`: Script for inserting transaction data into AstraDB
- `insert_to_opensearch.py`: Script for inserting transaction data into OpenSearch
- `opensearch_reference_queries.md`: Collection of OpenSearch queries demonstrating various capabilities
- `sample/`: Directory containing sample data files
  - `CTR-CompleteDoc.json`: Complete transaction document structure
  - `synthetic_transactions.json`: Generated synthetic transaction data

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with the following variables:
```
ASTRA_TOKEN=your_astra_token
ASTRA_API_ENDPOINT=your_astra_endpoint
ASTRA_COLLECTION=your_collection_name
ASTRA_BATCH_SIZE=100
SAMPLE_DATA_FILE=sample/synthetic_transactions.json
OPENSEARCH_HOST=your_opensearch_host
OPENSEARCH_INDEX=transaction_history
OPENSEARCH_BATCH_SIZE=100
```

## Usage

### Data Insertion

1. Insert data into AstraDB:
```bash
python insert_to_astra.py --action insert
```

2. Insert data into OpenSearch:
```bash
python insert_to_opensearch.py --action insert
```

### Data Cleanup

1. Clean AstraDB collection:
```bash
python insert_to_astra.py --action delete
```

2. Clean OpenSearch index:
```bash
python insert_to_opensearch.py --action delete
```

## OpenSearch Queries

The project includes 20 OpenSearch queries demonstrating various capabilities:

1. Complex Order Search with Facets
2. Advanced Client Profile Search
3. Advanced Status Analysis
4. Complex Payment Analysis
5. Advanced Store Transaction Analysis
6. Advanced Transaction Analytics
7. Advanced Risk Analysis
8. Advanced Shipping Analysis
9. Advanced Client Loyalty Analysis
10. Advanced Transaction Origin Analysis
11. Advanced Price Analysis
12. Advanced Item Analysis
13. Advanced Employee Analysis
14. Advanced Location Analysis
15. Advanced Discount Analysis
16. Advanced Customer Segmentation
17. Advanced Inventory Analysis
18. Advanced Fraud Detection
19. Advanced Customer Journey Analysis
20. Advanced Performance Metrics

Each query demonstrates different OpenSearch features and capabilities. See `opensearch_reference_queries.md` for detailed query documentation. 