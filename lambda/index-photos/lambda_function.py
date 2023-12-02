import os
import boto3

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from datetime import datetime


# Set up S3 and Rekognition clients
s3_client = boto3.client('s3')
print('s3 client configured', s3_client)
rekognition_client = boto3.client('rekognition')
print('rekognition client configured', rekognition_client)

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
    # Get bucket name and object key from the Lambda event
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    # bucket, object_key = 'vt2182-a3-b2', 'dog.jpg'
    print(bucket, object_key)

    # Detect labels in the image using Rekognition
    rekognition_response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': object_key
            },
        },
    )
    print(rekognition_response)
    
    # Get labels from Rekognition response
    labels = [label['Name'] for label in rekognition_response['Labels']]
    print(labels)
    
    # Get the image's metadata using S3's headObject method
    metadata_response = s3_client.head_object(Bucket=bucket, Key=object_key)
    custom_labels = metadata_response['Metadata'].get('x-amz-meta-customlabels', '').split(',')
    print(custom_labels)
    
    labels.extend(custom_labels)
    print(labels)
    
    # Construct the JSON document for OpenSearch
    document = {
        "objectKey": object_key,
        "bucket": bucket,
        "createdTimestamp": datetime.now().isoformat(),
        "labels": labels
    }
    print(document)

    # Index the document in OpenSearch
    index_response = opensearch_client.index(
        index='photos',
        body=document
    )

    # print(index_response)
    return {
        'statusCode': 200,
        'body': {
            'message': 'Photo indexed successfully.',
            'document': document
        }
    }


