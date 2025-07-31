# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# import os
#
# model = tf.keras.models.load_model("model/bird_model.h5")
# labels = np.load("model/class_labels.npy")
#
# def preprocess_image(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img) / 255.0
#     return np.expand_dims(img_array, axis=0)
#
# def predict_bird_from_image(img_path):
#     img_array = preprocess_image(img_path)
#     predictions = model.predict(img_array)
#     return labels[np.argmax(predictions)]


import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# Load model and labels
model = tf.keras.models.load_model("model/bird_model.h5")
labels = np.load("model/class_labels.npy")


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


def predict_bird_from_image(img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)[0]  # Shape: (num_classes,)

    # Get top 5 indices and sort by confidence descending
    top_indices = predictions.argsort()[-5:][::-1]
    top_5 = [(labels[i], float(predictions[i] * 100)) for i in top_indices]

    return top_5
