import librosa
import numpy as np

def extract_melspectrogram(file_path, n_mels=128, duration=5):
    y, sr = librosa.load(file_path, duration=duration)
    mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mels_db = librosa.power_to_db(mels, ref=np.max)
    mels_db = librosa.util.fix_length(mels_db, size=128, axis=1)
    return mels_db
