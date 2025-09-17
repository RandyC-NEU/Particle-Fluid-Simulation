import numpy as np

c_x = lambda theta: (5*(np.pi - theta) * (1/np.tan(theta)))/(np.pi*2)
c_y = lambda theta: -(5*(np.pi - theta))/(np.pi*2)

print(c_x(np.deg2rad(150)))
