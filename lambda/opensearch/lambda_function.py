import os
import boto3
import json

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from pprint import pprint


def lambda_handler(event, context):
    # Environment variables
    host = os.environ.get('HOST')
    auth = (os.environ.get('OPENSEARCH_USERNAME'), os.environ.get('OPENSEARCH_PASSWORD'))
    
    region = os.environ.get('AWS_REGION')
    service = 'es'
    
    print(host, auth)
    
    client = OpenSearch(
        hosts = [host],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        connection_class = RequestsHttpConnection
    )

    index_name = 'photos_index'  # Replace with your index name

    health = client.cluster.health()
    return {
        'statusCode': 200,
        'body': health
    }
    
    # # mapping for the index
    # mapping = {
    #     "properties": {
    #         "objectKey": {
    #             "type": "text"
    #         },
    #         "bucket": {
    #             "type": "text"
    #         },
    #         "createdTimestamp": {
    #             "type": "date"
    #         },
    #         "labels": {
    #             "type": "keyword"  # Use 'keyword' type for exact matches
    #         }
    #     }
    # }
    
    # # Create an index with the defined mapping
    # client.indices.create(
    #     index=index_name,
    #     body={
    #         "settings": {
    #             "index": {
    #                 "number_of_shards": 1,  # You can define number of shards and replicas as per your requirement
    #                 "number_of_replicas": 0
    #             }
    #         },
    #         "mappings": mapping
    #     },
    #     ignore=400  # Ignores IndexAlreadyExistsException if the index already exists
    # )
    
    # # Check the mapping
    # current_mapping = client.indices.get_mapping(index=index_name)
    # # return {
    # #     'statusCode': 200,
    # #     'body': current_mapping
    # # }
    
    # # List all indices
    # index_list = client.cat.indices(format='json')
    # return {
    #     'statusCode': 200,
    #     'body': index_list
    # }

    # document = {
    #     "objectKey": "my-photo.jpg",
    #     "bucket": "my-photo-bucket",
    #     "createdTimestamp": "2018-11-05T12:40:02",
    #     "labels": ["person", "dog", "ball", "park"]
    # }
    
    # # Index the sample document
    # client.index(
    #     index=index_name,
    #     body=document
    # )
    
    # def get_all_documents(index_name, max_docs=10000):
    #     query = {
    #         "size": 50,
    #         "query": {
    #             "match_all": {}
    #         }
    #     }
    #     response = client.search(body=query, index=index_name)
    #     documents = response['hits']['hits']  # List of documents in the index
        
    #     return documents
    
    # # Usage
    # documents = get_all_documents(index_name)
    # for doc in documents:
    #     print(doc)
        
    # return {
    #     'statusCode': 200,
    #     'body': documents
    # }
