import os
READ_DIR = "./lists_of_links/"
OUTPUT_DIR = "duplicate_links.txt"
EXCLUDE_LIST = []

try:
    with open("exclude_from_fetches.txt") as f:
        EXCLUDE_LIST = list(map(lambda x: x.strip(), f.readlines()))
except:
    pass

searching_for = set()
if __name__ == "__main__":
    
    repeat_links = {}
    links = {}
    files = [READ_DIR + f for f in os.listdir(READ_DIR)]
    for fi in range(len(files)):
        file = files[fi]
        with open(file) as f:
            file_links = [x.strip() for x in f.readlines()]
        for past_read in links.keys():
            past_list = links[past_read]
            for l in file_links:
                if False:
                    searching_for.add(l)
                if l in past_list:
                    if l in repeat_links:
                        repeat_links[l].add(file)
                    else:
                        repeat_links[l] = set([past_read, file])
        links[file] = file_links
        print("{}/{} - {}".format(fi+1, len(files), file))
    with open(OUTPUT_DIR, "w") as f:
        for key, item in repeat_links.items():
            #if len(item) > 2:
            if key not in EXCLUDE_LIST:
                f.write("{}\n".format(key))
                for i in item:
                    f.write("\t{}\n".format(i))
    print("------------")
    for i in list(searching_for):
        print(i)
    
        
            
