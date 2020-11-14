import os
check_list = "./lists_of_links/food_drink.txt"
files = "./images/food_drink"
output = check_list.split(r"/")[-1]

def remove_extension(f):
    return ".".join(f.split(".")[:-1])

all_images = [remove_extension(f) for f in os.listdir(files)]
total_images = len(all_images)

with open(check_list) as f:
    full_urls = [x.strip() for x in f.readlines()]

new = []
for url in full_urls:
    file_name = url.split(r"/")[-1].lower()
    if file_name in all_images:
        new.append(url)
        all_images.remove(file_name)

with open(output, "w") as f:
    f.write("\n".join(new))
    
print("urls saved: ", len(new))
print("total images:", total_images)
print("leftover images :")
for i in all_images:
    print("\t", i)
