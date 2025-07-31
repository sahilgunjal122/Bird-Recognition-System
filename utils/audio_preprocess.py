# import numpy as np
# import tensorflow as tf
# from utils.melspecto import extract_melspectrogram
#
# model = tf.keras.models.load_model("model_audio/model_audio.h5")
# labels = np.load("model_audio/labels_audio.npy")
#
# def preprocess_audio(file_path):
#     mels = extract_melspectrogram(file_path)
#     mels = mels[..., np.newaxis]  # Add channel dimension
#     return mels[np.newaxis, ...]
#
# def predict_bird_from_audio(file_path):
#     mels_array = preprocess_audio(file_path)
#     prediction = model.predict(mels_array)
#     return labels[np.argmax(prediction)]


import numpy as np
import tensorflow as tf
from utils.melspecto import extract_melspectrogram

# Load model and labels
model = tf.keras.models.load_model("model_audio/model_audio.h5")
labels = np.load("model_audio/labels_audio.npy")


def preprocess_audio(file_path):
    mels = extract_melspectrogram(file_path)
    mels = mels[..., np.newaxis]  # Add channel dimension for CNN
    return mels[np.newaxis, ...]


def predict_bird_from_audio(file_path):
    mels_array = preprocess_audio(file_path)
    predictions = model.predict(mels_array)[0]  # Shape: (num_classes,)

    top_indices = predictions.argsort()[-5:][::-1]
    top_5 = [(labels[i], float(predictions[i] * 100)) for i in top_indices]

    return top_5
