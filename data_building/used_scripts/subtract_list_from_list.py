"""
One time script used many times to remove duplicates
of links from categories during merging
"""

import os

file_1 = "./lists_of_links/media_and_communication.txt"
main = """
        ./lists_of_links/misc_product.txt
	./lists_of_links/dental_pharmaceutical.txt
	./lists_of_links/convenience_store.txt
	./lists_of_links/sports_clothing.txt
	./lists_of_links/electronics.txt
	./lists_of_links/software.txt
	./lists_of_links/media_and_communication.txt
	./lists_of_links/store.txt
	./lists_of_links/alcohol.txt
	./lists_of_links/money.txt
	./lists_of_links/sports.txt
	./lists_of_links/restaurant.txt
	./lists_of_links/utilities.txt
	./lists_of_links/adult.txt
	./lists_of_links/gas.txt
	./lists_of_links/gaming.txt
	./lists_of_links/esports.txt
""".split("\n")
subtract = """
	./lists_of_links/electronics.txt
""".split("\n")

#subtract = main

subtract = subtract[1:-1]
subtract = [s.strip() for s in subtract]

links = set()

with open(file_1) as f:
    links = set(f.readlines())
for file in subtract:
    with open(file) as f:
        links2 = set(f.readlines())
    links = links - links2
print(len(links))
with open(file_1, "w") as f:
    f.writelines(list(links))
