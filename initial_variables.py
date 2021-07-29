import math

import numpy
import numpy as np
k = 44  # W/m2C
ro = 7830  # kg/m3
cp = 481  # j/kgC
pi = math.pi
Nx=int(input('Nx'))
Ny = Nx
dt = float(input('dt'))
A=float(input('A'))
peclet= 480
ittrexit=2000
# input('peclet num')
H=peclet*k/(ro*cp*A)
W=H
print('h is',H)
delatTetaX = pi / (Nx - 1)
delatTetaY = pi / (Ny - 1)
deltaYn = 1 / (Ny - 1)
deltaXn = 1 / (Nx - 1)

alpha = k / (ro * cp)

T = np.zeros(Nx * Ny)

C= cp
Peclet = ro * C * A * H / k


def V(x, y):
    V = np.zeros(2)
    V[0] = A * math.sin(pi * (x + 0.5)) * math.cos(pi * (y + 0.5))
    V[1] = - A * math.cos(pi * (x + 0.5)) * math.sin(pi * (x + 0.5))
    return V

for i in range(0, int(Nx * Ny)):
    T[i] = 115
rightEdge = []
leftEdge = []

for i in range(1, Ny):
    rightEdge.append(i * Nx)
    leftEdge.append(i * Nx - 1)

leftEdge.append(Ny * Nx - 1)
top = []
bot = []
for i in range(0, Nx):
    top.append(i)
    bot.append((Nx * Ny) - Nx + i)

cornersPadSaatGard = [0, Nx - 1, Ny * Nx - 1, (Ny - 1) * Nx]

edges80 = []
edges80 = np.concatenate((leftEdge, rightEdge, bot), axis=0)
for i in edges80:
    T[i] = 80
for i in top:
    T[i] = 530

T[cornersPadSaatGard[0]] = (80 + 530) / 2
T[cornersPadSaatGard[1]] = (80 + 530) / 2
