import numpy as np

randint = np.random.randint

from .font_generator import FontGenerator
from .word_generator import WordGenerator


def get_text_size(text, font):
    right, bottom = font.getsize(text)
    offsetx, offsety = font.getoffset(text)
    return right, bottom, offsetx, offsety


class ForegroundGenerator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.font_generator = FontGenerator(font_list_file=cfg['font_list_file'])
        self.word_generator = WordGenerator(word_list_file=cfg['word_list_file'])

    def get_text_width_le(self, width, font):
        width_ = 0
        words = ''
        while True:
            word = self.word_generator.generate()
            right, bottom, offsetx, offsety = get_text_size(word, font)
            width_ += right
            if width_ <= width:
                words += word
            else:
                break

        right, bottom, offsetx, offsety = get_text_size(words, font)
        return words, right, bottom, offsetx, offsety

    def generate(self):
        cfg = self.cfg

        pad_y1 = randint(cfg['pad_y_min'], cfg['pad_x_max'])
        pad_y2 = randint(cfg['pad_y_min'], cfg['pad_x_max'])

        boxes = []
        texts = []
        text_cfg = []
        line_i = 0
        y = pad_y1
        while True:
            font, font_name, font_size = self.font_generator.get_random_font()
            space_w = font.getsize(' ')[0]

            pad_x1 = randint(cfg['pad_x_min'], cfg['pad_x_max'])
            pad_x2 = randint(cfg['pad_x_min'], cfg['pad_x_max'])

            words, right, bottom, offsetx, offsety = self.get_text_width_le(cfg['img_w'] - pad_x1 - pad_x2, font)
            if words == '':
                continue

            if y + bottom + pad_y2 > cfg['img_h']:
                break
            else:
                line_space = int(bottom * np.random.uniform(0.1, 1))
                line_i += 1
                text_cfg.append({
                    'stroke_width': randint(2),
                    'font_name': font_name,
                    'font_size': font_size,
                    'words': words,
                    'right': right,
                    'bottom': bottom,
                    'offsetx': offsety,
                    'x': pad_x1,
                    'y': y,
                })
                y += (bottom + line_space)

        return text_cfg
