words = {}
while True:
    try:
        fobj = open(input("Enter path to dictionary(relative or absolute): "), "r")
        break
    except FileNotFoundError:
        print("No such file or directory")
for line in fobj:
    line = line.lower().strip()
    pair = line.split(" ")
    words[pair[0]] = pair[1]
    words[pair[1]] = pair[0]
fobj.close()
print(words)

word = " "
while True:
    word = input("Enter a word or press return to close: ").lower()
    if word == "":
        break
    if not word in words:
        print("Unknown word")
    else:
        print("The translation is:", words[word])

import sys
sys.exit()

#alternative solution for reading from file
words = {}
with open(input("Enter path to dictionary(relative or absolute): "), "r") as fobj:
    for line in fobj:
        line = line.lower().strip()
        pair = line.split(" ")
        words[pair[0]] = pair[1]
        words[pair[1]] = pair[0]
