from urllib.parse import urljoin
import requests
import json

__all__ = ['get']

def get (sodas_api_base_url: str, access_token: str, environment_instance_id: str):
    """사용자의 개발도구 인스턴스 정보를 읽는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        access_token (str): Access Token
        environment_instance_id (str): SODAS+ Devops Environment Instance ID

    """
    optionsGetDistribution = {
        'url': urljoin(sodas_api_base_url, '/api/v1/devops/development/environment/instance/get'),
        'params': {
            'id': environment_instance_id
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