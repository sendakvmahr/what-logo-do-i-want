import os
from bs4 import BeautifulSoup

remove = ".references, #catlinks, .toc".split(", ")
search_for = "#bodyContent li a"
wiki_url = "https://en.wikipedia.org"

files = os.listdir("fetched")

def keep_link(href):
    result = href != None
    for item in ["action=edit", "#", ":"]: # is for a lot of wikimedia, external, and file links
        result = result and item not in href
    return result

def process_for_companies():
    total_brands = 0
    for file in files:
        with open("./fetched/" + file, encoding="utf-8") as f:
            html_data = f.read()
        soup = BeautifulSoup(html_data, 'html.parser')
        for tag in remove:
            elements = soup.select(tag)
            for el in elements: el.decompose()
        links = soup.select("#bodyContent li a")
        clean_links = []
        for l in links:
            href = l.get("href")
            if keep_link(href):
                clean_links.append(wiki_url + href)
        with open("./indiv_articles_cleaned/" + file, "w", encoding="utf-8") as f:
            f.write("\n".join(clean_links))
        total_brands += len(clean_links)
    print(total_brands)
process_for_companies()

