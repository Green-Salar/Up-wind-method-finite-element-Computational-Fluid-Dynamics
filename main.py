import nt

import shapely
from shapely.geometry import LineString, Point
import numpy as np
import math
import math
import matplotlib.pyplot as plt
import numpy as np
# from Grid_and_ds_generator import *
# from dnds_dndt import *

# grid and ds dx has been generated in th Grid file
# dnds dndt for integration points
from Grid_and_ds_generator import *

from scipy import linalg


#   dnds dndt of volumes center of sub cv
# dndx dndy and volumes for each ip

def DNDXY(X, Y):
    volumes = np.zeros(4)
    dndx = np.zeros((4, 4))
    dndy = np.zeros((4, 4))

    for ip in range(0, 4):
        temp = dndx_dndy_vol_ip(ip, X, Y)
        dndx[ip] = temp[0]
        dndy[ip] = temp[1]
        volumes[ip] = temp[2]

    return dndx, dndy, volumes


# atention for dsx k and j  + -
def CEOF(dsx_el, dsy_el, dndx, dndy, Vol, alpha, T_old, UV , cUpwinds):
    D = np.zeros(4)
    C = np.zeros((4, 4))
    for i in range(0, 4):
        j = i
        k = j - 1
        if j == 0:
            k = 3
        for m in range(0, 4):
            C[i][m] = - alpha * (
                    dndx[i][m] * (dsx_el[j]) + dndy[i][m] * (dsy_el[j]) -
                    dndx[k][m] * dsx_el[k] - dndy[k][m] * dsy_el[k]) + (
                    UV[j][0]*dsx_el[j]*cUpwinds[j][m] + UV[j][1]*dsy_el[j]*cUpwinds[j][m] -
                    UV[k][0]*dsx_el[k]*cUpwinds[k][m] - UV[k][1]*dsy_el[k]*cUpwinds[k][m])

            if m == i:
                C[i][m] = C[i][m] + (Vol[i] / dt)

        D[i] = T_old[i] * Vol[i] / dt
    return C, D


# for hame eleman haro bere squares:

err = 300
ittr = 0
while (err > .2):
    ittr = ittr + 1
    if(ittr==ittrexit):break
    if ittr%50==0: print(ittr)
    elemNum = 0
    A = np.zeros((Nx * Ny, Nx * Ny))
    B = np.zeros(Nx * Ny)
    for square in squaresQordinations:
        X = []
        Y = []
        for XY in square:
            X.append(XY[0])
            Y.append(XY[1])
        temp = DNDXY(X, Y)
        dndx = temp[0]
        dndy = temp[1]
        Volumes = temp[2]
        il = squareNums[elemNum]
        T_old_eleman = []
        for m in il:
            T_old_eleman.append(T[m])
        answer_CD = CEOF(dsx[elemNum], dsy[elemNum], dndx, dndy, Volumes, alpha, T_old_eleman,UV_elemans[elemNum],C_upwinds[elemNum])
        C = answer_CD[0]
        D = answer_CD[1]

        for i in range(0, 4):
            for j in range(0, 4):
                A[il[i]][il[j]] = A[il[i]][il[j]] + C[i][j]
            B[il[i]] = B[il[i]] + D[i]

        elemNum = elemNum + 1

    for i in edges80:
        for j in range(0, Nx * Ny):
            A[i, j] = 0
        A[i, i] = 1
        B[i] = 80

    for i in top:
        for j in range(0, Nx * Ny):
            A[i, j] = 0
        A[i, i] = 1
        B[i] = 530

    B[cornersPadSaatGard[0]] = (80 + 535) / 2
    B[cornersPadSaatGard[1]] = (80 + 535) / 2

    Tnew = np.linalg.solve(A, B)

    err = 0
    for i in range(0, Nx * Ny):
        err = err + abs(Tnew[i] - T[i])
        T[i] = Tnew[i]



import matplotlib.pyplot as plt

Xs=np.reshape(xs,(Nx,Ny))
Ys=np.reshape(ys,(Nx,Ny))
T = np.reshape(T, (Nx, Ny))
def dashLinePlotting():
    plt.figure()
    cp = plt.contour(Xs, Ys, T, colors='black', linestyles='dashed')
    plt.clabel(cp, inline=True,
               fontsize=10)
    plt.title('Contour Plot')
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.show()

def contourPlloting():
    fig = plt.figure(figsize=(10,10))
    left, bottom, width, height = 0.1, 0.1,.8, 0.8
    ax = fig.add_axes([left, bottom, width, height])

    cp = plt.contourf(Xs, Ys, T)
    plt.colorbar(cp)

    ax.set_title('Contour Plot')
    ax.set_xlabel('x (cm)')
    ax.set_ylabel('y (cm)')
    plt.show()

def colorLinePlotitng():
    fig = plt.figure(figsize=(6,5))
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes([left, bottom, width, height])
    cp = ax.contour(Xs, Ys, T)
    ax.clabel(cp, inline=True,
              fontsize=10)
    ax.set_title('Contour Plot')
    ax.set_xlabel('x (cm)')
    ax.set_ylabel('y (cm)')
    plt.show()

dashLinePlotting()
contourPlloting()
colorLinePlotitng()
g=9
g = 0