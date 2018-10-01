import multiprocessing
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def distribute(lst, n):
        """distributes lst as equal as possible to n elements
        """
        base_load = len(lst)//n
        extra_load = len(lst)%n
        load_per_element = [base_load for i in range(n)]
        for i in range(len(load_per_element)):
            if extra_load <= 0: break
            load_per_element[i] +=  1 if extra_load > 0 else 0
            extra_load -= 1
        indexes = [sum(load_per_element[:i+1]) for i in range(n)]
        indexes.insert(0, None) #added so that slicing can be used
        indexes.append(None)
        elements = [lst[indexes[i]:indexes[i+1]] for i in range(n)]
        return elements

def denoise(values, x=None, resolution=None):
    """Denoise input via spline interpolation
    Args:
        values  (iterable): Iterable with values that are to be interpolated
        x      (iteratble): corresponding x values - Defaults to a numpy array from 0 on with 1 for every value
        resolution   (int): Sets how many segments your original data will be split into for interpolation, lower is closer to original data
    Returns:
        tuple of iterables: (x_values_of_interpolation, interpolated_y_values)
    """
    resolution = len(values)//10 if resolution is None else resolution
    segments = len(values)//resolution
    segments = distribute(values, segments)
    average = []
    for segment in segments:
        average.append(sum(segment)/len(segment))
    x = np.linspace(0, len(values), len(average)) if x is None else x
    spline = interp1d(x, average, kind="cubic")
    y = spline(x)
    return x, y

path = os.path.dirname(__file__)
with open(path+"/times2", "r") as f:
        content = f.readlines()
        values = list(map(float, content))

denoised_x, denoised_y = denoise(values, resolution=500)

plt.plot(range(len(values)), values)
plt.plot(denoised_x, denoised_y)
plt.show()
