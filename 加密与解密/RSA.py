#!/usr/bin/env python
#encoding=utf-8
'''
测试rsa加密解密
'''
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)

# master的秘钥对的生成
private_pem = rsa.exportKey()

with open('master-private.pem', 'w') as f:
    f.write(private_pem)

public_pem = rsa.publickey().exportKey()
with open('master-public.pem', 'w') as f:
    f.write(public_pem)

# ghost的秘钥对的生成
private_pem = rsa.exportKey()
with open('ghost-private.pem', 'w') as f:
    f.write(private_pem)

public_pem = rsa.publickey().exportKey()
with open('ghost-public.pem', 'w') as f:
    f.write(public_pem)


if __name__ == '__main__':
    ###加密
    message = 'hello ghost, this is a plian text'
    with open('ghost-public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message))
        print "这是加密的结果：\n",cipher_text
    ###解密
    # Ghost使用自己的私钥对内容进行rsa 解密
    encrypt_text = cipher_text
    with open('ghost-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)
        print "这是解密的结果：\n",text
    # Master 使用自己的公钥对内容进行签名
    with open('master-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(message)
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        print(u"这是签名message的签名值：\n",signature)
