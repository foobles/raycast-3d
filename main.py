import sys
import math
import pygame as pg
from world import World
from scene import Scene
from camera import Camera 

class Texture:
    def __init__(self, path, transparent=False):
        image = pg.image.load(path)
        if not transparent:
            self.surface = image.convert()
        else:
            self.surface = image.convert_alpha()
        self.transparent = transparent


class Sprite:
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y


def world_from_surface(surface, tex_colors, spr_colors):
    conv_tex_colors = [surface.map_rgb(c) for c in tex_colors]
    conv_spr_colors = [surface.map_rgb(c) for c in spr_colors]
    arr = pg.PixelArray(surface)
    world_ret = [] 
    cur = []  
    spr_ret = []
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            cur_color = arr[x, y]
            try:
                cur.append(conv_tex_colors.index(cur_color)) 
            except ValueError: 
                cur.append(0) 
                spr_ret.append(Sprite(conv_spr_colors.index(cur_color), x + 0.5, y + 0.5))
        world_ret.append(cur) 
        cur = [] 
    arr.close() 
    return World(world_ret), spr_ret


WORLD_MAP, SPRITE_MAP = world_from_surface(
    pg.image.load("assets/map.bmp"), 
    tex_colors=[
        (255, 255, 255),
        (0, 0, 0),
        (255, 0, 0),
        (255, 0, 255)
    ],
    spr_colors=[
        (0, 255, 0),
        (0, 255, 255)
    ])


def handle_input(scene, dt):
    turn = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    turn += pg.key.get_pressed()[pg.K_RIGHT]
    turn -= pg.key.get_pressed()[pg.K_LEFT]
    scene.camera.rotate(dt * turn * 180 * math.pi / 180000)

    if pg.key.get_pressed()[pg.K_UP]:
        speed = 4
        dx, dy = scene.camera.dir
        px, py = scene.camera.pos
        buffer = 0.2
        dx_b = buffer if dx > 0 else -buffer
        dy_b = buffer if dy > 0 else -buffer

        x_mov = dt * dx * speed / 1000
        y_mov = dt * dy * speed / 1000

        if not scene.world.has_tile_at(int(px + x_mov + dx_b), int(py)):
            px += x_mov
        if not scene.world.has_tile_at(int(px), int(py + y_mov + dy_b)):
            py += y_mov

        scene.camera.pos = (px, py)


def main():
    pg.init()
    size = 910, 600
    screen = pg.display.set_mode(size)

    textures = [
        Texture("assets/wood.bmp"),
        Texture("assets/brick.bmp"),
        Texture("assets/glass.bmp", transparent=True),
        Texture("assets/world.bmp")
    ]

    sprites = [
        pg.image.load("assets/mado.bmp").convert_alpha(),
        pg.image.load("assets/uboa.png").convert_alpha()
    ]

    scene = Scene(
        world=WORLD_MAP,
        sprites=SPRITE_MAP,
        camera=Camera((1.5, 1.5), (0, -1), 60 * math.pi / 180))

    fps = 60
    ms_per_frame = 1000 // fps

    prev_ticks = 0
    cur_ticks = pg.time.get_ticks()

    surface = pg.Surface((size[0]//8, size[1]//8))

    while True:
        handle_input(scene, cur_ticks - prev_ticks)
        surface.fill([0, 0, 0])
        z_buf = scene.render_walls(surface, textures)
        scene.render_sprites(surface, z_buf, sprites)
        pg.transform.scale(surface, size, screen)
        pg.display.flip()
        pg.time.delay(max(0, ms_per_frame - (cur_ticks - prev_ticks)))
        prev_ticks = cur_ticks
        cur_ticks = pg.time.get_ticks()


if __name__ == "__main__":
    main()
