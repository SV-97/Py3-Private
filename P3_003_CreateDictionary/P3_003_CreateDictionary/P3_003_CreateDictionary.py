#works together with P3_002 to create dictionaries for translation

import sys
lan1 = input("Enter language 1: ").lower()
lan2 = input("Enter language 2: ").lower()
path = input("Enter optional path: ").lower()
filename = path + "dict-" + lan1 + "-" + lan2 + ".txt"
alt_filename =  path + "dict-" + lan2 + "-" + lan1 + ".txt"
try:
    open(filename, "r")
    print("Dictionary already exists!")
    sys.exit
except FileNotFoundError:
    try:
        open(alt_filename, "r")
        print("Dictionary already exists!")
        sys.exit
    except FileNotFoundError:
        with open(filename, "w") as dict:
            fobj = open(filename, "w")
            while True:
                lan1_word = input("Enter " + lan1 + " Word: ")
                lan2_word = input("Enter " + lan2 + " Word: ")
                dict.write("{} {}\n".format(lan1_word, lan2_word))
                b  = input("Add another pair? Y/n ").lower()
                if b == "n":
                    break