class Scene:
    def __init__(self, world, sprites, camera):
        self.world = world
        self.sprites = sprites
        self.camera = camera

    def update(self, dt):
        cam_x, cam_y = self.camera.pos
        for s in self.sprites:
            dist_x, dist_y = (
                cam_x - s.x,
                cam_y - s.y)
            e_dist_squared = dist_x**2 + dist_y**2
            if e_dist_squared <= 0.2**2:
                s.on_touch()
