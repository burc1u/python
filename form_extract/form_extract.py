#!/usr/bin/ env python3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

##################################
#this code extracts all the forms from a website using a given url
##################################

def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        pass


# url of the target page
target_url=""
response=request(target_url)
# use BeautifulSoup to parse the html
parsed_html=BeautifulSoup(response.content)
forms_list=parsed_html.findAll("form")

for form in forms_list:
    # get the action the form is doing
    action=form.get("action")
    # create an url to post the fork
    post_url=urljoin(target_url,action)
    # get the method
    method=form.get("method")
    # get all the input fields
    inputs_list=form.findAll("input")

    # dictionary to post
    post_data={}

    for input in inputs_list:
        # get the name of the input
        input_name=input.get("name")
        # get the type of the input
        input_type=input.get("type")
        input_value=input.get("value")

        if input_type=="text":
            input_value="text"
        # set the value of the name in dict
        post_data[input_name]=input_value
    # send the form with the created url and created dict as data
    requests.post(post_url,data=post_data)


