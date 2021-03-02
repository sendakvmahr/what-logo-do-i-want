import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

"""
First iteration
k means cluster with no image data
"""
data = pd.read_csv("../data_building/output.csv")

numerical_cols = [
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
]
categorical_cols = ["category", "profile"]
to_save = ["name"]

saved = data[to_save]
data = data.drop(columns=to_save)

numerical_transformer = StandardScaler()

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)

cluster = KMeans(n_clusters=40, random_state=0)

model = Pipeline(
    steps=[
        ('preprocessor', preprocessor),
        ('model', cluster)
        ]
    )

train, test = train_test_split(data)
model.fit(train, [])
preds = pd.Series(model.predict(data), name="cluster")
train['train_set'] = "True"
results = pd.concat([saved, data, preds], axis=1)
results = pd.concat([results, train[["train_set"]]], axis=1)
results.to_csv("output.csv")

import visualize
