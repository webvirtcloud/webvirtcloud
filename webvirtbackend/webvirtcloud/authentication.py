from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

from account.models import Token


class TokenAuthentication(BaseTokenAuthentication):
    model = Token
    keyword = "Bearer"
