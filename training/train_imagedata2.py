import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
import pickle
"""
First iteration
k means cluster with no image data
"""
data = pd.read_csv("../data_building/output.csv")

color_cols = [
    #"number of colors",
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
    #"percent_bg",
    #"percent color1",
    #"percent color2",
    #"percent color3",
]
imagedata_cols = ["imagedata_{}".format(i) for i in range(16*16)]
categorical_cols = ["category", "profile"]
to_save = ["name", "category"]
primary_colors = [
    "primary color r",
    "primary color g",
    "primary color b",
    "primary color a",
]
bg_colors = [
    "primary color r",
    "primary color g",
    "primary color b",
    "primary color a",
]
primary_percents = [
    'percent color1'
]

saved = data[to_save]
data = data.drop(columns=to_save)
data["percent_logo"] = data[imagedata_cols].sum(axis=1) / (16**2)
#data[primary_colors] = data[primary_colors] * 255

"""
for color in ["r", "g" ,"b"]:
    for i in range(3):
        term = ["primary", "secondary", "tertiary"][i]
        new_col = "{} color {}2".format(term, color)
        color_col = "{} color {}".format(term, color)
        percent_col = "percent color{}".format(i+1)
        data[new_col] = data[color_col] * data[percent_col]
"""

def buff(x):
    return lambda y: y*x

primary_percent_transformer = Pipeline(steps = [
    ('imp_color', FunctionTransformer(buff(20))),
    ("stan_color", StandardScaler()),
    ]
)
primary_color_transformer = Pipeline(steps = [
    ("stan_color", StandardScaler()),
    ('imp_color', FunctionTransformer(buff(10))),
    ]
)

bg_transformer = Pipeline(steps = [
    ("stan_color", StandardScaler()),
    ('imp_color', FunctionTransformer(buff(10))),
    ]
)
cat_transformer = Pipeline(steps = [
    ('cat_cat', OneHotEncoder(handle_unknown='ignore')),
    ]
)

profile_transformer = Pipeline(steps = [
    ('cat_prof', OneHotEncoder(handle_unknown='ignore')),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ('imagedata', StandardScaler(), imagedata_cols + color_cols),
        #('number_cols', StandardScaler(), ["number of colors"]),
        #('num', StandardScaler(), color_cols),
        ('colors', primary_color_transformer, primary_colors + bg_colors),
        ('bgcolors', bg_transformer, ["percent_bg"]),
        #('colors_per', primary_percent_transformer, primary_percents),
        #('category', cat_transformer, ["category"]),
        ('profile', profile_transformer, ["profile"]),
    ]
)
#35
cluster = KMeans(n_clusters=65, random_state=0)

model = Pipeline(
    steps=[
        ('preprocessor', preprocessor),
        ('model', cluster)
        ]
)
#train, test = train_test_split(data)

model.fit_transform(data, [])
preds = pd.Series(model.predict(data), name="cluster")

results = pd.concat([saved, data, preds], axis=1)
results.to_csv("output_shape3.csv")


pickle_out = open("cluster_algo.pickle","wb")
pickle.dump(cluster, pickle_out)
pickle_out.close()

pickle_out = open("data.pickle","wb")
pickle.dump(preprocessor.transform(data), pickle_out)
pickle_out.close()

import visualize
