from .background_generator import BackgroundGenerator
from .foreground_generator import ForegroundGenerator
from ocr_data_generator.random_layout_generator import RandomLayoutGenerator
from .painter import Painter
from .drawer import Drawer

class SampleGenerator:
    def __init__(self, back_cfg, fore_cfg, paint_cfg, draw_cfg, cfg={}):
        self.background_generator = BackgroundGenerator(back_cfg)

        layout_generator = cfg.get('layout_generator', None)
        if layout_generator=='RandomLayoutGenerator':
            self.foreground_generator = RandomLayoutGenerator(fore_cfg)
        else:
            self.foreground_generator = ForegroundGenerator(fore_cfg)
        self.painter = Painter(paint_cfg)
        self.drawer = Drawer(draw_cfg)

    def generate_raw(self):
        background = self.background_generator.generate()
        foreground = self.foreground_generator.generate()
        background, foreground = self.painter.paint(background, foreground)
        return background, foreground

    def generate(self, show=False):
        background, foreground = self.generate_raw()
        img, boxes = self.drawer.draw(background, foreground, show=show)
        return img, boxes
    