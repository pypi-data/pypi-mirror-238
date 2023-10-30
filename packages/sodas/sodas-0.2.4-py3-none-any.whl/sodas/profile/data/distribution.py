from urllib.parse import urljoin
import requests
import json

from sodas.datalake.object_storage import (
    get_credential as get_credential_from_datalake,
    _get_object as _get_object_from_datalake
)

__all__ = ['get', 'get_object']

def get (sodas_api_base_url: str, access_token: str, distribution_id: str) :
    """Distribution 정보를 읽는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        distribution_id (str): SODAS+ Distribution ID

    """
    optionsGetDistribution = {
        'url': urljoin(sodas_api_base_url, '/api/v1/profile/data/distribution/get'),
        'params': {
            'id': distribution_id
        },
        'headers': {
            'accept' : 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    }
    
    try:
        res = requests.get(optionsGetDistribution['url'],
                        headers=optionsGetDistribution['headers'],
                        params=optionsGetDistribution['params'])
        
        if res.status_code == 200:
            distribution = json.loads(res.content.decode('utf-8'))
            return distribution
        else :
            raise Exception(res.status_code, res.content)
    except Exception as e:
        print(e)

def get_object (sodas_api_base_url: str, user_id: str, access_token: str, distribution_id: str):
    """Distribution으로 등록된 Ceph Object Storage의 object 내용을 읽는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        user_id (str): User ID
        access_token (str): Access Token
        distribution_id (str): SODAS+ Distribution ID

    """
    distribution_info = get(sodas_api_base_url, access_token, distribution_id)
    # distribution에서 읽도록 변경
    datalake_api_base_url = 'http://datalake-api.221.154.134.31.traefik.me:10017'
    # distribution에서 읽도록 변경
    rook_ceph_base_url = 'http://object-storage.rook.221.154.134.31.traefik.me:10017'
    bucket_name = distribution_info['dataStorageConfig']['bucket']
    object_name = distribution_info['dataStorageConfig']['path']

    access_key, secret_key = get_credential_from_datalake(datalake_api_base_url, user_id, access_token)

    return _get_object_from_datalake(rook_ceph_base_url, access_key, secret_key, bucket_name, object_name)