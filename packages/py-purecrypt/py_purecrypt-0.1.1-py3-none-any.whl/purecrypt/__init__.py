from .method import Method
from .crypt_abc import Crypt

METHOD_SHA512 = Method.SHA512
METHOD_SHA256 = Method.SHA256
METHOD_MD5 = Method.MD5
METHOD_DEFAULT = METHOD_SHA512


def mksalt(method=None, *, rounds=None):
    if method is None:
        method = METHOD_DEFAULT
    return Crypt.generate_salt(method, rounds)


def crypt(word, salt=None):
    if salt is None:
        salt = METHOD_DEFAULT
    if isinstance(salt, Method):
        salt = Crypt.generate_salt(salt)

    return Crypt.encrypt(word, salt)
