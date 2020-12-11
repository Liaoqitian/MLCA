import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras.optimizers import SGD
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import numpy as np 
import matplotlib.pyplot as plt 
import argparse
import os
import cv2 
import random

import sys
from PIL import Image
import pickle
import math

DATADIR = "/Users/liaoqt/documents/CS294/data"
CATEGORIES = ["Boring", "Interesting"]
training_data = []
IMG_SIZE = 1185

## Stitch the images together 
## 0 1 2 
## 3 4 5
## 6 7 8

def stitch_images(file_path, file_name):
    images = [Image.open(image) for image in [file_path + "/" + file_name + str(x) + ".png" for x in range(100, 109)]]
    widths, heights = zip(*(i.size for i in images))
    total_width = int(sum(widths) / 3)
    total_height = int(sum(heights) / 3)
    new_image = Image.new("RGB", (total_width, total_height))
    for index in range(0, 9):
        image = images[index]
        new_image.paste(image, ((index % 3) * image.size[0], math.floor(index / 3) * image.size[1]))

    IMAGE_DIR = os.path.join(file_path, "combined/") + file_name + "combined.png"
    new_image.save(IMAGE_DIR)
    return IMAGE_DIR


def create_training_data():
    for category in CATEGORIES: 
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for image in sorted(os.listdir(path)): 
            if "100" not in image: ## Find the starting frame
                continue
            IMAGE_DIR = stitch_images(path, image[0:-7])
            try: 
                img_array = cv2.imread(IMAGE_DIR, cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e: 
                pass 

create_training_data()
random.shuffle(training_data)
X, y = [], []
for features, label in training_data: 
    X.append(features)
    y.append(label)
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
y = np.array(y)

## Data Training 
### Data Normalization
X = X / 255.0 
model = keras.Sequential()
model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(X, y, batch_size=32, epochs=3) 
# batch_size should be tuned


