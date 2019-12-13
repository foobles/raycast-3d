import pygame as pg


class RayHitInfo:
    def __init__(self, hit, distance, horizontal, wall_x_rat):
        self.hit = hit
        self.distance = distance
        self.horizontal = horizontal
        self.wall_x_rat = wall_x_rat


def _get_ray_hit_info(pos, ray, world, textures):
    pos_x, pos_y = pos
    ray_x, ray_y = ray
    ray_x = ray_x or 0.01
    ray_y = ray_y or 0.01
    tile_x, tile_y = int(pos_x), int(pos_y)
    x_tile_dist = abs(1 / ray_x)
    y_tile_dist = abs(1 / ray_y)

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

    ret = []
    hit = 0
    while hit == 0 or textures[hit-1].transparent:
        if x_dist_moved < y_dist_moved:
            x_dist_moved += x_tile_dist
            tile_x += x_step
            horizontal = False
        else:
            y_dist_moved += y_tile_dist
            tile_y += y_step
            horizontal = True
        hit = world[tile_x, tile_y]
        if hit > 0:
            if horizontal:
                distance = (tile_y - pos_y + (1-y_step) / 2) / ray_y
                wall_x_rat = abs(pos_x + ray_x * distance) % 1
            else:
                distance = (tile_x - pos_x + (1-x_step) / 2) / ray_x
                wall_x_rat = abs(pos_y + ray_y * distance) % 1
            ret.insert(0, RayHitInfo(hit, distance, horizontal, wall_x_rat))

    return ret


def _get_column(texture, x_rat, height):
    vertical = texture.subsurface(pg.Rect(
        int(texture.get_width() * x_rat),
        0,
        1,
        texture.get_height()))

    return pg.transform.scale(vertical, (1, height))


class Scene:
    def __init__(self, world, sprites, camera):
        self.world = world
        self.sprites = sprites 
        self.camera = camera

    def render_walls(self, surface, textures):
        surface_height = surface.get_height()
        dark = pg.Surface((1, surface_height))
        dark.fill((0, 0, 0))
        dark.set_alpha(0.3 * 256)
        z_buf = []

        for x, ray in self.camera.rays(surface.get_width()):
            ray_infos = _get_ray_hit_info(
                self.camera.pos,
                ray,
                self.world,
                textures)
            z_buf.append(ray_infos[0].distance)

            for ray_info in ray_infos:
                height = int(surface_height / ray_info.distance)
                column = _get_column(
                    textures[ray_info.hit - 1].surface,
                    ray_info.wall_x_rat,
                    height)

                surface.blit(column, (x, surface_height / 2 - height / 2))

                if (ray_info.horizontal and
                        not textures[ray_info.hit-1].transparent):
                    surface.blit(dark, (x, 0))
        return z_buf 

    def render_sprites(self, surface, z_buf):
        pos_x, pos_y = self.camera.pos 
        plane_x, plane_y = self.camera.screen 
        dir_x, dir_y = self.camera.dir 
        self.sprites.sort(key=lambda spr: (pos_x - spr.x)**2 + (pos_y - spr.y)**2)

        for spr in self.sprites:
            sr_x, sr_y = spr.x - pos_x, spr.y - pos_y 
            det =  1 / (plane_x  * dir_y - dir_x * plane_y)
            trans_x, trans_y = ( 
                det * (dir_y * sr_x - dir_x * sr_y),
                det * (-plane_y * sr_x + plane_x * sr_y))
            
            height = int(abs(surface.get_height() / trans_y))
            spr_x_pos = surface.get_width() * (trans_x + 1) / (trans_y * 2) 
            draw_y = int(max(0, (surface.get_height() - height) / 2))
          
            width = abs(surface.get_width() / trans_y)
            draw_start_x = int(max(0, spr_x_pos - width / 2))
            draw_end_x = int(min(surface.get_width(), spr_x_pos + width / 2))
            cur_surface = pg.Surface((1, height)).convert_alpha() 
            print("rendering")
            for x in range(draw_start_x, draw_end_x):
                spr_surface_x = int(spr.surface.get_width() * (x - spr_x_pos + width / 2) / width)
                subsurface = spr.surface.subsurface(pg.Rect(spr_surface_x, 0, 1, spr.surface.get_height()))
                surface.blit(pg.transform.scale(subsurface, (1, height)), (x, draw_y)) 