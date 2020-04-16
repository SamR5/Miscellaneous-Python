#!/usr/bin/python3
# -*- coding: utf-8 -*-

# an os.walk like program for websites
# it find all urls from www.domain.com

import os
import urllib.request
import re
import pickle as pk


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
        try:
            while s[0] in illegal:
                s = s[1:]
        except IndexError:
            continue
        if '?' in s:
            s = s[:s.index('?')]
        if s.startswith('http'):
            urls.add(s)
        elif s.endswith(('.html', '.php', '.htm', '.xml')):
            urls.add(website + s) # sometimes there is just the path
    return urls

def infgen():
    while 1:
        yield True

def main():
    global visited, toVisit
    try:
        with open(name + ".tmp", "rb") as sv:
            data = pk.load(sv)
        visited = data["visited"]
        toVisit = data["toVisit"]
    except:
        visited = set()
        toVisit = set(filter(lambda x: website in x, get_links(website)))

    toVisitNext = set()

    while len(toVisit) != 0:
        for page in toVisit:
            if page in visited:
                continue
            # only keeps urls with the website we want
            toVisitNext |= set(filter(lambda x: website in x, get_links(page)))
            visited.add(page)
        toVisit = toVisitNext.copy()
        toVisitNext = set()
        # save the results each visit to resume if crash or big website
        with open(name + ".tmp", "wb") as sv:
            pk.dump({"visited":visited, "toVisit":toVisit}, sv)
        print(1)

    with open(name + ".txt", "w") as f:
        for url in sorted(visited):
            f.write(url + "\n")
    os.remove(name + ".tmp")

if __name__ == "__main__":
    main()
        
