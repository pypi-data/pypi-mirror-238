from urllib.parse import urljoin
import requests
import boto3
from minio import Minio
from sodas.analyticops.environment_instance import (
    get as get_environment_instance
)

__all__ = ['list_objects', 'get_object', 'put_object', 'delete_object']

def _get_connection_info (
        sodas_api_base_url: str,
        access_token: str,
        environment_instance_id: str
    ) -> (str, str, str) :
    
    environment_instance = get_environment_instance(
        sodas_api_base_url = sodas_api_base_url, 
        access_token = access_token,
        environment_instance_id = environment_instance_id
    )
    host = [o['host'] for o in environment_instance['sandbox']['ingress'] if o['servicePort'] == 9000][0]
    port = [o['clusterAccessPort'] for o in environment_instance['sandbox']['ingress'] if o['servicePort'] == 9000][0]
    minio_endpoint_url = host + ':' + str(port)
    access_key = [o['value'] for o in environment_instance['config']['environments'] if o['name'] == 'MINIO_ACCESS_KEY'][0]
    secret_key = [o['value'] for o in environment_instance['config']['environments'] if o['name'] == 'MINIO_SECRET_KEY'][0] 

    return minio_endpoint_url, access_key, secret_key

def _list_objects (
        minio_endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str
    )-> dict:

    try:
        minioClient = Minio(endpoint=minio_endpoint_url, secure=False, access_key=access_key, secret_key=secret_key)
        
        res = minioClient.list_objects(bucket_name = bucket_name)
        objects = []
        for o in res:
            objects.append(
                {
                    'bucket_name': o.bucket_name,
                    'content_type': o.content_type,
                    'etag': o.etag,
                    'is_delete_marker': o.is_delete_marker,
                    'is_dir': o.is_dir,
                    'is_latest': o.is_latest,
                    'last_modified': o.last_modified,
                    'object_name': o.object_name,
                    'owner_id': o.owner_id, 
                    'owner_name': o.owner_name,
                    'size': o.size,
                    'storage_class': o.storage_class,
                    'version_id': o.version_id
                }
            )

        return objects
    except Exception as e:
        print(e)

def list_objects (
        sodas_api_base_url: str,
        access_token: str,
        storage_id: str,
        bucket_name: str
    )-> list:
    """사용자의 MinIO object storage에 저장된 objects의 list를 얻는 함수

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        storage_id (str): SODAS+ Devops Storage ID
        bucket_name (str): Bucket Name

    Returns:
        list: List Object List
    """
    minio_endpoint_url, access_key, secret_key = _get_connection_info(sodas_api_base_url, access_token, environment_instance_id=storage_id)
    return _list_objects(minio_endpoint_url, access_key, secret_key, bucket_name)


def _get_object (
        minio_endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        object_name: str
    ) -> object:

    try:
        minioClient = Minio(endpoint=minio_endpoint_url, secure=False, access_key=access_key, secret_key=secret_key)
        res = minioClient.get_object(bucket_name = bucket_name, object_name = object_name)
        return res
    except Exception as e:
        print(e)

def get_object (
        sodas_api_base_url: str,
        access_token: str,
        storage_id: str,
        bucket_name: str,
        object_path: str
    ) -> object:
    """사용자의 MinIO Object storage에 저장된 object를 read하는 함수

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        storage_id (str): SODAS+ Devops Storage ID
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    Returns:
        object: Object File
    """
    
    minio_endpoint_url, access_key, secret_key = _get_connection_info(sodas_api_base_url, access_token, environment_instance_id=storage_id)
    return _get_object(minio_endpoint_url, access_key, secret_key, bucket_name, object_path)


def _put_object(
        minio_endpoint_url: str,
        access_key: str,
        secret_key: str,
        local_file_path: str,
        bucket_name: str,
        object_name: str
    ):
    try:
        minioClient = Minio(endpoint=minio_endpoint_url, secure=False, access_key=access_key, secret_key=secret_key)
        
        minioClient.fput_object(bucket_name, object_name, local_file_path)
        
    except Exception as e:
        print(e)


def put_object(
        sodas_api_base_url: str,
        access_token: str,
        storage_id: str,
        local_file_path: str,
        bucket_name: str,
        object_path: str
    ):
    """사용자의 MinIO Object storage에 object를 put하는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        storage_id (str): SODAS+ Devops Storage ID
        local_file_path (str): Local File Path
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    """
    
    minio_endpoint_url, access_key, secret_key = _get_connection_info(sodas_api_base_url, access_token, environment_instance_id=storage_id)
    _put_object(minio_endpoint_url, access_key, secret_key, local_file_path, bucket_name, object_path)


def _delete_object(
        minio_endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        object_name: str
    ):
    try:
        minioClient = Minio(endpoint=minio_endpoint_url, secure=False, access_key=access_key, secret_key=secret_key)
        
        minioClient.remove_object(bucket_name, object_name)
        
    except Exception as e:
        print(e)


def delete_object(
        sodas_api_base_url: str,
        access_token: str,
        storage_id: str,
        bucket_name: str,
        object_path: str
    ):
    """사용자의 MinIO Object Storage에서 object를 delete 하는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        storage_id (str): SODAS+ Devops Storage ID
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    """
    minio_endpoint_url, access_key, secret_key = _get_connection_info(sodas_api_base_url, access_token, environment_instance_id=storage_id)
    _delete_object(minio_endpoint_url, access_key, secret_key, bucket_name, object_path)