# Project "GALAXY" - version 3 - DEBUG

""" For DEBUGGING & TUNING """
from matplotlib import pyplot as plt
from statistics import mean

IS_DEBUG_ENABLE = False  # Default is False (vs. True)
debug_factors_y = []  # used to compute and draw the factors and difference between factor_y(s)
debug_dt = []  # used to draw the dt over time
debug_speed_factor = []  # used to draw the speed_factor over time
debug_offset_y = []  # used to draw the current_offset_y over time

""" 
    DEBUGGING, VISUALIZATION & TUNING (see https://matplotlib.org/)
"""


def debug_and_tune(self):
    print(f"debug_and_tune... ")
    plt.plot(self.debug_dt, label="dt")
    plt.title('Dt over time')
    plt.xlabel('Time')
    plt.ylabel('Dt')
    plt.grid()
    avg_dt = round(mean(self.debug_dt), 4)
    plt.ylim(top=2 * avg_dt)  # ymax is your value
    plt.ylim(bottom=0)  # ymin is your value
    print(f"debug_and_tune: avg(dt)={avg_dt}")
    plt.hlines(avg_dt, xmin=0, xmax=len(self.debug_dt), label="avg(dt)", colors='red', linestyles='--', lw=2)
    plt.legend()
    plt.text(int(len(self.debug_dt) / 2), avg_dt + avg_dt / 10, str(f"avg={avg_dt}"),
             bbox=dict(facecolor='red', alpha=0.5))
    plt.show()

    plt.plot(self.debug_speed_factor)
    plt.title('Speed factor over time')
    plt.xlabel('Time')
    plt.ylabel('Speed factor')
    plt.grid()
    avg_sf = round(mean(self.debug_speed_factor), 2)
    plt.ylim(top=2 * avg_sf)  # ymax is your value
    plt.ylim(bottom=0)  # ymin is your value
    print(f"debug_and_tune: avg(sf)={avg_sf}")
    plt.hlines(avg_sf, xmin=0, xmax=len(self.debug_speed_factor), label="avg(sf)", colors='blue', linestyles='--', lw=2)
    # plt.legend()
    plt.text(int(len(self.debug_speed_factor) / 2), avg_sf + avg_sf / 10, str(f"avg={avg_sf}"),
             bbox=dict(facecolor='blue', alpha=0.5))
    plt.show()


"""
    plt.plot(self.debug_offset_y)
    plt.title('Current offset_y over time')
    plt.show()
    plt.plot(self.debug_factors_y)
    plt.title('Vertical factors on y')
    plt.show()
    result = map(lambda n1, n2: round(n1 - n2, 2), self.debug_factors_y[0:len(self.debug_factors_y) - 1],
                 self.debug_factors_y[1:])
    plt.plot(list(result))
    plt.title('Difference between vertical factors to remove optical illusion')
    plt.show()
"""

# Ref. https://stackoverflow.com/questions/41906679/how-to-calculate-and-plot-multiple-linear-trends-for-a-time-series
