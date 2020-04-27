#!/usr/bin/python3
# -*- coding: utf-8 -*-

# an os.walk like program for websites
# it find all urls from www.domain.com

import os
import urllib.request
import re
import pickle as pk


linkExp = r'href="(.+?)"'
website = "https://www.programiz.com/"
websiteShort = "programiz.com"
name = "programiz"
illegal = """ \\<>{}"'"""
notWanted = [".js", ".css", ".jpg", ".svg", ".png", ".ico"]

def get_links(url):
    """Return a list of all urls present in the webpage"""
    try:
        response = urllib.request.urlopen(url)
    except:
        return []
    # find all things between quotes
    links = re.findall(linkExp, str(response.read()))
    urls = set()
    for s in links:
        try:
            while s[0] in illegal:
                s = s[1:]
        except IndexError:
            continue
        if s[0]=='#': continue
        elif '#' in s:
            s = s[:s.index('#')]
        elif '?' in s:
            s = s[:s.index('?')]
        if any([s.endswith(i) for i in notWanted]):
            continue
        elif s[0] == '/' and websiteShort not in s:
            urls.add(website + s[1:])
        elif s.startswith("http") or s.startswith('www'):
            urls.add(s)
    return urls

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

    with open(name + ".txt", "w") as f:
        for url in sorted(visited):
            f.write(url + "\n")
    try: # in case no links has been found, no .tmp file written
        os.remove(name + ".tmp")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
        
