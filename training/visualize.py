import csv
num_clusters = 200
clusters = {}
extension ="_shape3"
for i in range(num_clusters):
    clusters[i] = []
HTML_FILE_TEMPLATE = """
<html>
<style>
body, html {{
  //background: #808080;
}}
img {{
    width: 50px;
    height: 50px;
//    border: 2px solid green;
}}
body>div {{
  border: 1px solid black;
  //background: #808080;
  max-height: 300px;
  overflow-y: scroll;
  padding: 20px;
}}
body {{
  display: grid;
  grid-template-columns: 51% 51%;
}}
img.trained {{
//    border: 2px solid red;
}}
</style>
{}
<body>
"""

with open("output{}.csv".format(extension), encoding="utf-8") as file:
    reader = csv.reader(file)
    headers = list(next(reader, None))
    i_cluster = headers.index("cluster")
    i_category = headers.index("category")
    i_name = headers.index("name")
    #i_is_train = headers.index("train_set")
    for row in reader:
        link = r"../data_building/images_processed/{}/{}.png".format(
            row[i_category],
            row[i_name]
            )
        #training = row[i_is_train] == "True"
        training = True
        class_str = "class='trained'" if training else ""
        ahref = '<a href={l}><img {c} src="{l}"/></a>'.format(c=class_str, l=link)
        try:
            clusters[int(float(row[i_cluster]))].append(ahref)
        except:
            print(row)
html = ""

for i in range(num_clusters):
    links = clusters[i]
    html += "<div></h2>Cluster {}</h2><br/>".format(i)
    for link in links:
        html += link
    html += "</div>"

with open("output{}.html".format(extension), "w", encoding="utf-8") as file:
    file.write(HTML_FILE_TEMPLATE.format(html))
