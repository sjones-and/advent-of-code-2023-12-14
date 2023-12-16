#!/usr/bin/env python3

import os
from time import perf_counter_ns

class Tile:
    tiles = {}
    tiles_x = {}
    max_x = None
    max_y = None

    def cycle():
        for iy in range(Tile.max_y + 1):
            tile_row = Tile.tiles[iy]
            for tile in tile_row.values():
                if tile.tile_type == 'O':
                    tile.roll_up()

        for ix in range(Tile.max_x + 1):
            tile_col = Tile.tiles_x[ix]
            for tile in tile_col.values():
                if tile.tile_type == 'O':
                    tile.roll_left()

        for iy in range(Tile.max_y, -1, -1):
            tile_row = Tile.tiles[iy]
            for tile in tile_row.values():
                if tile.tile_type == 'O':
                    tile.roll_down()

        for ix in range(Tile.max_x, -1, -1):
            tile_col = Tile.tiles_x[ix]
            for tile in tile_col.values():
                if tile.tile_type == 'O':
                    tile.roll_right()
        
        return Tile.calculate_hash()

    def calculate_load():
        load = 0
        for iy in range(Tile.max_y + 1):
            multiplier = Tile.max_y + 1 - iy
            for ix in range(Tile.max_x + 1):
                if Tile.tiles[iy][ix].tile_type == 'O':
                    load += multiplier
        return load

    def calculate_hash():
        hash = 0
        for iy in range(Tile.max_y + 1):
            multiplier = (Tile.max_y + 1 - iy)
            for ix in range(Tile.max_x + 1):
                if Tile.tiles[iy][ix].tile_type == 'O':
                    hash += multiplier * ix
        return hash

    def connect_all_neighbours():
        Tile.max_y = max(Tile.tiles.keys())
        Tile.max_x = max(Tile.tiles[0].keys())
        for tile_row in Tile.tiles.values():
            for tile in tile_row.values():
                tile.connect_neighbours()

    def __init__(self, tile_type, x, y):
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.to_left = None
        self.to_right = None
        self.to_top = None
        self.to_bottom = None
        if not Tile.tiles.get(y, None):
            Tile.tiles[y] = {}
        if not Tile.tiles_x.get(x, None):
            Tile.tiles_x[x] = {}
        Tile.tiles[y][x] = self
        Tile.tiles_x[x][y] = self

    def connect_neighbours(self):
        if self.x > 0:
            self.to_left = Tile.tiles[self.y][self.x - 1]
        if self.y > 0:
            self.to_top = Tile.tiles[self.y - 1][self.x]
        if self.x < Tile.max_x:
            self.to_right = Tile.tiles[self.y][self.x + 1]
        if self.y < Tile.max_y:
            self.to_bottom = Tile.tiles[self.y + 1][self.x]
        
    def roll_up(self):
        if self.to_top and self.to_top.tile_type == '.':
            self.tile_type = '.'
            self.to_top.tile_type = 'O'
            self.to_top.roll_up()

    def roll_left(self):
        if self.to_left and self.to_left.tile_type == '.':
            self.tile_type = '.'
            self.to_left.tile_type = 'O'
            self.to_left.roll_left()

    def roll_down(self):
        if self.to_bottom and self.to_bottom.tile_type == '.':
            self.tile_type = '.'
            self.to_bottom.tile_type = 'O'
            self.to_bottom.roll_down()

    def roll_right(self):
        if self.to_right and self.to_right.tile_type == '.':
            self.tile_type = '.'
            self.to_right.tile_type = 'O'
            self.to_right.roll_right()

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        data = input_stream.read().split('\n')

    range_x = list(range(len(data[0])))
    for iy in range(len(data)):
        for ix in range_x:
            Tile(data[iy][ix], ix, iy)

    Tile.connect_all_neighbours()

    patterns = []
    loads = []

    while True:
        for _ in range(250):
            patterns.append(Tile.cycle())
            loads.append(Tile.calculate_load())

        subsets = (
            (i, int(j / 2))
            for i in range(0, len(patterns) - 50 + 1)
            for j in range(50, len(patterns) - i + 1, 2)
            if patterns[i:i+int(j/2)] == patterns[i+int(j/2):i+j]
        )

        if repetition := next(subsets, None):
            start_pos, period = repetition
            print(start_pos, period, start_pos + period)
            repetition_pos = (1000000000 - start_pos) % period
            answer = loads[start_pos + repetition_pos - 1]
            break

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
