
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key ='37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'
def encrypt_data(data):

    try:        
        key = get_random_bytes(16)
        print(f"key: {key}")
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return key, nonce, ciphertext, tag
    except ValueError as e:
        #print(f"Error: {e}")
        return None, None, None, None

def decrypt_data(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

data = b"Laurindo Benjamim"
key, nonce, ciphertext, tag = encrypt_data(data)
print(f"Encrypted data: {key}")
dec = decrypt_data(key, nonce, ciphertext, tag)
print(f"Decrypted data: {dec}")