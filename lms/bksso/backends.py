from social_core.backends.oauth import BaseOAuth2
from django.contrib.auth import get_user_model
# from django.conf import settings

User = get_user_model()

class BKCustomBackend(BaseOAuth2):
    """BK OAuth authentication backend"""
    name = 'bksso'
    AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def get_user_details(self, response):
        """Return user details from BK account"""
        return {
            'username': response.get('login'),
            'email': response.get('email') or '',
            'first_name': response.get('name')
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.github.com/user?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)
