import numpy as np
randint = np.random.randint

class BackgroundGenerator:
    def __init__(self, cfg):
        self.w = cfg['img_w']
        self.h = cfg['img_h']

    def gen_rectangle(self):
        w, h = self.w, self.h
        x1, x2 = sorted(randint(w, size=2))
        y1, y2 = sorted(randint(h, size=2))
        pt1 = x1, y1
        pt2 = x2, y2

        width = randint(0, 20)
        config = {
            'shape':'rectangle',
            'width': width,
            'pt1': pt1,
            'pt2': pt2,
        }
        return config
    
    def gen_circle(self):
        w, h = self.w, self.h
        r = randint(1, max(w,h))
        pt = randint(w), randint(h)
        width = randint(0, 20)
        config = {
            'shape':'circle',
            'width': width,
            'pt': pt,
            'r': r,
        }
        return config
    
    def gen_line(self):
        w, h = self.w, self.h
        pt1 = randint(w), randint(h)
        pt2 = randint(w), randint(h)
        width = randint(1, 20)
        config = {
            'shape':'line',
            'width': width,
            'pt1': pt1,
            'pt2': pt2,
        }
        return config
    
    def gen_polygon(self):
        w, h = self.w, self.h
        pt = np.array([randint(w), randint(h)])
        n = randint(2, 100) # number of polygon vertexs
        r = randint(1, max(w,h)) # max radious of polygon
        pts = pt + randint(r, size=(n, 2))
        pts = pts.astype(np.int32).reshape([-1, 2])            
        width = randint(1, 20)
        config = {
            'shape':'polygon',
            'width': width,
            'pts': pts,
        }
        return config
        
    def generate(self):
        w, h = self.w, self.h

        background = []
        n = randint(10, 50)
        for i in range(n):
            row = self.gen_rectangle()
            background.append(row)

            row = self.gen_circle()
            background.append(row)

            row = self.gen_line()
            background.append(row)

            for _ in range(randint(1, 10)):
                row = self.gen_polygon()
                background.append(row)

            for _ in range(randint(1, 10)):
                row = self.gen_line()
                background.append(row)

        return background