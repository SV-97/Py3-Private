import hashlib

hash_ = input("Hash: ")
path = input("Path: ")

with open(path, "rb") as file:
    hash_is = hashlib.md5(file.read()).hexdigest()
    hash_should = hash_
    print("""
Is:     {}
Should: {}
    """.format(hash_is, hash_should))
    if hash_is == hash_should:
        
        print("File is valid")
    else:
        print("File is corrupted")
input()