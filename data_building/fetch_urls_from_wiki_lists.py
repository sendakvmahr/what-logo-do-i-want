import requests
import os
from bs4 import BeautifulSoup

OUTPUT_PATH = "./lists_of_links/"
TO_REMOVE = ".references, #catlinks, .toc, .navbox".split(", ")
SEARCH_FOR = "#bodyContent li a"
WIKI_URL = "https://en.wikipedia.org"


def get_links(link):
    #records links from a wiki "list of things" page
    r = requests.get(url)
    return process_html(r.text)

def url_output_filename(url):
    return url.split("/")[-1].lower() + ".txt"

def keep_link(href):
    result = href != None
    for item in ["action=edit", "#", ":"]: # is for a lot of wikimedia, external, and file links
        result = result and item not in href
    return result

def process_html(html_data):
    """ Gets links from html data, excludes edit links"""
    soup = BeautifulSoup(html_data, 'html.parser')
    # deletes links that tend not to be part of lists
    for tag in TO_REMOVE: 
        elements = soup.select(tag)
        for el in elements: el.decompose()
        
    # selects collects all possible good links
    links = soup.select(SEARCH_FOR)
    clean_links = set()
    for l in links:
        href = l.get("href")
        if keep_link(href):
            clean_links.add(WIKI_URL + href)
    return clean_links


if __name__ == "__main__":
    with open("lists_of_lists_urls.txt") as file:
        urls = list(map(lambda x: x.strip(), file.readlines()))
    for i in range(len(urls)):
        url = urls[i]
        all_urls = list(get_links(url))
        file_name = url_output_filename(url)
        with open(OUTPUT_PATH + file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(all_urls))
        print("{}/{}".format(i+1, len(urls)))
