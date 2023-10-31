import matplotlib.pyplot as plt
from math import ceil
import numpy as np

def plot_fit_results(x, y, popt, func, title="", save_file=None):

    x = np.array(x)
    y = np.array(y)

    fit = func(x, *popt)

    fig, ax = plt.subplots(figsize=(8,5))

    ax.scatter(x, y, s=50)
    ax.plot(x, fit , ls='-', c='black', lw=1.5)

    # ax.set_xlim(-0.2, 4)
#     ax.set_ylim(-10, max(y)+50)

    # ax.xaxis.set_major_locator(ticker.FixedLocator(range(0, ceil(max(x)), 1)))
    # ax.xaxis.set_minor_locator(ticker.FixedLocator([i/10 for i in range(0, int(max(x)*10), 1)]))

    ax.tick_params(which='major', labelsize='xx-large', length=8, width=2)
    ax.tick_params(which='minor', length=5, width=2)

    plt.xticks(fontname = "Arial Unicode MS")
    plt.yticks(fontname = "Arial Unicode MS")

    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)

    ax.set_title(title)
    if not save_file is None:
        fig.savefig(save_file, format="svg")
    
    plt.show()

if __name__ == '__main__':
    from scipy.optimize import curve_fit

    def fit_function(x, a, b, c):
        return a*b**x + c

    popt, pcov = curve_fit(fit_function, x, y, maxfev=10000, p0=[10000,0.95,-10000])

    plot_fit_results(x, y, popt, fit_function, title="", save_file=None)
