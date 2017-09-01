def getchars(data):
    byteslist = []
    for chars in data:
        byteslist.append(ord(chars))
    return byteslist
def encrypt(data, key):
    crypted = []
    data = getchars(data)
    for chars in data:
        data = chars+int(key)
        crypted.append(str(chr(data)))
    data = ''.join(crypted)
    print data
    return data

def decrypt(data, key):
    decrypted = []
    data = getchars(data)
    for chars in data:
        data = chars - key
        decrypted.append(str(chr(data)))
    data = ''.join(decrypted)
    print data
    return data

