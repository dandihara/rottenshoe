import jwt
from django.conf import settings

def decoder(token):
    return jwt.decode(token,settings.SECRET_KEY,algorithms =settings.SIMPLE_JWT['ALGORITHM'])
