import hashlib
import os
import random
import string
import getpass

"""
Known-Issues:
    - In one run of the program you can add the same domain multiple times (If anyone is so inclined you'd have to read known_domains from the modified files each iteration of the main loop)
Additional ideas:
    - reading username and adding that to the salt (getpass.getuser())
    - saving the domains(encrypted?)
"""
known_domains = []
if len(known_domains) > 0:
    print("Known Domains are: ")
    for x in known_domains:
        print("     Domain: {:^50} Length: {:^3}".format(x[0], x[1]))
salt = "salty_s4l7" # primary salt to set
directory = os.path.dirname(__file__)
absolute_path = input("[Path]({}/archive): ".format(__file__)) # additional salt depending on location of the file(or input if path of original generation is known)
if not absolute_path:
    relative_path  = "/archive"
    absolute_path = directory + relative_path
seed = salt + absolute_path

alphabet = string.ascii_letters
without = list("OIlL")
for letter in without:
    alphabet = alphabet.replace(letter, "")
pw_chars = alphabet + "123456789" + "!,;.-_+-*()[]{}$%=?"

master_password = False
master_password_check = True
while master_password != master_password_check:
    master_password = getpass.getpass()
    master_password_check = getpass.getpass("Reenter Password: ")
    if master_password != master_password_check:
        print("Passwords don't match!")
while True:
    with open(__file__, "r+") as file:
        rnd = random.Random(seed)
        domain = input("Domain: ")
        len_ = input("[Length](25): ")
        len_ = int(len_) if len(len_) > 0 else 25
        if True: # set to False if you don't want to use this as password manager but rather password generator
            if len(known_domains) < 1 or domain not in [x[0] for x in known_domains]:
                copy = file.readlines()
                for i in range(len(copy)):
                    if "known_domains = [" in copy[i]:
                        if "[(" not in copy[i]:
                            copy[i] = copy[i].replace("known_domains = [", 'known_domains = [("{}", {})'.format(domain, len_))                   
                        else:
                            copy[i] = copy[i].replace("]", ', ("{}", {})]'.format(domain, len_))                       
                        break
                file.seek(0)
                file.writelines(copy)
                file.truncate()
        abs_salt = "".join(rnd.choices(pw_chars, k=50))
        hash_str = abs_salt + master_password + domain
        randomized_iterations = 9600 # still need a good idea for this
        hashed = hashlib.pbkdf2_hmac("sha512", hash_str.encode(), str(rnd.randint(0, int(1e100))+len_).encode(), randomized_iterations)
        rnd2 = random.Random(hashed.hex())
        print("".join(rnd2.choices(pw_chars, k=len_)))

""" Not going to save the data - unnecessary security risk
directory = os.path.dirname(__file__)
absolute_path = input("[Path]: ")
if not absolute_path:
    relative_path  = "/archive"
    absolute_path = directory + relative_path

with open(absolute_path, "r+") as archive:
    password = input("Password: ").encode()
    pw_hash = hashlib.sha512(password).hexdigest()
    print(pw_hash)
    arch_pw = archive.read(128)
    print("arch_pw = {}".format(arch_pw))
    def write():
        rnd = random.Random(password)
        while True:
            domain = input("Domain: ")
            len_ = int(input("Lenght: "))
            pw = "".join(rnd.choices(pw_chars, len_))

    def read():
        print("reading")
    if not arch_pw:
        archive.write(pw_hash + "\n") 
        write()
    else:
        if pw_hash == arch_pw:    
            if input("Read(Y) or Write(n): ") == "n":
                write()
            else:
                read()
        else:
            print("Wrong Password!")
"""