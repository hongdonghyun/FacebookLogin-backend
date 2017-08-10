import requests
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView


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

        debug_result = self.debug_token(token)
        return Response(debug_result)

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
