from typing import List, Dict

import pandas as pd
from google.cloud import storage
from pathlib import Path


def get_csv_from_gcs(bucket_name, path):
    full_path = 'gs://{bucket}/{path}'.format(bucket=bucket_name, path=path)
    file_type = path.split(".")[-1]
    result_df = pd.DataFrame()
    if file_type == 'csv':
        result_df = pd.read_csv(full_path)
    elif file_type == 'xlsx' or file_type == 'xls':
        result_df = pd.read_excel(full_path, engine='openpyxl')
    return result_df


def get_all_file_from_gcs_folder(bucket_name, path, file_type='csv'):
    file_dict = {}
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        for blob in bucket.list_blobs(prefix=str(path)):
            current_path = Path(blob.name)
            if str(current_path) != str(path):
                full_path = 'gs://{bucket}/{path}'.format(bucket=bucket_name, path=str(current_path))
                file = pd.DataFrame()
                if file_type == 'csv':
                    file = pd.read_csv(full_path)
                elif file_type == 'excel':
                    file = pd.read_excel(full_path)
                file_dict[current_path] = file
    except Exception as e:
        raise e
    return file_dict


def get_file_as_string_from_gcs(bucket_name, path) -> bytes:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(path)

    # Download the contents of the blob as a string and then parse it using json.loads() method
    return blob.download_as_string(client=None)


def get_all_json_from_gcs(bucket_name, folder_path) -> Dict[str, bytes]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)
    result_dict = {}
    for blob in blobs:
        if blob.name.endswith('.json'):
            result_dict[blob.name] = blob.download_as_string(client=None)
    return result_dict


def upload_json_to_gcs(bucket_name, destination_blob_name, json_data):
    # 初始化GCS客户端
    client = storage.Client()

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json_data, content_type='application/json')


def delete_file_from_gcs(bucket_name, file_name):
    # 初始化 GCS 客户端
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print(f'File {file_name} deleted from {bucket_name}.')


def upload_file_to_gcs(bucket_name, path, file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    public_url = blob.public_url
    return {"public_url": public_url}
