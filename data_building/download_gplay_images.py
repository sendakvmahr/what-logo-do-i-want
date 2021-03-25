import os
from bs4 import BeautifulSoup
import requests
import os
import shutil
import time
from io import BytesIO
from PIL import Image
import csv

OUTPUT_PATH = "./images/g_play/"


def save_logo_image(name, link, category):
    print(link)
    image_raw = requests.get(link)
    image = Image.open(BytesIO(image_raw.content))
    #extension = str(link).split(".")[-1]
    extension = "png"
    save_as_name = "{}.{}".format(name, extension).replace("/", " ")
    save_as_name = OUTPUT_PATH + category + "/" + save_as_name
    if "*" not in save_as_name:
        image.save(save_as_name)

   

files = os.listdir("./lists_of_links/google_play")
files.remove("cat_list.txt")    

for f in files:
    try:
        cat = f.replace(".csv", "").split("/")[-1].lower()
        os.mkdir(OUTPUT_PATH + cat)
    except OSError as e:
        if type(e) == FileExistsError:
            pass
        else:
            print(e)
            input("Error - double check then continue")
    with open("./lists_of_links/google_play/" + f) as file:
    	reader = csv.reader(file, delimiter="\t")
    	for row in reader:
    		name = row[0]
    		url = row[1]
    		save_logo_image(name, url, cat)

