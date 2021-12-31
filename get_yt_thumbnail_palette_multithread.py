from PIL import Image
import requests
from utils.ExtractColor import extract_palette

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from multiprocessing import Pool


def get_youtube_img_url(vid):
    return f"https://i.ytimg.com/vi/{vid}/sddefault.jpg"
    # return f"https://img.youtube.com/vi/{vid}/sddefault.jpg"


def get_image_palette(vid):
    try:
        url = get_youtube_img_url(vid)
        img = Image.open(requests.get(url, stream=True).raw)
        palette = extract_palette(img, max_width=128, deltaE_threshold=10)
        palette['vid'] = vid
        print(vid)
        return palette
    except:
        pass


if __name__ == "__main__":

    df = pd.read_json("./Takeout/YouTube and YouTube Music/history/watch-history.json")
    df['time'] = pd.to_datetime(df['time'])
    df = df[df['time'] >= '2021-01-01']
    df = df[~df['titleUrl'].isna()]
    df['vid'] = df['titleUrl'].apply(lambda x: x.split('=')[1])
    unique_vid = np.array(df['vid'].drop_duplicates())
    num_vid = len(unique_vid)

    with Pool(5) as p:
        palette_array = p.map(get_image_palette, unique_vid)

    palette_df = pd.concat(palette_array)

    palette_df.to_csv("./yt_thumbnail_palettes.csv", index=False)