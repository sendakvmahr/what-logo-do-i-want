import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from tensorflow.keras.preprocessing import image_dataset_from_directory
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
use_full_data = True
images = image_dataset_from_directory(
    "../data_building/{}/".format("images_processed" if use_full_data else "test_images_processed"),
    labels="inferred",
    label_mode="categorical",
    image_size=[128, 128],
    interpolation='nearest',
    color_mode='grayscale'
)

convnet = keras.Sequential([
    layers.Conv2D(
        filters=32,
        kernel_size=5,
        activation="relu",
        padding="same",
        input_shape=(128, 128, 1) # very much want only grayscale, colors have been looked at plenty
    ),
    layers.MaxPool2D(),
    layers.Conv2D(
        filters=64,
        kernel_size=3,
        activation="relu",
        padding="same"
    ),
    layers.MaxPool2D(),
    layers.Conv2D(
        filters=128,
        kernel_size=3,
        activation="relu",
        padding="same"
    ),
    layers.MaxPool2D(),
    layers.Conv2D(
        filters=256,
        kernel_size=3,
        activation="relu",
        padding="same"
    ),
    layers.MaxPool2D(),
    layers.Conv2D(
        filters=512,
        kernel_size=3,
        activation="relu",
        padding="same"
    ),
    layers.MaxPool2D(),
    layers.Flatten()
])


convnet.compile()
convnet_preds = convnet.predict(images)

convnet_preds = pd.DataFrame(convnet_preds)

o_data = pd.read_csv("../data_building/output.csv" if use_full_data else "../data_building/output_test.csv")
data = pd.concat([o_data, convnet_preds], axis=1)
data = convnet_preds

cluster = KMeans(n_clusters=40, random_state=0)
cluster = Pipeline(
    steps=[
        #('preprocessor', preprocessor),
        ('model', cluster)
    ]
)

#train, test = train_test_split(data)
cluster.fit(data, [])
preds2 = pd.Series(cluster.predict(data), name="cluster")
#train['train_set'] = "True"
#results = pd.concat([saved, data, preds2], axis=1)
#results = pd.concat([results, train[["train_set"]]], axis=1)
results =  pd.concat([o_data, preds2], axis=1)
results.to_csv("output_shape.csv")

"""
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
"""
