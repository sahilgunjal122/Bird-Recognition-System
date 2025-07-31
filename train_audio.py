# import os
# import numpy as np
# import tensorflow as tf
# from sklearn.model_selection import train_test_split
# from utils.melspecto import extract_melspectrogram
#
# dataset_path = "dataset/audio_data"
# labels = os.listdir(dataset_path)
#
# X, y = [], []
# for i, label in enumerate(labels):
#     folder = os.path.join(dataset_path, label)
#     for file in os.listdir(folder):
#         if file.endswith(".wav"):
#             path = os.path.join(folder, file)
#             try:
#                 mels = extract_melspectrogram(path)
#                 X.append(mels)
#                 y.append(i)
#             except:
#                 continue
#
# X = np.array(X)[..., np.newaxis]
# y = np.array(y)
# np.save("model_audio/labels_audio.npy", np.array(labels))
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#
# model = tf.keras.Sequential([
#     tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=X.shape[1:]),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(len(labels), activation='softmax')
# ])
#
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)
# model.save("model_audio/model_audio.h5")



import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils.melspecto import extract_melspectrogram

dataset_path = "dataset/audio_data"

# ✅ Only include directories (skip .DS_Store and files)
labels = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

X, y = [], []
for i, label in enumerate(labels):
    folder = os.path.join(dataset_path, label)
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            path = os.path.join(folder, file)
            try:
                mels = extract_melspectrogram(path)
                X.append(mels)
                y.append(i)
            except Exception as e:
                print(f"❌ Skipping {path} due to error: {e}")

X = np.array(X)[..., np.newaxis]  # Add channel dimension
y = np.array(y)

# Save label names for prediction use
np.save("model_audio/labels_audio.npy", np.array(labels))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=X.shape[1:]),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(labels), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)

# Save trained model
model.save("model_audio/model_audio.h5")
print("✅ Audio model training complete and saved to model_audio/model_audio.h5")
