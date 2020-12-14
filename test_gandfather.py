import pygame as pg
from time import perf_counter
from shapely.geometry import Point, Polygon


# Vars
triangles = [[(100, 600), (400, 80), (700, 600)]]
SQRT_3 = 3 ** (1 / 2)
WHITE = (255, 255, 255)

# Graphics part
pg.init()
screen = pg.display.set_mode((800, 800))


# Funcs
distance = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5


def generatePoints(pt1, pt2, reference):
    slope = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
    a = pt1[0] + (pt2[0] - pt1[0]) / 3
    b = pt1[1] + (pt2[1] - pt1[1]) / 3
    c = pt1[0] + (pt2[0] - pt1[0]) * 2 / 3
    d = pt1[1] + (pt2[1] - pt1[1]) * 2 / 3
    ptm = (pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2
    dis = distance((a, b), (c, d))
    h = SQRT_3/2 * dis
    if slope == 0:
        ptc1 = ptm[0], ptm[1] - h
        ptc2 = ptm[0], ptm[1] + h
        ptc = ptc1 if distance(reference, ptc1) > distance(ptc2, reference) else ptc2
        return (round(a), round(b)), (round(c), round(d)), ptc
    perp = -1 / slope
    x_c = h / (perp ** 2 + 1) ** 0.5
    y_c = perp * x_c
    ptc1 = round(ptm[0] - x_c), round(ptm[1] - y_c)
    ptc2 = round(ptm[0] + x_c), round(ptm[1] + y_c)
    ptc = ptc1 if distance(reference, ptc1) > distance(ptc2, reference) else ptc2
    return (round(a), round(b)), (round(c), round(d)), ptc


def split(tri):
    a, b, c = generatePoints(tri[0], tri[1], tri[2])
    d, e, f = generatePoints(tri[1], tri[2], tri[0])
    g, h, i = generatePoints(tri[2], tri[0], tri[1])
    return [a, c, b], [b, tri[1], d], [d, f, e], [e, tri[2], g], [g, i, h], [h, tri[0], a]


def run(array: list, level):
    for l in range(level):
        org = array.copy()
        for tri in org:
            for thing in split(tri):
                array.append(thing)

start = perf_counter()
run(triangles, 7)


# Game Loop
while True:
    screen.fill((0, 0, 0))
    for triangle in triangles:
        pg.draw.polygon(screen, WHITE, triangle)
    # exit code
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit(0)
    # Updating
    pg.display.update()
    print(perf_counter() - start)
