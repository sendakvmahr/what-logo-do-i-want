"""
After manually going through images and removing non-logo images,
run this to update the corresponding list of links to match. That way, if run on
another computer, you can just use the recorded list of links. 
"""

import os
# leave out demoscene, it has no links

wiki_names=sorted(os.listdir("./lists_of_links/wikipedia"))

g_play_names = sorted(os.listdir("./lists_of_links/g_play"))
g_play_names.remove("cat_list.txt")

def remove_extension(f):
    return ".".join(f.split(".")[:-1])

#for source in ["wikipedia", "g_play"]:
for source in ["wikipedia"]:
    names = wiki_names if source == "wikipedia" else g_play_names
    for name in names:
        #print("========== {} : {}".format(source, name))
        check_list = "./lists_of_links/{}/{}".format(source, name)
        files = "./images/{}/{}".format(source, remove_extension(name))
        output = check_list

        all_images = [remove_extension(f) for f in os.listdir(files)]
        total_images = len(all_images)
        with open(check_list) as f:
            full_urls = [x.strip().split("\t") for x in f.readlines()]

        new = []
        missing = []
        for f_url in full_urls:
            file_name = f_url[0]
            url = f_url[1]
            if file_name in all_images:
                new.append("\t".join(f_url))
                all_images.remove(file_name)
            else:
                missing.append("{} {} {}".format(source, remove_extension(name), file_name))

        with open(output, "w") as f:
            f.write("\n".join(new))

        if len(new) != total_images or len(missing) != 0:
            print("========== {} : {}".format(source, name))
            print("urls saved: {} / {}".format(len(new), len(full_urls)))
            print("total images:", total_images)
            print("delted from csv: {}".format(missing))
