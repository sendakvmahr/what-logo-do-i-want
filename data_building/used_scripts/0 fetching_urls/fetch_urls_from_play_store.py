"""
reads list_of_lists_urls.py ande gathers links that may have logos on them.
"""
import requests
import os
from bs4 import BeautifulSoup

OUTPUT_PATH = "./lists_of_links/google_play/"

def url_output_filename(url):
    return url.split("/")[-1].lower() + ".csv"

def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser').find("body")
    return soup 

def process_html(soup):
    """Gets apps image urls and their app name """
    result = {}
    apps = soup.find_all(class_="Vpfmgd")
    for a in apps:
        title = a.find("div", class_="b8cIId ReQCgd Q9MA7b").find("a").find("div")
        img = a.find("img", class_="QNCnCf")
        if len(title.contents) >= 1 and ("data-src" in img.attrs or "src" in img.attrs):
            if "src" in img.attrs:
                img = img.attrs["src"]
            else:
                img = img.attrs["data-src"]
            title = title.contents[0]
            title = title.split("-")[0].split(":")[0].strip()
            result[title] = img        
    return result

def create_output_file(di):
    result = ""
    for title, image in di.items():
        result += "{}\t{}\n".format(title.replace("\t", " "), image)
    return result

if __name__ == "__main__":
    with open("lists_of_links/google_play/cat_list.txt") as file:
        urls = list(map(lambda x: x.strip(), file.readlines()))
    for i in range(len(urls)):
        url = urls[i]
        soup = get_html(url)
        images = process_html(soup)
        #all_urls = list(get_links(url))
        file_name = url_output_filename(url)
        with open(OUTPUT_PATH + file_name, "w", encoding="utf-8") as f:
            f.write(create_output_file(images))
