
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import re

def getDERKey(dw30sfpkey, dw30sfpprs):
    try: 
        key = dw30sfpkey
        passkey = dw30sfpprs
        key = bytes(key, encoding='utf-8')
        passkey = bytes(passkey, encoding='utf-8')
        p_key = serialization.load_pem_private_key(key, password=passkey, backend=default_backend())
        pkb = p_key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption())
    except Exception as e:
        print(e)        

    return pkb


def getPEMKey(dw30sfpkey, dw30sfpprs):

    try: 
        key = dw30sfpkey
        passkey = dw30sfpprs
        key = bytes(key, encoding='utf-8')
        passkey = bytes(passkey, encoding='utf-8')
        p_key = serialization.load_pem_private_key(key, password=passkey, backend=default_backend())
        pkb = p_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption())
        pkb = pkb.decode("UTF-8")
        pkb = re.sub("-*(BEGIN|END) PRIVATE KEY-*\n", "", pkb).replace("\n", "")
    except Exception as e:
        print(e)

    return pkb