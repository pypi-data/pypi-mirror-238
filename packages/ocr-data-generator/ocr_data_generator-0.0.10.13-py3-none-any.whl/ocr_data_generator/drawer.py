from PIL import Image, ImageDraw

from .font_generator import FontGenerator


def draw_rectangle_transparent(img, pt1, pt2, color, outline, width, show=False):
    assert img.mode == 'RGBA'

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle([*pt1, *pt2], color, outline, width)
    img = Image.alpha_composite(img, overlay)
    return img


def draw_circle_transparent(img, pt, r, color, outline, width, show=False):
    assert img.mode == 'RGBA'

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pt1 = (pt[0] - r, pt[1] - r)
    pt2 = (pt[0] + r, pt[1] + r)
    draw.ellipse([*pt1, *pt2], color, outline, width)

    img = Image.alpha_composite(img, overlay)

    return img


def draw_polygon_transparent(img, pts, color, outline, width):
    assert img.mode == 'RGBA'

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pts = [tuple(pt) for pt in pts]
    draw.polygon(pts, color, outline)

    img = Image.alpha_composite(img, overlay)

    return img


def draw_line_transparent(img, pts, color, width, show=False):
    assert img.mode == 'RGBA'

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pts = [tuple(pt) for pt in pts]
    draw.line(pts, color, width)

    img = Image.alpha_composite(img, overlay)

    return img


def draw_background(img, backgound_cfg):
    for item in backgound_cfg:
        if item['shape'] == 'rectangle':
            img = draw_rectangle_transparent(img, item['pt1'], item['pt2'], item['fill_color'], item['outline_color'],
                                             item['width'])
        elif item['shape'] == 'circle':
            img = draw_circle_transparent(img, item['pt'], item['r'], item['fill_color'], item['outline_color'],
                                          item['width'])
        elif item['shape'] == 'polygon':
            img = draw_polygon_transparent(img, item['pts'], item['fill_color'], item['outline_color'], item['width'])
        elif item['shape'] == 'line':
            img = draw_line_transparent(img, [item['pt1'], item['pt2']], item['fill_color'], item['width'])
    return img


def draw_text_transparent(img, text, pos, color, font, stroke_width, show=False):
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(txt)

    draw.text(pos, text, fill=color, font=font, stroke_width=stroke_width)

    right, bottom = font.getsize(text)
    ox, oy = font.getoffset(text)
    x = pos[0] + ox
    y = pos[1] + oy

    box = (x, y, pos[0] + right, pos[1] + bottom)

    if show:
        draw.rectangle(box, None, "#f00", width=4)

    img = Image.alpha_composite(img, txt)

    return img, box


class Drawer:
    def __init__(self, cfg):
        self.w = cfg['img_w']
        self.h = cfg['img_h']
        self.font_generator = FontGenerator(font_list_file=cfg['font_list_file'])
        pass

    def draw(self, background, foreground, show=False):
        img = self.draw_background(background)
        img, boxes = self.draw_foreground(img, foreground, show=show)
        return img, boxes

    def draw_background(self, background):
        w, h = self.w, self.h
        img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        img = draw_background(img, background)
        return img

    def draw_foreground(self, img, foreground, show=False):
        boxes = []
        for item in foreground:
            try:
                font = self.font_generator.get_font(item['font_name'], item['font_size'])
                img, box = draw_text_transparent(
                    img, item['words'],
                    (item['x'], item['y']),
                    item['fill_color'], font, item['stroke_width'], show=show)
                boxes.append(box)
            except Exception as e:
                print(item)
                raise e
        return img, boxes