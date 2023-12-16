#!/usr/bin/env python3

import os
from time import perf_counter_ns

class Tile:
    tiles = {}
    max_x = None
    max_y = None

    def calculate_load():
        load = 0
        for iy in range(Tile.max_y + 1):
            multiplier = Tile.max_y + 1 - iy
            for ix in range(Tile.max_x + 1):
                if Tile.tiles[iy][ix].tile_type == 'O':
                    load += multiplier
        return load

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
        Tile.tiles[y][x] = self

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

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        data = input_stream.read().split('\n')

    range_x = list(range(len(data[0])))
    for iy in range(len(data)):
        for ix in range_x:
            Tile(data[iy][ix], ix, iy)

    Tile.connect_all_neighbours()

    for iy in range(Tile.max_y + 1):
        tile_row = Tile.tiles[iy]
        for tile in tile_row.values():
            if tile.tile_type == 'O':
                tile.roll_up()

    answer = Tile.calculate_load()
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
