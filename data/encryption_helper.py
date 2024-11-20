def encrypt_user_id(user_id):
    from cryptography.fernet import Fernet
    key = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
    fernet = Fernet(key)
    return fernet.encrypt(user_id.encode()).decode()

def decrypt_user_id(encrypted_id):
    from cryptography.fernet import Fernet
    key = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_id.encode()).decode()