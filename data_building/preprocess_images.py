import os, csv
import urllib
import numpy as np
import PIL.Image as Image
from collections import defaultdict

COLOR_THRESHOLD = .1
COMBINE_THRESHOLD = 50
INPUT_FOLDER ="images"

WEBP_OUTPUT = "images_webp"
SIL_OUTPUT = "images_silhouette"
OUTPUT_FOLDER = "images_processed"

HEADER = [
    "category",
    "name",
    "profile",
    "number of colors",
    "variance r",
    "variance g",
    "variance b",
    "variance a",
    "background color r",
    "background color g",
    "background color b",
    "background color a",
    "primary color r",
    "primary color g",
    "primary color b",
    "primary color a",
    "secondary color r",
    "secondary color g",
    "secondary color b",
    "secondary color a",
    "tertiary color r",
    "tertiary color g",
    "tertiary color b",
    "tertiary color a",
    "percent_bg",
    "percent color1",
    "percent color2",
    "percent color3",
] + ["imagedata_{}".format(i) for i in range(16*16)]

HTML_FILE_TEMPLATE = """
<html>
<style>
body, html {{
  background: #808080;
}}
body>div {{
  border: 1px solid black;
  background: #808080;
  padding: 20px;
}}
body {{
  display: grid;
  grid-template-columns: 31% 31% 31%;
}}
.colordiv {{
    display: inline-block;
    width: 2em; height: 2em;
    margin-left: 1em;
    margin-right: 1em;
}}
</style>
{}
<body>
"""

HTML_TEMPLATE = """
<div>
<img src="{image}"/>
<br/>
<p><b>Profile: </b>{profile}</p>
<p><b>Number of Colors: </b>{num_colors}</p>
<p><b>Background Color: </b><br/><span class="colordiv" style="background:rgba{bg_color};"></span>{bg_color}</p>
<p><b>Primary Color: </b><br/><span class="colordiv" style="background:rgba{color1};"></span>{color1}</p>
<p><b>Secondary Color: </b><br/><span class="colordiv" style="background:rgba{color2};"></span>{color2}</p>
<p><b>Tertiary Color: </b><br/><span class="colordiv" style="background:rgba{color3};"></span>{color3}</p>
<p><b>Variance: </b>{variance}</p>
</div>
"""

class ImageData():
    def __init__(self, imagepath):
        self._imagepath = imagepath
        self._name = imagepath.split("/")[-1]
        self.image_category = "/".join(imagepath.split("/")[1:3])
        self.unquoted_name = urllib.parse.unquote(".".join(self._name.split(".")[:-1]))
        self.unquoted_name = self.unquoted_name.replace('"' ,"").replace('"', "")
        
        image = Image.open(imagepath)
        self.image = image = image.convert("RGBA")
        self._image_data = self.image.getdata()
        self._image_data = [(0, 0, 0, 0) if x[-1] == 0 else x for x in self._image_data]
        image_data_dict = self._get_dict_percentage(self._image_data)
        self.image_data_dict = image_data_dict
        
        self.profile = self.get_profile(image)
        self.num_colors = len(image_data_dict)
        self._num_pixels = image.width * image.height
        self.variance = np.var(list(image_data_dict.keys()), axis=0)
        
        sorted_by_percent = self._list_by_percentage(image_data_dict)
        self.background_color = self._decide_bg_color(sorted_by_percent, image)
        self.primary_colors = self._primary_colors(sorted_by_percent)
        
    def export_image(self, output_folder, option=""):
        """
        resizes image to square by extending it with detected bg color
        and saves it as a png
        """
        if option == "webp":
            dim = 128
            ending = ".webp"
        elif option == "sil":
            dim = 16
            ending = ".png"
        else:
            dim = 128
            ending = ".png"
        folder_path = os.path.join(output_folder)

        final_image = Image.new("RGBA", (dim, dim), color=self.background_color)
        if self.profile == "square":
            size = (dim, dim)
            offset = (0, 0)
        elif self.profile == "portrait":
            width, height = self.image.width, self.image.height
            ratio = dim / height
            size = (int(ratio * width), dim)
            offset= (int((dim - size[0])/2), 0)
        else:
            width, height = self.image.width, self.image.height
            ratio = dim / width
            size = (dim, int(ratio * height))
            offset= (0, int((dim - size[1])/2))
        if "demoscene" in self.image_category or option == "sil":
            to_paste = self.image.resize(size, resample=Image.NEAREST)
        else:
            to_paste = self.image.resize(size, resample=Image.BILINEAR)

        final_image.paste(to_paste, offset, to_paste)

        if option == "sil":
            data = list(final_image.getdata())
            to_reshape = []
            image_01 = []
            for i in range(len(data)):
                is_background = sum(np.var([data[i], self.background_color], axis=0)) < (COLOR_THRESHOLD *2)
                to_reshape += [255, 255, 255, 255] if is_background else [0, 0, 0, 255]
                image_01.append(0 if is_background else 1)
            data = np.array(to_reshape)
            data = data.reshape(dim, dim, 4)
            
            final_image = Image.fromarray(data.astype(np.uint8))
            self.image_mask = image_01

        final_image.save(os.path.join(output_folder, self.image_category, self.unquoted_name) + ending
        )
        

    def get_profile(self, image):
        """Decides portrait, landscape, or square"""
        if image.width == image.height:
            return "square"
        elif image.width > image.height:
            return "landscape"
        return "portrait"

    def _list_by_percentage(self, imagedata, include_percent=False):
        """
        takes dict from dict_percentage
        returns a list(color, percent of picture) sorted by
        the percent of picture the color makes up
        """
        result = []
        for color, count in imagedata.items():
            percentage = count / self._num_pixels
            result.append((percentage, color))
        result.sort(key=lambda x: x[0], reverse=True)
        if not include_percent:
            result = [x[1] for x in result]
        return result
    
    def _get_dict_percentage(self, imagedata):
        """
        returns a dict of {(r, g, b, a) : num_times_appeared}
        """
        result = defaultdict(int)
        for pixel in imagedata:
            result[pixel] += 1
        return result
    

    def _decide_bg_color(self, sorted_colors, image):
        """
        decides on bg color 
        """
        # transparency is always going to be a bg color if it is included
        if (0, 0, 0, 0) in sorted_colors: return (0, 0, 0, 0)

        # only colors that appear on the edge of an image can be a bg color
        width = image.width
        edge_data = []
        for i in range(0, len(self._image_data), width):
            edge_data.append(self._image_data[i])           #left
            edge_data.append(self._image_data[i + width -1])#right
        edge_data += self._image_data[1:width-1]            #top
        edge_data += self._image_data[(-width+1):-1]        #bottom
        edge_data = self._list_by_percentage(self._get_dict_percentage(edge_data))
        return edge_data[0] #return dominant color on edge if no color is found
        
            
    def _primary_colors(self, by_percent):
        """
        returns 3 common but not too similar colors as primary color choices
        """
        sorted_by_percent = list(by_percent)
        sorted_by_percent.remove(self.background_color)
        # includ bg color in results to exclude it, it is removed at the end
        result = [self.background_color]
        i = 0
        while len(result) < 4 and i < len(sorted_by_percent):
            # mess that basically asks for colors to be somewhat different from main colors
            test_color = sorted_by_percent[i]
            append = True
            for r in result:
                is_different = sum(np.var([r, test_color], axis=0))
                is_different = is_different > COMBINE_THRESHOLD
                append = append and is_different
            if append: result.append(test_color)
            i += 1
        if len(result) != 4:
            while len(result) < 4:
                result.append(result[-1])
        return result[1:]
        
    def to_html(self, output_folder):
        save = HTML_TEMPLATE.format(image=os.path.join(output_folder, self.image_category, self.unquoted_name) + ".webp"
        ,
                                    profile = self.profile,
                                    num_colors = self.num_colors,
                                    color1 = self.primary_colors[0],
                                    color2 = self.primary_colors[1],
                                    color3 = self.primary_colors[2],
                                    bg_color = self.background_color,
                                    variance = self.variance)
        return save

    def csv_line(self):
        """ Returns a list that is used as a csv row"""
        return [
            self.image_category,
            self.unquoted_name,
            self.profile,
            self.num_colors,
            self.variance[0],
            self.variance[1],
            self.variance[2],
            self.variance[3],
            self.background_color[0],
            self.background_color[1],
            self.background_color[2],
            self.background_color[3],
            self.primary_colors[0][0],
            self.primary_colors[0][1],
            self.primary_colors[0][2],
            self.primary_colors[0][3],
            self.primary_colors[1][0],
            self.primary_colors[1][1],
            self.primary_colors[1][2],
            self.primary_colors[1][3],
            self.primary_colors[2][0],
            self.primary_colors[2][1],
            self.primary_colors[2][2],
            self.primary_colors[2][3],
            self.image_data_dict[self.background_color],
            self.image_data_dict[self.primary_colors[0]],
            self.image_data_dict[self.primary_colors[1]],
            self.image_data_dict[self.primary_colors[2]],
        ] + self.image_mask

    def __repr__(self):
        return "{n}: \n\tp:  {p}\n\t#c: {c}\n\tbg: {bg}\n\tC:  {C}\n\tv:  {v}".format(
            n = self._name,
            c = self.num_colors,
            bg = self.background_color,
            C = self.primary_colors,
            p = self.profile,
            v = self.variance
        )
html=""
csv_rows = []


outputs = [WEBP_OUTPUT, SIL_OUTPUT, OUTPUT_FOLDER]

for source in os.listdir(INPUT_FOLDER):
    for category in os.listdir(os.path.join(INPUT_FOLDER, source)):
        image_folder = os.path.join(INPUT_FOLDER, source, category)

        for out in outputs:
            if not os.path.isdir(os.path.join(out, source)):
                os.mkdir(os.path.join(out, source))
            if not os.path.isdir(os.path.join(out, source, category)):
                os.mkdir(os.path.join(out, source, category))
        for image in os.listdir(image_folder):

            result = ImageData(os.path.join(image_folder, image))
            for out in outputs:
                output_folder = os.path.join(out, source, category)
                if out == WEBP_OUTPUT:
                    result.export_image(out, "webp")
                elif out == SIL_OUTPUT:
                    result.export_image(out, "sil")
                elif out == OUTPUT_FOLDER:
                    result.export_image(out)
            html += result.to_html(WEBP_OUTPUT)
            csv_rows.append(result.csv_line())
            print(output_folder + "/" + image)
"""
            if stop == 0:
                break;
        if stop == 0:
            break;
    if stop == 0:
        break;

"""
with open("output.html", "w", encoding="utf-8") as file:
    file.write(HTML_FILE_TEMPLATE.format(html))

with open("output.csv", "w", newline="", encoding="utf-8") as csvoutput:    
    writer = csv.writer(csvoutput, delimiter=",")
    writer.writerow(HEADER)
    for info in csv_rows:
        writer.writerow(info)
    
