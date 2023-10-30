import os
import numpy as np

randint = np.random.randint
from PIL import ImageFont


class FontGenerator:
    def __init__(self, font_list_file):
        self.min_font_size = 20
        self.max_font_size = 50
        with open(font_list_file, encoding='utf8') as f:
            font_path_list = f.read().strip().split()

        self.font_path_list = font_path_list
        self.font_name_to_path = {os.path.basename(path): path for path in font_path_list}
        print('fonts', len(self.font_path_list))
        self.font_cache = {}

    def get_random_font(self):
        font_path = np.random.choice(self.font_path_list)
        font_name = os.path.basename(font_path)
        font_size = randint(self.min_font_size, self.max_font_size)
        font = self.get_font(font_name, font_size)

        return font, font_name, font_size

    def get_font(self, font_name, font_size):
        font_name = os.path.basename(font_name)
        key = f'{font_name}-{font_size}'
        if key in self.font_cache:
            return self.font_cache[key]
        else:
            font_path = self.font_name_to_path[font_name]
            try:
                font = ImageFont.truetype(font_path, size=font_size, index=0, encoding="utf-8")
            except OSError as e:
                print(f"file not found: {font_path}")
                raise e

            self.font_cache[key] = font
        return font
