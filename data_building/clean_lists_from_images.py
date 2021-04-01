"""
After manually going through images and removing non-logo images,
run this to update the corresponding list of links to match. That way, if run on
another computer, you can just use the recorded list of links. 
"""

import os
# leave out demoscene, it has no links
"""
names=[
    'adult',
    'alcohol',
    'convenience_store',
    'dental_pharmaceutical',
    'electronics', 'esports',
    'food_drink',
    'gaming',
    'gas',
    'media_and_communication',
    'misc',
    'money',
    'restaurant',
    'software',
    'sports',
    'sports_clothing',
    'store',
    'utilities'
]
"""
g_play_names = os.listdir("./lists_of_links/google_play")



def remove_extension(f):
    return ".".join(f.split(".")[:-1])
for name in g_play_names:
    if name == "cat_list.txt": continue
    check_list = "./lists_of_links/google_play/{}".format(name)
    files = "./images/g_play/{}".format(remove_extension(name))
    output = check_list

    all_images = [remove_extension(f) for f in os.listdir(files)]
    print(all_images)
    total_images = len(all_images)

    with open(check_list) as f:
        full_urls = [x.strip().split("\t") for x in f.readlines()]

    new = []
    for f_url in full_urls:
        file_name = f_url[0]
        url = f_url[1]
        if file_name in all_images:
            new.append("\t".join(f_url))
            all_images.remove(file_name)
    with open(output, "w") as f:
        f.write("\n".join(new))
"""
for name in names:
    print(name)
    check_list = "./lists_of_links/{}.txt".format(name)
    files = "./images/{}".format(name)
    #output = check_list.split(r"/")[-1]
    output = check_list

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

"""