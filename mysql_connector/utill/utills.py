# python3自带的函数库，没有使用额外框架
import hashlib
import os

from flask import Response, make_response, request


def myBcryptEncoder(password):
    # 将字符串密码转换为字节串
    password_bytes = password.encode('utf-8')

    # 生成盐并进行加密
    salt = os.urandom(8)  # 生成8字节的盐
    dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)  # 使用 PBKDF2 算法进行加密

    # 将盐和密文组合后转换为十六进制存储，只保存部分密文
    encoderPassword_str = salt.hex() + dk.hex()[:16]
    print("加密后的密文：", encoderPassword_str)

    return encoderPassword_str


def myCheckpw(password, encoderPassword):
    # 打印验证的密码明文和密文
    print("验证的密码明文：", password)
    print("验证的密码密文：", encoderPassword)

    # 从存储的密文中提取盐
    salt = bytes.fromhex(encoderPassword[:16])  # 前16个字符是盐的十六进制表示
    stored_password_hash = encoderPassword[16:]  # 剩下的是部分密码散列

    # 将输入的密码字符串转换为字节串并再次加密
    password_bytes = password.encode('utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)

    # 比较
    if dk.hex()[:len(stored_password_hash)] == stored_password_hash:
        print("Password is correct")
        return True
    else:
        print("Password is incorrect")
        return False


# 按传入对象列表大小增加占位符
# [1,2,3]=====>[,%s ,%s,%s]主要用于in查询
def myGetPlaceHolders(preDataList):
    placeholders = ', '.join(['%s'] * len(preDataList))
    return placeholders


# 将传入对象进行转换，可序列
def myToDir(dataList):
    dataResultList = []
    for perData in dataList:
        resultData = perData.to_dict()
        dataResultList.append(resultData)

    return dataResultList


def myFolderExitsAndMkdir(fileFolder):
    if not os.path.exists(fileFolder):
        os.makedirs(fileFolder)
    return True


# origin='http://127.0.0.1:3000'
# origin='http://localhost:3000'
def set_cors_headers(response, origin='*'):
    """
    Sets CORS headers for a response object and returns the modified response.
    :param response: Response object
    :param origin: A string that specifies the origin which should be allowed to access the resource.
    :return: Modified response object with CORS headers
    """
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # 如果需要处理 cookies
    return response
