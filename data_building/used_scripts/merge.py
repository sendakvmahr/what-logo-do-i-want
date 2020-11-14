import os
# cax software
# list_of_marketing_research_firms.txt finance
merge = """
        ./lists_of_links/list_of_eda_companies.txt
        ./lists_of_links/softwares.txt
""".split("\n")
merge = merge[1:-1]
merge = [s.strip() for s in merge]
final_name = "./lists_of_links/" + "software" + ".txt"

for f in merge:
    print(f)

links = set()

for file in merge:
    with open(file) as f:
        #links = links.intersect(set(f.readlines()))
        links = links.union(set(f.readlines()))
    
with open(final_name, "w") as f:
    f.writelines(list(links))

    
for file in merge:
    os.remove(file)
