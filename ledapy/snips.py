"""
Random functions for occasional use
"""


def linewithpeaks(data, peaks):
    """
    plots line with overlaid peaks
    """
    from pylab import plot, show
    import numpy as np
    plot(data)
    for i in peaks:
        plot([i, i], [np.min(data), np.max(data)])
    show()
