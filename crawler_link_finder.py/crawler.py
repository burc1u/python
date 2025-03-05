#!/usr/bin/env python3

import requests
###########################################


# this code is meant to find all subdomains of a given target


###########################################






# url of the website where you want to discover subdomains
target_url="google.com"

def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        # if domain does not exist
        pass

with open("path_to_file","r")  as wordlist_file:
    # iterate over each word in file
    for line in wordlist_file:
        # strip whitespace
        word=line.strip()
        # append word from file to target url to create the subdomain
        test_url=word+"."+target_url
        response=request(test_url)
        if response:
            print("[+] Discovered subdomain: "+ test_url)

