import jwt
import datetime


def create_token(nickname,email,id):
    exp = datetime.datetime.now() + datetime.timedelta(days=7)
    payload = {
        'id' : id,
        'exp' : exp,
        'email' : email,
        'nickname' : nickname
    }
    return jwt.encode(payload,"secret_key is me",algorithm = 'HS256')

def decoder(token):
    data = jwt.decode(token,"secret_key is me", algorithms = "HS256")
    # if data['exp'] > datetime.datetime.utcnow():
    #     return {'result' : 'expried token!'}
    return jwt.decode(token,"secret_key is me",algorithms ="HS256")