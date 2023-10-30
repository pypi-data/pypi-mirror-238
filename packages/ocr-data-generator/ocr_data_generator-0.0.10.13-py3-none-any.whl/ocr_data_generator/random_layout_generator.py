import numpy as np
import random

randint = np.random.randint

from .font_generator import FontGenerator
from .word_generator import WordGenerator
from .word_generator import MongolianWordGenerator


def get_text_size(text, font):
    right, bottom = font.getsize(text)
    offsetx, offsety = font.getoffset(text)
    return right, bottom, offsetx, offsety

class RandomLayoutGenerator:
    def __init__(self, cfg):
        self.img_w = cfg['img_w']
        self.pad_x_min = cfg['pad_x_min']
        self.pad_x_max = cfg['pad_x_max']
        self.pad_y_min = cfg['pad_y_min']
        self.pad_y_max = cfg['pad_y_max']
        self.img_h = cfg['img_h']
        self.min_block_len = cfg['min_block_len']
        self.max_block_len = cfg['max_block_len']
        self.font_generator = FontGenerator(font_list_file=cfg['font_list_file'])
        word_generator = cfg['word_generator']
        print(word_generator)
        if word_generator=='MongolianWordGenerator':
            self.word_generator = MongolianWordGenerator()
        else:
            self.word_generator = WordGenerator(word_list_file=cfg['word_list_file'])

    def generate_line(self, yoffset):
        pad_x1 = randint(self.pad_x_min, self.pad_x_max)
        pad_x2 = randint(self.pad_x_min, self.pad_x_max)
        blocks = []
        line_height = 0
        x = pad_x1
        while x < self.img_w-pad_x2:
            block_len = random.randint(self.min_block_len,self.max_block_len)
            words = self.word_generator.generate(block_len)

            font, font_name, font_size = self.font_generator.get_random_font()
            space_w = font.getsize(' ')[0]

            block = ''.join(words)
            w, h, offsetx, offsety = get_text_size(block, font)

            r = h*random.uniform(0,0.1)
            if x + w <= self.img_w-pad_x2:
                row = {
                    'words':block,
                    'x':x,
                    'y':yoffset + r,
                    'w':w,
                    'h':h,
                    'stroke_width':randint(0,2),
                    'font_name':font_name,
                    'font_size':font_size
                }
                blocks.append(row)
                x += w+space_w*random.randint(1,5)
                line_height = max(line_height, h+r)
            else:
                break
        return blocks, line_height
    
    def generate(self):
        pad_y1 = randint(self.pad_y_min, self.pad_y_max)
        pad_y2 = randint(self.pad_y_min, self.pad_y_max)
        layout = []
        y = pad_y1
        while True:
            line, line_height = self.generate_line(y)

            y += line_height
            if y >= self.img_h -pad_y2:
                break
            else:
                layout +=line
                y += line_height * random.uniform(0.1,1)


        return layout
    