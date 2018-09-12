
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d

# values from http://img.photobucket.com/albums/v495/Driftwood_Johnson/pressure_curve.jpg
black = {"time":
[0, 0.1, 0.25,  0.5,  0.7,  1,    1.7,  2,    2.5,  3,   3.5, 4], "pressure":
[0, 2000, 3200, 4000, 4700, 3500, 2000, 1600, 1000, 500, 250, 240]}

smokeless = {"time":
[0, 0.1, 0.25, 0.5,  0.7,  1,    1.5,  2,   2.5, 3,   3.5, 4], "pressure":
[0, 500, 1000, 6000, 9000, 4000, 1000, 500, 250, 240, 235, 230]}

black_fit = np.polyfit(black["time"], black["pressure"], 7)
sl_fit = np.polyfit(smokeless["time"], smokeless["pressure"], 5)
black_spline = interp1d(black["time"], black["pressure"], kind="cubic")
sl_spline = interp1d(smokeless["time"], smokeless["pressure"], kind="cubic")

time = np.linspace(0, 4, 100e3)
pressure_black = np.polyval(black_fit, time)
pressure_sl = np.polyval(sl_fit, time)
pressure_black_sp = black_spline(time)
pressure_sl_sp = sl_spline(time)
plt.plot(time, pressure_black_sp, label="blackpowder spline")
plt.plot(time, pressure_sl_sp, label="smokeless powder spline")
plt.plot(time, pressure_black, "--", label="blackpowder", alpha=0.5)
plt.plot(time, pressure_sl, "--", label="smokeless powder", alpha=0.5)

step = time[1]-time[0]
area_black = 0
area_sl = 0
for i in range(len(time)):
    area_black += pressure_black_sp[i]*step
    area_sl += pressure_sl_sp[i]*step

plt.annotate("18gr of smokeless" , xy=(1, 5000), arrowprops=dict(arrowstyle='->'), xytext=(1.5, 6000))
plt.annotate("82gr of blackpowder" , xy=(2, 1800), arrowprops=dict(arrowstyle='->'), xytext=(2.25, 4000))
plt.title(r"$\int_0^4$Blackpowder $\approx$ {:.2f}$\int_0^4$Smokeless".format(area_black/area_sl))
plt.xlabel("time/ms(?)")
plt.ylabel("pressure/psi")
plt.suptitle("Approximate pressurecurves of blackpowder and smokeless powder")
plt.legend()
plt.show()