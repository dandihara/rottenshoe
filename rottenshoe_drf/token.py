import jwt
from django.conf import settings

import os

def decoder(token):
    return jwt.decode(token,os.environ['SECRET_KEY'],algorithms =settings.SIMPLE_JWT['ALGORITHM'])
