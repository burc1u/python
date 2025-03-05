#!/usr/bin/env python3
import requests
import re
from urllib.parse import urlparse


###############################################
# this code is meant to discover all the links in a web page

###############################################

# url of the website where you want to discover subdomains
target_url ="http://google.com"
target_links=[]

def extract_links(url):

    response=requests.get(url)
    # find all links in href
    return re.findall(r'(?:href=")(.*?)"', str(response.content))


def crawl(url):


    href_links=extract_links(url)

    for link in href_links:
        # for relative links
        link=urlparse.urljoin(url,link)
        if "#" in link:
            link=link.split("#")[0]

        # some links can be not related to domain
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            # using the function recursively allows to map the entire website
            crawl(link)

crawl(target_url)