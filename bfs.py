import pygame as pg
from random import random
from math import sqrt
from collections import deque
import time
from PIL import Image
from find_color import qwe_2

bad_colors = [(216, 207, 200), (171, 211, 223), (217, 208, 201), (205, 196, 189), (167, 167, 165), (215, 206, 199),
              (214, 203, 197), (217, 206, 200), (209, 200, 193), (215, 208, 202), (219, 210, 203), (204, 197, 191),
              (205, 198, 192), (209, 204, 200), (202, 195, 187), (207, 196, 190), (219, 210, 201), (213, 204, 195),
              (217, 208, 201), (168, 167, 165), (175, 174, 170), (225, 221, 218), (227, 222, 218), (216, 209, 203),
              (210, 201, 194), (230, 226, 223), (221, 214, 208), (199, 201, 180), (223, 214, 205), (168, 167, 165),
              (197, 196, 194), (202, 196, 180), (204, 199, 196), (178, 174, 173), (224, 219, 213), (222, 215, 207),
              (212, 205, 197), (216, 207, 200), (157, 156, 154), (223, 212, 210), (223, 215, 212), (217, 208, 201),
              (211, 202, 193), (211, 210, 206), (220, 215, 212), (222, 213, 206), (176, 175, 173), (205, 201, 198),
              (209, 204, 198), (223, 214, 209), (217, 206, 200)]


def tank(sc, cords, TILE_2=sqrt(3) * 17 / 2, shift=20):
    if cords[1] % 2 != 0:
        shift_2 = 25
    else:
        shift_2 = 0
    y_0 = 0
    for row in qwe_2:
        x_0 = 0
        for i in row:
            if i != (255, 255, 255):
                pg.draw.line(sc, i,
                             (cords[0] * TILE + 2 + shift * cords[0] + shift_2 + x_0 - 3,
                              cords[1] * TILE_2 + 2 + y_0 - 7),
                             (cords[0] * TILE + 2 + shift * cords[0] + shift_2 + x_0 - 3,
                              cords[1] * TILE_2 + 2 + y_0 - 7))
            x_0 += 1
        y_0 += 1


def get_pixel(w=2 + sqrt(3) * 15 / 2, TILE_2=sqrt(3) * 17 / 2, shift=20, q=16):
    img = Image.open('2_2.jpg')
    full_pixel = []
    for y, row in enumerate(range(rows)):
        row_pixel = []
        if y % 2 != 0:
            shift_pixel = 25
        else:
            shift_pixel = 0
        for x, col in enumerate(range(cols)):
            row_pixel.append(1 if img.getpixel((((x * TILE + q + shift * x + shift_pixel) / 1) * 1,
                                                ((y * TILE_2 + w) / 1) * 1)) in bad_colors else 0)
        full_pixel.append(row_pixel)
    return full_pixel


def put_pixel(list_pixel):
    img = Image.open('2.png')
    for y_pixel, row in enumerate(list_pixel):
        print(row)
        for x_pixel, i in enumerate(row):
            # print(i)
            # print(x_pixel)
            # print(y_pixel)
            if i == 1:
                img.putpixel((x_pixel, y_pixel), (0, 0, 0))
            else:
                img.putpixel((x_pixel, y_pixel), (255, 255, 255))
    img.show()
    img.save('2.png')


def get_rect(x, y, TILE_2=sqrt(3) * 17 / 2, shift=20):
    if y % 2 != 0:
        shift_2 = 25
    else:
        shift_2 = 0
    # print(x)
    # print(y)
    return [(x * TILE + 2 + shift * x + shift_2, y * TILE_2 + 2 + sqrt(3) * 15 / 2),
            (x * TILE + 2 + 7.5 + shift * x + shift_2, y * TILE_2 + 2),
            (x * TILE + 2 + 22.5 + shift * x + shift_2, y * TILE_2 + 2),
            (x * TILE + 2 + 30 + shift * x + shift_2, y * TILE_2 + 2 + sqrt(3) * 15 / 2),
            (x * TILE + 22.5 + 2 + shift * x + shift_2, y * TILE_2 + 2 + sqrt(3) * 15),
            (x * TILE + 2 + 7.5 + shift * x + shift_2, y * TILE_2 + 2 + sqrt(3) * 15)]


def get_next_nodes(x, y, choice):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    # print(check_next_node)
    if not choice:
        ways = [0, 1], [0, 2], [1, 1], [1, -1], [0, -2], [0, -1]
    else:
        ways = [-1, 1], [0, 2], [0, 1], [0, -1], [0, -2], [-1, -1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = (x - 25 * x // 62) // TILE, y // 15
    pg.draw.polygon(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def get_click_mouse_start():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = (x - 25 * x // 62) // TILE, y // 15
    pg.draw.polygon(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


shift_2 = 0
cols, rows = 28, 51
TILE = 30

pg.init()
sc = pg.display.set_mode([24 * 59, 13 * 59])
clock = pg.time.Clock()

# grid
list_pixel = get_pixel()
put_pixel(list_pixel)
grid = list_pixel
print(len(grid))
print(len(grid[0]))
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    if y % 2 == 0:
        choice = True
    else:
        choice = False
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y, choice)

print(graph[0, 0])

# BFS settings
start = False
bg = pg.image.load('2_2.jpg').convert()
while True:
    sc.blit(bg, (0, 0))
    # draw grid
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == 1:
                pg.draw.polygon(sc, pg.Color('darkmagenta'),
                                get_rect(x, y), width=5)
    if not start:
        start = get_click_mouse_start()
        goal = start
        queue = deque([start])
        visited = {start: None}
    else:

        # draw BFS work
        [pg.draw.polygon(sc, pg.Color('forestgreen'), get_rect(x, y), width=3) for x, y in
         visited]
        [pg.draw.polygon(sc, pg.Color('darkslategray'), get_rect(x, y), width=3) for x, y
         in queue]

        # bfs, get path to mouse click
        mouse_pos = get_click_mouse_pos()
        if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
            queue, visited = bfs(start, mouse_pos, graph)
            goal = mouse_pos

        # BFS
        if queue:
            cur_node = queue.popleft()
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        # draw path
        path_head, path_segment = goal, goal
        while path_segment and path_segment in visited:
            pg.draw.polygon(sc, pg.Color('white'), get_rect(path_segment[0], path_segment[1]))
            path_segment = visited[path_segment]
        tank(sc, (start[0], start[1]))
        # pg.draw.polygon(sc, pg.Color('blue'), get_rect(start[0], start[1]))
        pg.draw.polygon(sc, pg.Color('magenta'), get_rect(path_head[0], path_head[1]))

        # print('Очередь')
        # print(queue)
        # print('Визит')
        # print(visited)
        # pygame
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(100)
