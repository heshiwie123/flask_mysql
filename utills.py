import bcrypt


def myBcryptEncoder(password):
    # 打印需要加密的密码明文
    print("需要加密的密码明文：password======>", password)

    # 将字符串密码转换为字节串
    password_bytes = password.encode('utf-8')

    # 生成盐并进行加密
    salt = bcrypt.gensalt()
    encoderPassword = bcrypt.hashpw(password_bytes, salt)

    # 将加密后的密文转换为字符串用于打印和存储
    encoderPassword_str = encoderPassword.decode('utf-8')
    print("加密后的密文：encoderPassword======>", encoderPassword_str)

    return encoderPassword_str


def myCheckpw(password, encoderPassword):
    # 打印验证的密码明文和密文
    print("验证的密码明文：password======>", password)
    print("验证的密码密文：encoderPassword======>", encoderPassword)

    # 将输入的字符串和密文字符串转换为字节串
    password_bytes = password.encode('utf-8')
    encoderPassword_bytes = encoderPassword.encode('utf-8')

    # 进行密码验证
    if bcrypt.checkpw(password_bytes, encoderPassword_bytes):
        print("Password is correct")
        return True
    else:
        print("Password is incorrect")
        return False

