from matplotlib import pyplot as plt
from scipy import signal
from scipy import misc
import numpy as np
ascent = misc.ascent()
scharr = np.array([[-3, 0,  +3],
                   [-10, 0, +10],
                   [-3, 0,  +3]])  # Gx + j*Gy
grad = signal.convolve2d(ascent, scharr, boundary='symm', mode='same')

plt.imshow(grad, interpolation='nearest')
plt.show()
