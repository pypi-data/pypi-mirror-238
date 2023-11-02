import hashlib

def md5(plain_text:str)->str:
    """
    获取MD5摘要
    """
    md5=hashlib.md5()
    md5.update(plain_text.encode())
    return md5.hexdigest()