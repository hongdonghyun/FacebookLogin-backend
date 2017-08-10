import requests
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class FacebookLoginAPIView(APIView):
    FACEBOOK_APP_ID = '269436596886905'
    FACEBOOK_SECRET_CODE = 'b38d960268ebaf587be7a5650f1d84b8'
    APP_ACCESS_TOKEN = '{}|{}'.format(
        FACEBOOK_APP_ID,
        FACEBOOK_SECRET_CODE,
    )

    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise APIException('token require')

        self.debug_token(token)
        user_info = self.get_user_info(
            token=token,
        )
        if User.objects.filter(username=user_info['id']).exists():
            user = User.objects.get(username=user_info['id'])
        else:
            user = User.objects.create_facebook_user(user_info)

        token, token_created = Token.objects.get_or_create(user=user)

        ret = {
            'token': token.key,
            'user': {
                'pk': user.pk,
                'username': user.username
            }
        }
        return Response(ret)

    def debug_token(self, token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': self.APP_ACCESS_TOKEN
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise APIException('token invalid')
        else:
            return result

    @staticmethod
    def get_user_info(token):
        url_user_info = 'https://graph.facebook.com/v2.9/me'
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result
