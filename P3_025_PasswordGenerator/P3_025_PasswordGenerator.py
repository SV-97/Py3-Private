import hashlib
import os
import random # used rather than secrets because secrets doesn't support seeds
import string
import getpass

"""
Known-Issues:
    - In one run of the program you can add the same domain multiple times (If anyone is so inclined you'd have to read known_domains from the modified files each iteration of the main loop)
Additional ideas:
    - reading username and adding that to the salt (getpass.getuser())
    - saving the domains(encrypted?)
    - timeout of password
    - UI
"""
known_domains = []
if len(known_domains) > 0:
    print("Known Domains are: ")
    for x in known_domains:
        print("     Domain: {:^50} Length: {:^3}".format(x[0], x[1]))
salt = "salty_s4l7" # primary salt to set

directory = os.path.dirname(__file__)
absolute_path = input("[Path]({}/archive): ".format(directory)) # additional salt depending on location of the file(or input if path of original generation is known)
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
master_hash = hashlib.sha512(master_password.encode()).digest()
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
        randomizer = int.from_bytes(master_hash, byteorder="big", signed=False)%8        
        randomized_iterations = 2*randomizer**randomizer
        hashed = hashlib.pbkdf2_hmac("sha512", hash_str.encode(), str(rnd.randint(0, int(1e100))+len_).encode(), randomized_iterations)
        rnd2 = random.Random(hashed.hex())
        print("".join(rnd2.choices(pw_chars, k=len_)))