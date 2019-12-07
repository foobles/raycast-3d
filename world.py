class World:
    def __init__(self, map):
        for row in map:
            if len(row) != len(map[0]):
                raise ValueError("All map rows must have equal length.")
        self._map = map 
        self.width = len(map[0]) 
        self.height = len(map)

    def __getitem__(self, pos):
        x, y = pos 
        if not self.is_in_bounds(x, y):
            raise ValueError("Out of bounds access of world.")
        return self._map[y][x]

    def has_tile_at(self, x, y):
        return self.is_in_bounds(x, y) and bool(self[x, y])

    def is_in_bounds(self, x, y):
        return (x >= 0 and 
            x < self.width and 
            y >= 0 and 
            y < self.height)  
