import boto3
import pickle
import os


def _get_enviroment_variables():
    endpoint = os.environ.get('s3_endpoint')
    if endpoint is None:
        raise ValueError('The -s3_endpoint- enviroment variable was not defined')

    bucket_name = os.environ.get('s3_bucket_name')
    if bucket_name is None:
        raise ValueError('The -s3_bucket_name- enviroment variable was not defined')

    access_key = os.environ.get('s3_access_key')
    if access_key is None:
        raise ValueError('The -s3_access_key- enviroment variable was not defined')

    secret_key = os.environ.get('s3_secret_key')
    if secret_key is None:
        raise ValueError('The -s3_secret_key- enviroment variable was not defined')

    return endpoint, bucket_name, access_key, secret_key

def _get_s3_resource(endpoint, access_key, secret_key):
    s3 = boto3.resource(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    return s3

def upload_object(object, prefix, file_name):
    endpoint, bucket_name, access_key, secret_key = _get_enviroment_variables()
    s3  = _get_s3_resource(endpoint, access_key, secret_key)

    key = os.path.join(prefix + file_name)
    s3.Object(bucket_name, key).put(Body=pickle.dumps(object))


def download_object(prefix, file_name):
    endpoint, bucket_name, access_key, secret_key = _get_enviroment_variables()
    s3  = _get_s3_resource(endpoint, access_key, secret_key)

    key = os.path.join(prefix + file_name)
    respone = s3.Object(bucket_name, key).get()
    response_object = pickle.load(respone['Body'])

    return response_object