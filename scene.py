from collections import namedtuple
import math
import pygame as pg


RayHitInfo = namedtuple("RayHitInfo", [
    "hit",
    "distance",
    "horizontal",
    "wall_x_rat"])


def _get_ray_hit_info(pos, ray, world):
    pos_x, pos_y = pos
    ray_x, ray_y = ray
    tile_x, tile_y = int(pos_x), int(pos_y)
    x_tile_dist = math.sqrt(1 + (ray_y * ray_y) / (
        (ray_x * ray_x)
        if ray_x != 0
        else 1))
    y_tile_dist = math.sqrt(1 + (ray_x * ray_x) / (
        (ray_y * ray_y)
        if ray_y != 0
        else 1))

    x_step = 1 if ray_x > 0 else -1
    x_dist_moved = x_tile_dist * (
        (1 + tile_x - pos_x)
        if ray_x > 0
        else (pos_x - tile_x))

    y_step = 1 if ray_y > 0 else -1
    y_dist_moved = y_tile_dist * (
        (1 + tile_y - pos_y)
        if ray_y > 0
        else (pos_y - tile_y))

    hit = 0
    while hit == 0:
        if x_dist_moved < y_dist_moved:
            x_dist_moved += x_tile_dist
            tile_x += x_step
            horizontal = False
        else:
            y_dist_moved += y_tile_dist
            tile_y += y_step
            horizontal = True
        hit = world[tile_x, tile_y]
    if horizontal:
        distance = (tile_y - pos_y + (1-y_step) / 2) / ray_y
        wall_x_rat = abs(pos_x + ray_x * distance) % 1
    else:
        distance = (tile_x - pos_x + (1-x_step) / 2) / ray_x
        wall_x_rat = abs(pos_y + ray_y * distance) % 1

    return RayHitInfo(hit, distance, horizontal, wall_x_rat)


def _get_column(texture, x_rat, height):
    vertical = texture.subsurface(pg.Rect(
        int(texture.get_width() * x_rat),
        0,
        1,
        texture.get_height()))
    return pg.transform.scale(vertical, (1, height))


class Scene:
    def __init__(self, world, camera):
        self.world = world
        self.camera = camera

    def render(self, surface, textures):
        dark = pg.Surface((1, surface.get_height()))
        dark.fill((0, 0, 0))
        dark.set_alpha(128)

        for x, ray in self.camera.rays(surface.get_width()):
            ray_info = _get_ray_hit_info(self.camera.pos, ray, self.world)
            height = int(surface.get_height() / ray_info.distance)
            column = _get_column(
                textures[ray_info.hit - 1],
                ray_info.wall_x_rat, height)

            surface.blit(column, (x, surface.get_height() / 2 - height / 2))

            if ray_info.horizontal:
                surface.blit(dark, (x, 0))
