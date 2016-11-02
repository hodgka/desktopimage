import numpy as np
import matplotlib.pyplot as plt


N = 2000
rad = 10
tck = 5
sep = 5


def create_datasets(radius, thickness, separation, n=2000):
    y = np.random.random_integers(0, 1, size=n)
    x = np.empty((n, 2))
    for i in range(n):
        if y[i] == 1:
            x[i] = create_pos(radius, separation, thickness)
        else:
            x[i] = create_neg(radius, separation, thickness)
    return x


def create_pos(radius, separation, thickness):
    # r in arc centered at 0
    r = np.random.uniform(radius, radius + thickness)
    print r
    # angle in arc centered at 0
    angle = np.radians(np.random.uniform(0, 180))
    x = r*np.cos(angle) - (radius/2 + thickness/float(radius))
    y = r*np.sin(angle) + separation/2.0
    return np.array([x, y])


def create_neg(radius, separation, thickness):
    # r in arc centered at 0
    r = np.random.uniform(radius, radius + thickness)
    # angle in arc centered at 0
    angle = np.radians(np.random.uniform(0, 180))
    x = r*np.cos(angle) + (radius/2 + thickness/float(radius))
    y = -r*np.sin(angle) - separation/2.0
    return (x, y)


x = create_datasets(rad, tck, sep, N)

fig = plt.figure(1)
plt.scatter(x[:, 0], x[:, 1])
plt.show()
