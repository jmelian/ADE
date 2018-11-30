from django.conf import settings

_PASSPHRASE=settings.SECRET_KEY
_PROJECT_NAME='ADE'


def generate_RSA_files(bits=2048, code=_PASSPHRASE):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA
    
    key = RSA.generate(bits) 
    private_key = key.export_key(passphrase=code, pkcs=8, protection="scryptAndAES128-CBC")
    file_out = open(_PROJECT_NAME+"_private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open(_PROJECT_NAME+"_public.pem", "wb")
    file_out.write(public_key)
    file_out.close()
    return 


def verify_sign(public_key_loc, signature_file, data_file):
    '''
    Verifies with a public key from whom the data came that it was indeed 
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    return: Boolean. True if the signature is valid; False otherwise. 
    '''
    from Crypto.PublicKey import RSA 
    from Crypto.Signature import PKCS1_v1_5 
    from Crypto.Hash import SHA256 
    from base64 import b64decode 

    pub_key = open(public_key_loc, "r").read() 
    rsakey = RSA.importKey(pub_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    # Assumes the data is base64 encoded to begin with
    digest.update(b64decode(open(data_file).read())) 
    if signer.verify(digest, b64decode(open(signature_file).read())):
        return True
    return False


def encrypt_RSA_file (pub_key_file, data_file, output_file):
    #from __future__ import print_function, unicode_literals
    import base64
    import sys

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5

    pubkey = RSA.importKey(open(pub_key_file).read())
    cipher = PKCS1_v1_5.new(pubkey)
    cipher_text = cipher.encrypt(str.encode(open(data_file).read()))
    cipher_text = base64.b64encode(cipher_text)
    f = open(output_file, 'wb')
    f.write(cipher_text)
    f.close()

def encrypt_RSA_text (pub_key_file, data_text, output_file):
    #from __future__ import print_function, unicode_literals
    import base64
    import sys

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5

    pubkey = RSA.importKey(open(pub_key_file).read())
    cipher = PKCS1_v1_5.new(pubkey)
    cipher_text = cipher.encrypt(str.encode(data_text))
    cipher_text = base64.b64encode(cipher_text)
    #print("cifrado: ", cipher_text)
    f = open(output_file, 'wb')
    f.write(cipher_text)
    f.close()


def decrypt_RSA_file (priv_key_file, data_file, passphrase=_PASSPHRASE):
    import base64
    import sys

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5

    # read key file and a private key object
    privkey = RSA.importKey(open(priv_key_file).read(), passphrase=passphrase)

    # create a cipher object
    cipher = PKCS1_v1_5.new(privkey)

    # decode base64
    cipher_text = base64.b64decode(open(data_file).read())
	
    # decrypt
    plain_text = cipher.decrypt(cipher_text, None)
    #print(plain_text.decode('utf-8').strip())
    #f = open(output_file, 'wb')
    #f.write(plain_text.decode('utf-8').strip())
    #f.close()
    #with open(output_file, 'wb') as f: f.write(plain_text.decode('utf-8').strip())
    #print("texto: ", plain_text)
    return plain_text.decode('utf-8').strip()


def sign_file (priv_key_file, file_to_sign, passphrase=_PASSPHRASE):
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
    import base64

    privkey = RSA.importKey(open(priv_key_file).read(), passphrase=passphrase)
    signer = PKCS1_v1_5.new(privkey)
    digest = SHA256.new()
    digest.update(base64.b64decode(open(file_to_sign).read()))
    sign = signer.sign(digest)

    with open(file_to_sign + '.sha256', 'wb') as f: f.write(base64.b64encode(sign))

