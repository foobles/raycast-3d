import sys
import math
import pygame as pg
from world import World
from scene import Scene
from camera import Camera


WORLD_MAP = World([
    [1, 1, 1, 1, 1, 1, 0, 0],
    [2, 0, 0, 1, 0, 1, 0, 0],
    [2, 0, 0, 0, 0, 1, 1, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
])


def load_textures(*textures):
    return list(map(lambda x: pg.image.load(x).convert(), textures))


def handle_input(scene):
    turn = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    turn += pg.key.get_pressed()[pg.K_RIGHT]
    turn -= pg.key.get_pressed()[pg.K_LEFT]
    scene.camera.rotate(turn * 5 * math.pi / 180)

    if pg.key.get_pressed()[pg.K_UP]:
        dx, dy = scene.camera.dir
        px, py = scene.camera.pos

        scene.camera.pos = (px + dx * 0.2, py + dy * 0.2)
        # if not scene.world.has_tile_at(int(px + dx * 0.2), int(py)):
        #     scene.camera.pos[0] += dx * 0.2
        #     px += dx * 0.2
        # if not scene.world.has_tile_at(int(px), int(py + dy * 0.2)):
        #     scene.camera.pos[1] += dy * 0.2
        #     py += dy * 0.2


def main():
    pg.init()
    size = 600, 600
    screen = pg.display.set_mode(size)

    textures = load_textures(
        "assets/wood.bmp",
        "assets/brick.bmp")

    scene = Scene(WORLD_MAP, Camera((4, 4), (0, -1), 60 * math.pi / 180))

    fps = 30
    prev_ticks = pg.time.get_ticks()

    while True:
        handle_input(scene)
        screen.fill([0, 0, 0])
        scene.render(screen, textures)
        pg.display.flip()
        cur_time = pg.time.get_ticks()
        pg.time.delay(max(0, fps//1000 - (cur_time - prev_ticks)))
        prev_ticks = cur_time


if __name__ == "__main__":
    main()
