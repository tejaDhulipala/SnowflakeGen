import pygame as pg
from shapely.geometry import Point, Polygon
from time import perf_counter


# Vars
A = [(100, 600), (700, 600), (400, 80)]
triangles = [[(100, 600), (700, 600), (400, 80)]]
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


def generatePoints_2(pt1, pt2, father: Polygon):
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
        ptc = ptc1 if father.contains(Point(*ptc2)) else ptc2
        return (round(a), round(b)), (round(c), round(d)), ptc
    perp = -1 / slope
    x_c = h / (perp ** 2 + 1) ** 0.5
    y_c = perp * x_c
    ptc1 = round(ptm[0] - x_c), round(ptm[1] - y_c)
    ptc2 = round(ptm[0] + x_c), round(ptm[1] + y_c)
    ptc = ptc1 if father.contains(Point(*ptc2)) else ptc2
    return (round(a), round(b)), (round(c), round(d)), ptc


def generateSnowflake(array: list, level):
    for i in range(level):
        org = array.copy()
        for j in range(len(org)):
            pt1 = org[j]
            pt2 = org[(j + 1) % (len(org))]
            ref = None
            for triangle in triangles:
                if pt1 in triangle and pt2 in triangle:
                    b = triangle.copy()
                    b.remove(pt1)
                    b.remove(pt2)
                    ref = b[0]
            if ref == None:
                pta, ptb, ptc = generatePoints_2(pt1, pt2, Polygon(array))
            else:
                pta, ptb, ptc = generatePoints(pt1, pt2, ref)
            index = array.index(pt2)
            array.insert(index, ptb)
            array.insert(index, ptc)
            array.insert(index, pta)
            triangles.append([pta, ptb, ptc])

start = perf_counter()
# Call Func
generateSnowflake(A, 6)
print(len(A))

# Game Loop
while True:
    screen.fill(WHITE)
    A.append(A[0])
    for i in range(len(A) - 1):
        pg.draw.line(screen, (0, 0, 0), A[i], A[i + 1])
    # exit code
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit(0)
    # Updating
    pg.display.update()
    print(perf_counter() - start)
