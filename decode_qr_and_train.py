import cv2
from pyzbar.pyzbar import decode
import os
import pandas as pd
from utils import extract_features  # ✅ IMPORT here
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def decode_qr_images(folder_path, label):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            img = cv2.imread(os.path.join(folder_path, filename))
            decoded_objs = decode(img)
            for obj in decoded_objs:
                url = obj.data.decode('utf-8')
                data.append((filename, url, label))
    return data

benign_path = r"C:\Users\yasee\Downloads\1000 QR dataset\benign_qr_images_500"
malicious_path = r"C:\Users\yasee\Downloads\1000 QR dataset\malicious_qr_images_500"
# Decode QR images
benign_data = decode_qr_images(benign_path, 0)
malicious_data = decode_qr_images(malicious_path, 1)

# Create dataframe
df = pd.DataFrame(benign_data + malicious_data, columns=["image", "url", "label"])
df.to_csv("decoded_qr_data.csv", index=False)

# Feature extraction
feature_rows = df["url"].apply(extract_features).apply(pd.Series)
df_features = pd.concat([df, feature_rows], axis=1)
df_features.to_csv("qr_url_features.csv", index=False)

# Model training
X = df_features.drop(columns=["image", "url", "label"])
y = df_features["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\nClassification Report:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "model.pkl")
print("\n✅ New model saved as model.pkl!")
