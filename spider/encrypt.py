# coding=utf-8
# import os
# import base64
# import platform
# import json

# if platform.system() == 'Darwin':
#     try:
#         import crypto
#         import sys
#         sys.modules['Crypto'] = crypto
#     except ImportError:
#         pass


# from Crypto.Cipher import AES


# # https://github.com/darknessomi/musicbox/wiki/网易云音乐新版WebAPI分析
# def aes_encrypt(text, secKey):
#     pad = 16 - len(text) % 16
#     text = text + pad * chr(pad)
#     encryptor = AES.new(secKey, 2, '0102030405060708')
#     ciphertext = encryptor.encrypt(text)
#     ciphertext = base64.b64encode(ciphertext)
#     return ciphertext


# def rsa_encrypt(text, pubKey, modulus):
#     text = text[::-1]
#     rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
#     return format(rs, 'x').zfill(256)


# def create_secretKey(size):
#     return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))[0:16]


def gen_data():
    # text = {
    #     'username': '邮箱',
    #     'password': '密码',
    #     'rememberLogin': 'true'
    # }

    # modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    # nonce = '0CoJUm6Qyw8W8jud'
    # pubKey = '010001'
    # text = json.dumps(text)
    # secKey = create_secretKey(16)
    # encText = aes_encrypt(aes_encrypt(text, nonce), secKey)
    # encSecKey = rsa_encrypt(secKey, pubKey, modulus)

    encText = '0P8yMxf0sOcnMZVRiVLwwtKb2AV2QmmPf + kLpLSEMJGwUqlWD + Dz9dF7dePAbmN7ezi1wLpvRWlSsJh / ExD9bUAwHzM9dKFK + wwCUUjH7ZmfD9mD2zHLJ0 / xpXGxUrx0pfxe / 7ZnF4HBEsOXcWceUxLY5nysq59OO8zVRGyXtk8QzIQxAicQRqL2Wyen8QTc'  # noqa
    encSecKey = '97a9e831599736380d7377a9910ef2de8503d8959b4f0f4e3abf34c0203b38b845d4f78a10ab0becdb471eaced043aafaa1645e7f6eb7343f71dc430a92e12720a9ddf04e618010b4cc613f2eb4c0da15a420750796cc26815ede6f69c0d9c4420386cff288491cfa423d16d9d18ceb188ffd1c6447d2f8a1524f8c478fab9d4'  # noqa
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data
