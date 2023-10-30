import numpy as np
randint = np.random.randint

class Painter:
    def __init__(self, cfg):
        self.min_fore_rgb = cfg['min_fore_rgb']
        self.max_fore_rgb = cfg['max_fore_rgb']
        self.min_fore_alpha = cfg['min_fore_alpha']
        self.max_fore_alpha = cfg['max_fore_alpha']

        self.min_rgb_gap = cfg['min_rgb_gap']
        self.max_rgb_gap = cfg['max_rgb_gap']
        self.min_back_alpha = cfg['min_back_alpha']
        self.max_back_alpha = cfg['max_back_alpha']

        self.reset()

    def reset(self):
        fore_color = randint(self.min_fore_rgb,self.max_fore_rgb, size=3)
        alpha = randint(self.min_fore_alpha, self.max_fore_alpha)
        self.fore_color = tuple(fore_color) + (alpha, )

    def get_fore_color(self):
        return self.fore_color

    def get_back_color(self):
        fore_color = np.array(self.fore_color[:3])
        back_color = np.mod(fore_color + randint(self.min_rgb_gap, self.max_rgb_gap, size=3), 255)
        alpha = randint(self.min_back_alpha,self.max_back_alpha)
        back_color = tuple([int(c) for c in back_color])+(alpha,)
        return back_color
    
    def paint(self, geometry, layout):
        self.reset()
        for item in geometry:
            item['fill_color'] = self.get_back_color()
            item['outline_color'] = self.get_back_color()

        for item in layout:
            item['fill_color'] = self.get_fore_color()
            item['outline_color'] = self.get_fore_color()
        return geometry, layout