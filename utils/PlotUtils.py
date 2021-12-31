import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

fontfamily = "Inconsolata"

sns.set_theme(style="whitegrid",
              context="paper",
              font_scale=1.25,
              rc={
                  "figure.figsize": (10.5, 4.5),
                  "figure.dpi": 250,
                  "grid.alpha": 0.1,
                  "grid.color": "#1b262c",
                  "grid.linewidth": 0.5,
                  "font.family": fontfamily
              })

_30k = ["#202f66", "#ff7048", "#7f68d0", "#f3d36e", "#d869ab", "#48ADA9", "#1b262c"]
sns.set_palette(_30k)

import warnings

warnings.filterwarnings('ignore')

from .Color import Color

DPI = 300


def plot_WCAG_contrast(color_df, suptitle="WCAG contrast"):

    contrast_matrix = []

    for i, base_color in color_df.iterrows():
        base_color = Color(base_color['color'])
        row = []
        for j, color in color_df.iterrows():
            color = Color(color['color'])
            row.append(base_color.contrast(color))
        contrast_matrix.append(np.array(row))

    contrast_matrix = np.array(contrast_matrix)
    tri_mask = np.triu(np.ones_like(contrast_matrix))

    fig, ax = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(10, 10),
        dpi=DPI,
        gridspec_kw={
            'height_ratios': [10, 1],
            'width_ratios': [1, 10]
        },
    )

    vmax = 21
    vmin = 1
    if (vmax - vmin) // 2 >= 20:
        n_colors = (vmax - vmin) // 2
    else:
        n_colors = (vmax - vmin) * 2

    # matrix content
    sns.heatmap(contrast_matrix,
                mask=tri_mask,
                square=False,
                annot=True,
                linewidths=0.5,
                vmin=vmin,
                vmax=vmax,
                fmt='.1f',
                cmap=sns.color_palette('light:b', n_colors=n_colors),
                cbar=False,
                ax=ax[0][1])
    # hide ticks
    ax[0][1].set_xticks([], [])
    ax[0][1].set_yticks([], [])

    # horizontal palette

    sns.heatmap([color_df.index], cmap=color_df['color'].tolist(), linewidths=0.5, cbar=False, ax=ax[1][1], square=True)
    ax[1][1].set_xticks(ticks=color_df.index + 0.5, labels=color_df['name'], rotation=-90)
    ax[1][1].set_yticks([], [])

    # vertical palette
    sns.heatmap(np.array([color_df.index]).transpose(),
                cmap=color_df['color'].tolist(),
                linewidths=0.5,
                cbar=False,
                ax=ax[0][0])
    ax[0][0].set_yticks(ticks=color_df.index + 0.5, labels=color_df['name'] + ' ' + color_df['color'], rotation=0)
    ax[0][0].set_xticks([], [])

    # hide unuse axis
    ax[1][0].set_visible(False)

    plt.suptitle(suptitle, fontsize=24, fontweight='bold', horizontalalignment="left", y=1, x=0.1)

    plt.tight_layout(pad=1.0)
    # plt.show()

    return fig


def plot_delta_E(color_df, suptitle="delta E"):

    deltaE_matrix = []

    for i, base_color in color_df.iterrows():
        base_color = Color(base_color['color'])
        row = []
        for j, color in color_df.iterrows():
            color = Color(color['color'])
            row.append(base_color.delta_E(color))
        deltaE_matrix.append(np.array(row))

    deltaE_matrix = np.array(deltaE_matrix)
    tri_mask = np.triu(np.ones_like(deltaE_matrix))

    fig, ax = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(10, 10),
        dpi=DPI,
        gridspec_kw={
            'height_ratios': [10, 1],
            'width_ratios': [1, 10]
        },
    )

    vmax = 100
    vmin = 1
    if (vmax - vmin) // 2 >= 20:
        n_colors = (vmax - vmin) // 2
    else:
        n_colors = (vmax - vmin) * 2
    # matrix content
    sns.heatmap(deltaE_matrix,
                mask=tri_mask,
                square=False,
                annot=True,
                linewidths=0.5,
                vmin=vmin,
                vmax=vmax,
                cmap=sns.color_palette('light:b', n_colors=n_colors),
                fmt='2.1f',
                cbar=False,
                ax=ax[0][1])
    # hide ticks
    ax[0][1].set_xticks([], [])
    ax[0][1].set_yticks([], [])

    # horizontal palette

    sns.heatmap([color_df.index], cmap=color_df['color'].tolist(), linewidths=0.5, cbar=False, ax=ax[1][1], square=True)
    ax[1][1].set_xticks(ticks=color_df.index + 0.5, labels=color_df['name'], rotation=-90)
    ax[1][1].set_yticks([], [])

    # vertical palette
    sns.heatmap(np.array([color_df.index]).transpose(),
                cmap=color_df['color'].tolist(),
                linewidths=0.5,
                cbar=False,
                ax=ax[0][0])
    ax[0][0].set_yticks(ticks=color_df.index + 0.5, labels=color_df['name'] + ' ' + color_df['color'], rotation=0)
    ax[0][0].set_xticks([], [])

    # hide unuse axis
    ax[1][0].set_visible(False)

    plt.suptitle(suptitle, fontsize=24, fontweight='bold', horizontalalignment="left", y=1, x=0.1)

    plt.tight_layout(pad=1.0)
    # plt.show()

    return fig


def plot_line_vs_bg(color_df, accent_type, linewidth=1):
    x = np.arange(-2, 2, 0.01)

    background_colors = color_df[color_df['type'] == 'background'].reset_index()
    accent_colors = color_df[color_df['type'] == accent_type]
    phi_diff = 90 / len(accent_colors)

    each_axes_h = 5
    num_rows = len(background_colors)
    fig, ax = plt.subplots(num_rows,
                           1,
                           figsize=((num_rows * each_axes_h) + each_axes_h,
                                    ((num_rows * each_axes_h) + each_axes_h) // 2.5),
                           dpi=DPI)

    for i, bg_color in background_colors.iterrows():
        bg_color = bg_color['color']
        ax[i].set_facecolor(bg_color)
        for j, color in accent_colors.iterrows():
            color = color['color']
            sns.lineplot(x=x, y=np.sin(np.pi * x + phi_diff * j), color=color, linewidth=linewidth, ax=ax[i])
        ax[i].set_xticks([], [])
        ax[i].set_title(f"BG: {bg_color}, linewidth: {linewidth}")
        # plt.show()
    return fig