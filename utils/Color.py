import numpy as np
import skimage


class Color:

    def __init__(self, color_hex):
        assert color_hex[0] == '#', 'color hex should be #RRGGBB (start with #)'
        assert len(color_hex) == 7, 'color hex should be #RRGGBB (length = 7)'
        # RGB hex: #RRGGBB
        self.hex = color_hex

        # calculate another space
        self.to_RGB_decimal()
        self.to_sRGB()
        self.to_luminance()
        self.to_HSB()

    def to_RGB_decimal(self):
        self.RGB = np.array([
            np.int(f"0x{self.hex[1:3]}", base=16),
            np.int(f"0x{self.hex[3:5]}", base=16),
            np.int(f"0x{self.hex[5:]}", base=16)
        ],
                            dtype=np.int)

    def to_sRGB(self):
        self.sRGB = self.RGB / 255.0

    def to_luminance(self):
        l_rgb = []
        for color_sRGB in self.sRGB:
            if color_sRGB <= 0.03928:
                l_rgb.append(color_sRGB / 12.92)
            else:
                l_rgb.append(((color_sRGB + 0.055) / 1.055)**2.4)
        luminance_const = np.array([0.2126, 0.7152, 0.0722])
        self.relative_luminance = np.sum(luminance_const * np.array(l_rgb))
    
    def to_HSB(self):
        # HSB: hue(0-360 degree), saturation(0-100 %), brightness(0-100 %)
        # HSV: hue, saturation, value
        self.HSV = np.round(skimage.color.rgb2hsv(self.sRGB), 4)
        self.HSB = self.HSV

        self.HSV_decimal = np.round(self.HSV * np.array([360, 100, 100]))
        self.HSB_decimal = self.HSV_decimal

    def contrast(self, color_obj):
        assert type(color_obj) == Color

        l1 = self.relative_luminance
        l2 = color_obj.relative_luminance
        if l2 > l1:
            l1, l2 = l2, l1

        return np.round((l1 + 0.05) / (l2 + 0.05), 3)

    def rgb_euclidean_distance(self, color_obj):
        assert type(color_obj) == Color

        return np.round(np.linalg.norm(self.RGB - color_obj.RGB), 3)

    def delta_E(self, color_obj):
        # https://en.wikipedia.org/wiki/Color_difference
        # delta E

        assert type(color_obj) == Color
        lab1 = skimage.color.rgb2lab(self.sRGB)
        lab2 = skimage.color.rgb2lab(color_obj.sRGB)

        return np.round(skimage.color.deltaE_ciede2000(lab1, lab2), 3)