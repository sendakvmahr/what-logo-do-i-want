import os
from bs4 import BeautifulSoup
import requests
import os
import shutil
import time
from io import BytesIO
from PIL import Image


with open("exclude_from_fetches.txt") as f:
    EXCLUDE_LIST = list(map(lambda x: x.strip(), f.readlines()))

OUTPUT_PATH = "./images/"


def save_logo_image(category, link, img_link, image):
    extension = str(img_link).split(".")[-1]
    save_as_name = "{}.{}".format(link.split("/")[-1].lower(), extension)
    save_as_name = OUTPUT_PATH + category + "/" + save_as_name
    if "*" not in save_as_name:
        image.save(save_as_name)

    
def save_image(link, category):
    """saves image, preserving their name and category"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser').find("body")

    images = soup.find_all('img')
    img_index = 0
    searching = img_index != len(images)
    found = False
    img_link = ""
    while searching:
        try:            
            img_link = "https://" + images[img_index].get("src").replace(r"//", "")
            if "static/images" in img_link:
                img_index += 1
                searching = img_index != len(images)
                continue
            image_raw = requests.get(img_link)
            image = Image.open(BytesIO(image_raw.content))
            width, height = image.size
            if width > 50 and height > 50:
                save_logo_image(category, link, img_link, image)
                found = True
                searching = False
            else:
                img_index += 1
                searching = img_index != len(images)
        except requests.exceptions.InvalidURL as e:
            print("invalid url - {}".format(img_link))
            img_index += 1
            searching = img_index != len(images)
        except Exception as e:
            print("--------------------------------------------------")
            print("{} - {} - Exception.".format(category, link))
            print(e)
            print(type(e))
            print("--------------------------------------------------")
    if not found:
        print("{} - {} - no image found.".format(category, link))
        print("--------------------------------------------------")


files = ['./lists_of_links/adult.txt',
         './lists_of_links/alcohol.txt',
         './lists_of_links/convenience_store.txt',
         './lists_of_links/dental_pharmaceutical.txt',
         './lists_of_links/electronics.txt',
         './lists_of_links/esports.txt',
         './lists_of_links/food_drink.txt',
         './lists_of_links/gaming.txt',
         './lists_of_links/gas.txt',
         './lists_of_links/media_and_communication.txt',
         './lists_of_links/megabrands.txt',
         './lists_of_links/misc_product.txt',
         './lists_of_links/money.txt',
         './lists_of_links/restaurant.txt',
         './lists_of_links/software.txt',
         './lists_of_links/sports.txt',
         './lists_of_links/sports_clothing.txt',
         './lists_of_links/store.txt',
         './lists_of_links/utilities.txt'
]

finished = [
    './lists_of_links/adult.txt',
    './lists_of_links/alcohol.txt',
    './lists_of_links/convenience_store.txt',
    './lists_of_links/electronics.txt',
    './lists_of_links/esports.txt'
    './lists_of_links/food_drink.txt',
    './lists_of_links/gaming.txt',
    "./lists_of_links/gas.txt",
    './lists_of_links/megabrands.txt',
]

for f in finished:
    if f in files: files.remove(f)

    
for f in files:
    print(f)
    try:
        cat = f.replace(".txt", "").split("/")[-1].lower()
        os.mkdir(OUTPUT_PATH + cat)
    except OSError as e:
        if type(e) == FileExistsError:
            pass
        else:
            print(e)
            input("Error - double check then continue")
    with open(f) as file:
        urls = list(map(lambda x: x.strip(), file.readlines()))
    for url in urls:
        lower = url.lower()
        save_image(url, cat)
    print("*********************************************************")
    print(f)
            
