#!/usr/bin/env python3
import requests


target_url=""
# get the keys from the website login form
data={"username":"fff","password":"ddd","Login":"123"}
response=requests.post(target_url,data=data)
print(response.content)