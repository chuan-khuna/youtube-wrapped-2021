import numpy as np
import pandas as pd
from PIL import Image
from .Color import Color


def rgb_to_hex(row):
    r = row['r']
    g = row['g']
    b = row['b']
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_palette(img, max_width=256, deltaE_threshold=20):

    img = img.convert('RGB')
    img_size = np.array(img.size)

    if np.max(img_size) > max_width:
        img_size = img_size // (np.max(img_size) / max_width)
        img_size = np.array(img_size, dtype=np.int)
        img = img.resize((img_size[0], img_size[1]))

    img_arr = np.array(img)
    img_arr = img_arr.reshape((np.product(img_arr.shape[:2]), 3))

    rgb, counts = np.unique(img_arr, axis=0, return_counts=True)

    # use pandas just for pairing  RGBhex and frequency
    df = pd.DataFrame(data={'r': rgb[:, 0], 'g': rgb[:, 1], 'b': rgb[:, 2], 'freq': counts})
    df['color'] = df[['r', 'g', 'b']].apply(rgb_to_hex, axis=1)
    df = df.drop(columns=['r', 'g', 'b'])
    df = df.sort_values(by=['freq'], ascending=False)

    rgb = np.array(df['color'])
    counts = np.array(df['freq'])

    num_colors = len(df)

    for i in range(num_colors):
        c1 = Color(rgb[i])

        if counts[i] > 0:
            for j in range((i + 1), num_colors):
                c2 = Color(rgb[j])
                if c1.delta_E(c2) < deltaE_threshold:
                    counts[i] += counts[j]
                    counts[j] = 0


    df = pd.DataFrame({'color': rgb[counts > 0], 'freq': counts[counts > 0]})
    # df = pd.DataFrame({'color': [rgb_to_hex(i) for i in rgb], 'freq': counts})
    df['ratio'] = df['freq'] / df['freq'].sum()

    return df.sort_values(by=['ratio'], ascending=False, ignore_index=True)