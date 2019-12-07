import math 

def _rotate_vec(vec, rads):
    x, y = vec 
    return (
        x * math.cos(rads) - y * math.sin(rads),
        x * math.sin(rads) + y * math.cos(rads))

class Camera:
    def __init__(self, pos, dir, fov):
        self.pos = pos
        self.dir = dir 
        dir_x, dir_y = dir;
        dir_len =  math.sqrt(dir_x*dir_x + dir_y*dir_y)
        screen_rat = math.tan(fov / 2) 
        self.screen = (
            -dir_y * screen_rat, 
            dir_x * screen_rat)

    def rotate(self, rads):
        self.dir = _rotate_vec(self.dir, rads)
        self.screen = _rotate_vec(self.screen, rads)

    def rays(self, width):
        dir_x, dir_y = self.dir 
        screen_x, screen_y = self.screen  
        for x in range(width):
            cur = (2 * x / width) - 1 
            yield x, (
                dir_x + screen_x * cur,
                dir_y + screen_y * cur)