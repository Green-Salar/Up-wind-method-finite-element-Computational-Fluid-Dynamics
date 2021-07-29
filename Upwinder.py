import math

import numpy as np

import shapely
from shapely.geometry import LineString, Point
import numpy as np
import math
import math
import matplotlib.pyplot as plt
import numpy as np


# square = squaresQordinations[0]

# print(square)
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def upwind_intersectionFinder(PoL1, PoL2):
    line1 = LineString([PoL1[0], PoL1[1]])
    line2 = LineString([PoL2[0], PoL2[1]])
    D = [line1, line2]
    int_pt = D[0].intersection(D[1])
    if is_empty(int_pt):
        return False
    else:
        point_of_intersection = round(int_pt.x, 4), round(int_pt.y, 4)
        return point_of_intersection


def Lmax(square):
    x, y = square[0]
    Ymax = y
    Ymin = y
    Xmax = x
    Xmin = x
    for i in square:
        if i[1] > Ymax: Ymax = i[1]
        if i[1] < Ymin: Ymin = i[1]
        if i[0] > Xmax: Xmax = i[0]
        if i[0] < Xmin: Xmin = i[0]
    L = math.sqrt((Xmax - Xmin) ** 2 + (Ymax - Ymin) ** 2)
    return L


# square midi ba uv , ip 4x4 tahvil migiri baraye zarayeb
def square_upwinder(square, ips, uvs):
    L = 2 * Lmax(square)
    upwind_coef = []
    for i in range(0, 4):
        x_ip = ips[i][0]
        y_ip = ips[i][1]
        u = uvs[i][0]
        v = uvs[i][1]
        p1 = [x_ip, y_ip]
        if u == 0:
            x2 = x_ip
            y2 = y_ip - np.sign(v) * L
        else:
            m = v / u
            LMparams = L / math.sqrt(m ** 2 + 1)
            if np.sign(u) > 0:
                LMparams = -LMparams
            x2 = LMparams + x_ip
            y2 = LMparams * m + y_ip
        p2 = (x2, y2)
        #yesar ro ip yesar 2Lmax oonvartar
        GoP1 = [p1, p2]

        row = np.zeros(4)
        for i in range(0, 4):
            p1 = square[i]
            j = i + 1
            if j == 4: j = 0
            p2 = square[j]
            GoP2 = [p1, p2]
            thePoint = upwind_intersectionFinder(GoP1, GoP2)
            if thePoint:
                row[i] = distance(p2, thePoint) / distance(p1, p2)
                row[j] = distance(p1, thePoint) / distance(p1, p2)
                break
        upwind_coef.append(row)
    return upwind_coef

# coef = square_upwindFinder([(1, 1), (-1, 1), (-1, -1), (1, -1)], [(0, 1), (1, 0), (-1, -1), (1 / 2, -1 / 2)],
#                          [(1 / 2, 1 / 2), (1 / 2, -1 / 2), (-1 / 2, -1 / 2), (2 / 3, -2 / 3)])
# print(coef)
