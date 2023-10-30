from urllib.parse import urljoin
import requests
import boto3

__all__ = ['get_credential', 'list_objects', 'get_object', 'put_object', 'delete_object']

def get_credential (
        datalake_api_base_url: str,
        user_id: str,
        access_token: str
    ) -> (str, str) :
    """User의 Ceph Object Storage에 접근할 credential 정보를 얻는 함수

    Args:
        datalake_api_base_url (str): Datalake API Base URL
        user_id (str): User ID
        access_token (str): Access Token

    Returns:
        dict: Dictionary of Object List
    """
    
    credential_list = _get_credential_object_storage(
        sodas_datalake_base_url = datalake_api_base_url, 
        user_id = user_id, 
        access_token = access_token
    )
    access_key, secret_key = _get_credential_key(credential_list)

    return access_key, secret_key


def _get_credential_object_storage(
        sodas_datalake_base_url: str, 
        user_id: str,
        access_token: str
    ):
    
    optionGetObjectStorageCredental = {
        'url': urljoin(sodas_datalake_base_url, '/datalake/object-storage/credential/user/' + user_id + '/list'),
        'headers': {
            'Authorization': 'Bearer ' + access_token
        }
    }
    try :
        res = requests.get(optionGetObjectStorageCredental['url'],
                    headers=optionGetObjectStorageCredental['headers'])

        if res.status_code != 200:
            raise Exception(res.status_code)
        else :
            res = res.json()
            return res
            
    except Exception as e:
        print(e)


def _get_credential_key(response: object):
    # 일단 한개만 있다고 가정함
    access_key = response[0]['accessKey']
    secret_key = response[0]['secretKey']
    
    return access_key, secret_key


def _list_objects (
        rook_ceph_base_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str
    )-> dict:
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = rook_ceph_base_url,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        res = s3.list_objects(Bucket = bucket_name)
        status = res.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            keys = res['Contents']
            return keys
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
    except Exception as e:
        print(e)

def list_objects (
        user_id: str,
        access_token: str,
        datalake_api_base_url: str,
        rook_ceph_base_url: str,
        bucket_name: str
    )-> list:
    """User의 Ceph Object Storage에 저장된 objects의 list를 얻는 함수

    Args:
        user_id (str): User ID
        access_token (str): Access Token
        datalake_api_base_url (str): Datalake API Base URL
        rook_ceph_base_url (str): Rook Ceph Base URL
        bucket_name (str): Bucket Name

    Returns:
        list: List of Objects
    """
    access_key, secret_key = get_credential(datalake_api_base_url, user_id, access_token)
    return _list_objects(rook_ceph_base_url, access_key, secret_key, bucket_name)


def _get_object (
        rook_ceph_base_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        object_path: str
    ) -> object:
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = rook_ceph_base_url,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        res = s3.get_object(Bucket=bucket_name, Key=object_path)
        status = res.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            obj = res.get("Body")
            return obj
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
    except Exception as e:
        print(e)

def get_object (
        user_id: str,
        access_token: str,
        datalake_api_base_url: str,
        rook_ceph_base_url: str,
        bucket_name: str,
        object_path: str
    ) -> object:
    """User의 Object storage에 저장된 object를 read하는 함수

    Args:
        user_id (str): User ID
        access_token (str): Access Token
        datalake_api_base_url (str): Datalake API Base URL
        rook_ceph_base_url (str): Rook Ceph Base URL
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    Returns:
        object: Object File
    """
    
    access_key, secret_key = get_credential(datalake_api_base_url, user_id, access_token)
    return _get_object(rook_ceph_base_url, access_key, secret_key, bucket_name, object_path)


def _put_object(
        rook_ceph_base_url: str,
        access_key: str,
        secret_key: str,
        local_file_path: str,
        bucket_name: str,
        object_path: str
    ):
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = rook_ceph_base_url,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        response = s3.upload_file(local_file_path, bucket_name, object_path)
        
    except Exception as e:
        print(e)


def put_object(
        user_id: str,
        access_token: str,
        datalake_api_base_url: str,
        rook_ceph_base_url: str,
        local_file_path: str,
        bucket_name: str,
        object_path: str
    ):
    """User의 Ceph Object Storage에 object를 put하는 함수.

    Args:
        user_id (str): User ID
        access_token (str): Access Token
        datalake_api_base_url (str): Datalake API Base URL
        rook_ceph_base_url (str): Rook Ceph Base URL
        local_file_path (str): Local File Path
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    """
    access_key, secret_key = get_credential(datalake_api_base_url, user_id, access_token)

    _put_object(rook_ceph_base_url, access_key, secret_key, local_file_path, bucket_name, object_path)


def _delete_object(
        rook_ceph_base_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        object_path: str
    ):
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = rook_ceph_base_url,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        response = s3.delete_object(Bucket=bucket_name, Key=object_path)
        
        if (response['DeleteMarker'] == True):
            return 'Success'
        else:
            return 'Failed'
        
    except Exception as e:
        print(e)


def delete_object(
        user_id: str,
        access_token: str,
        datalake_api_base_url: str,
        rook_ceph_base_url: str,
        bucket_name: str,
        object_path: str
    ):
    """User의 Ceph Object Storage에서 object를 delete 하는 함수.

    Args:
        user_id (str): User ID
        access_token (str): Access Token
        datalake_api_base_url (str): Datalake API Base URL
        rook_ceph_base_url (str): Rook Ceph Base URL
        bucket_name (str): Bucket Name
        object_path (str): Object Path

    """
    access_key, secret_key = get_credential(datalake_api_base_url, user_id, access_token)

    return _delete_object(rook_ceph_base_url, access_key, secret_key, bucket_name, object_path)