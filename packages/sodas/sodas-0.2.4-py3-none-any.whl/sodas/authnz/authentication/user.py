from urllib.parse import urljoin
import requests

__all__ = ['get_access_token']

def get_access_token(sodas_api_base_url: str, user_id: str, refresh_token: str) -> str:
    """refresh token으로 access token을 재발급받는 함수.

    Args:
        sodas_api_base_url (str): SODAS+ API Base URL
        user_id (str): User ID
        refresh_token (str): Refresh Token

    """
    optionUserLogin = {
        'url': urljoin(sodas_api_base_url, '/api/v1/authnz/authentication/user/refreshUser'),
        'data': {
            'id' : user_id,
            'refreshToken' : refresh_token
        }
    }

    try :
        res = requests.post(optionUserLogin['url'],
                        data=optionUserLogin['data']
                        )

        if res.status_code != 201:
            raise Exception(res.status_code)
        else :
            res = res.json()
            return res['accessToken']
    except Exception as e:
        print(e)