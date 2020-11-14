"""
goes through all the files, removes links in an exclude list
"""

import os

with open("exclude_from_fetches.txt") as f:
    EXCLUDE_LIST = list(map(lambda x: x.strip(), f.readlines()))
    
files = ["./lists_of_links/" +  x for x in os.listdir("./lists_of_links/")]

for file in files:
    with open(file) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    new = []
    for line in data:
        lower = line.lower()
        if "list" not in lower and \
           "type" not in lower and \
           line not in EXCLUDE_LIST:
            new.append(line)
    with open(file, "w") as f:
        print(new)
        f.writelines(new)
