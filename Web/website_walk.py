#!/usr/bin/python3
# -*- coding: utf-8 -*-

# an os.walk like program for websites
# it find all urls from www.domain.com


import urllib.request
import re
import time as t


linkExp = r'"http(.*?)"'
linkExp2 = r'"(.*?)"'
website = "https://reactos.org"
name = "reactos"
illegal = """ \\<>{}"'"""

def get_links(url):
    """Return a list of all urls present in the webpage"""
    try:
        response = urllib.request.urlopen(url)
    except:
        return []
    # find all things between quotes
    links = re.findall(linkExp2, str(response.read()))
    urls = set()
    for s in links:
        while s[0] in illegal:
            s = s[1:]
        if '?' in s:
            s = s[:s.index('?')]
        if s.startswith('http'):
            urls.add(s)
        elif s.endswith(('.html', '.php', '.htm', '.xml')): # won't starts with 'http'
            urls.add(website + s) # sometimes there is just the path

    return urls

def main():
    visited = set()
    toVisit = set()
    toVisitNext = set()
    # only keeps urls in the website
    toVisit = set(filter(lambda x: website in x, get_links(website)))

    while len(toVisit) != 0: #len(visited) < 100:
        for page in toVisit:
            if page in visited:
                continue
            # only keeps urls with the website we want
            toVisitNext |= set(filter(lambda x: website in x, get_links(page)))
            visited.add(page)
        toVisit = toVisitNext.copy()
        toVisitNext = set()

    with open(name + ".txt", "w") as file:
        for url in sorted(visited):
            file.write(url + "\n")

if __name__ == "__main__":
    main()
