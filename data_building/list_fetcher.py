import requests
OUTPUT_PATH = "./fetched/"

def record_html(link):
    r = requests.get(url)
    with open(OUTPUT_PATH + url_output_filename(url), "w", encoding="utf-8") as file:
        file.write(r.text)

def url_output_filename(url):
    return url.split("/")[-1].lower() + ".txt"

with open("urls.txt") as file:
    urls = list(map(lambda x: x.strip(), file.readlines()))
    
for url in urls:
    record_html(url)
