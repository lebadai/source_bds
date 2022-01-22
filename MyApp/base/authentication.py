import base64
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from library.constant.error_codes import BEARER_TOKEN_NOT_FOUND, ERROR_CODE_MESSAGE, BEARER_TOKEN_NOT_VALID

# check token authorize
class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_FOUND,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_FOUND]
            })

        if len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
            })

        receive_token = auth[1]

        user_id, token = self.parse_token(receive_token)
        if not user_id or not token:
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
            })

        return self.check_user_and_token(user_id, token, request)

    @staticmethod
    def parse_token(key):
        try:
            receive_token = base64.b64decode(key)
            receive_token = receive_token.decode()

            _info_list = receive_token.split(':')
            if len(_info_list) != 2:
                return None, None

            user_id = _info_list[0]
            token = _info_list[1]

            return user_id, token
        except ValueError:
            return None, None

    def authenticate_header(self, request):
        return self.keyword

def service_encode_from_json(_dict):
    try:
        data = json.dumps(_dict, cls=DjangoOverRideJSONEncoder)

        data = data.encode('utf-8')

        data = zlib.compress(data)

        return data
    except Exception as ex:
        # logger('--- Error Encode ---')
        # logger(ex)
        return ''

def get_encode_header(request):
    if request:
        client_encode = request.META.get('HTTP_MNV_ENCODE')

        # if MNV_ENCODE_DISABLED == client_encode:
        #     return False

        try:
            client_encode = int(client_encode)
        except (TypeError, ValueError):
            client_encode = 1

        if client_encode == 0:
            return False
    return True