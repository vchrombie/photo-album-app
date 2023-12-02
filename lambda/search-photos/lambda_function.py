import os
import boto3
import json

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from pprint import pprint


# Set up OpenSearch client
host = os.environ.get('HOST')
username = os.environ.get('OPENSEARCH_USERNAME')
password = os.environ.get('OPENSEARCH_PASSWORD')
auth = (username, password)
print(host, auth)

opensearch_client = OpenSearch(
    hosts = [host],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    connection_class = RequestsHttpConnection
)
print('opensearch client configured', opensearch_client)


def lambda_handler(event, context):

    # Extract the slots from the event
    slots = event['currentIntent']['slots']
    slot_values = [value for key, value in slots.items() if value]
    print(slot_values)
    
    index_name = 'photos'  # Replace with your index name
    
    # Construct the search query for OpenSearch
    query = {
        'size': 10,
        'query': {
            'bool': {
                'should': [
                    {'match': {'labels': slot}} for slot in slot_values
                ],
                'minimum_should_match': 1
            }
        }
    }
    
    # Execute the search query
    response = opensearch_client.search(
        body=query,
        index=index_name
    )
    print(response)
    
    # Extract the results from the response
    results = [
        {
            '_score': hit['_score'],
            'objectKey': hit['_source']['objectKey'],
            'bucket': hit['_source']['bucket']
        }
        for hit in response['hits']['hits']
    ]
    print(results)
    
    # Return the search results
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
