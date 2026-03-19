import pandas as pd
import requests
import os
from tqdm import tqdm

CSV_PATH = r"unsplash-research-dataset-lite-latest\photos.csv000"
SAVE_DIR = "unsplash"

START_ROW = 0 # Edit here to download which rows you want in the csv000
END_ROW = 100 # Edit here to download which rows you want in the csv000

os.makedirs(SAVE_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH, sep='\t')

df_subset = df.iloc[START_ROW:END_ROW] if END_ROW is not None else df.iloc[START_ROW:]

count = 0
for idx, row in tqdm(df_subset.iterrows(), total=len(df_subset), desc="Downloading images"):
    url = row['photo_image_url']
    photo_id = row['photo_id']

    if not isinstance(url, str) or url.strip() == "":
        continue

    file_path = os.path.join(SAVE_DIR, f"{photo_id}.jpg")

    if os.path.exists(file_path):
        continue

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(resp.content)
            count += 1
        else:
            print(f"Failed {photo_id}: Status {resp.status_code}")
    except Exception as e:
        print(f"Failed {photo_id}: {e}")

print(f"Download completed. Total new images downloaded: {count}")