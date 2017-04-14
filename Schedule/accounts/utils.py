import random
import string


def token_generator(size=25, chars=string.ascii_letters+string.digits+"-"+"_"):
    new_token = ""
    for _ in range(size-15):
        new_token += random.choice(chars)
    new_token += "."
    for _ in range(size-10):
        new_token += random.choice(chars)
    new_token += "."
    for _ in range(size):
        new_token += random.choice(chars)
    return new_token


def create_token(instance):
    new_token = token_generator()
    token_class = instance.__class__
    qs = token_class.objects.filter(token=new_token)
    if qs.exists():
        return create_token()
    return new_token

