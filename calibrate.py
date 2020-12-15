import os
import platform
from datetime import datetime, timedelta
from threading import Timer
from subprocess import call, check_output
from threading import _Timer
import matplotlib.pyplot as plt
import time
import numpy as np

def calibrate_overhead_distribution(ntrial=200, delay=0.1, nbin=40):
    """Calibrates the script overhead time distribution.
    """
    overhead_arr = np.zeros(ntrial)
    for i in xrange(ntrial):
        if np.mod(i, 10) == 0:
            print i,
        now = datetime.now()
        run_at = now + timedelta(seconds=delay)
        run_at = run_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        output = check_output(['python', 'jackpot.py', run_at, '0'])
        overhead = float(output.split('\n')[-2])
        overhead_arr[i] = overhead
    # overhead_arr = np.random.random(ntrial)*10000.0
    print('done')
    # calculate probabilities
    psafe = np.array([0.95, 0.80, 0.65, 0.50])
    colors = ['green', 'cyan', 'magenta', 'red']
    isafe = (psafe * float(ntrial)).astype(int)
    # descending order
    overhead_psafe = np.sort(overhead_arr)[::-1][isafe]
    # plotting
    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(211)
    ax.plot(overhead_arr, ls='None', marker="o", mfc="r", mec="k")
    ax.set_ylabel('overhead [microsec]', fontsize=12)
    ax.set_xlabel('# of trial', fontsize=12)
    #
    ax = plt.subplot(212)
    xmin, xmax = np.min(overhead_arr), np.max(overhead_arr)
    bins = np.linspace(xmin, xmax, nbin)
    hist = np.histogram(overhead_arr, bins=bins)[0]
    ymax = np.max(hist) * 1.4
    ax.step(bins[:-1], hist, where="post", color="k")
    mode = 0.5 * (bins[np.argmax(hist)] + bins[np.argmax(hist)+1])
    print("The most likely overhead calibrated against your computer is %10.6f microsec" % mode)
    for p, oh, color in zip(psafe, overhead_psafe, colors):
        _p = p * 100.0
        ax.axvline(oh, color=color, linestyle='solid', linewidth=1)
        ax.annotate(format(_p, '2.0f') + "% safe", xy=(oh, 0.95*ymax),
                xycoords='data', rotation=90, horizontalalignment='right',
                color=color, fontsize=12)
        print("pick %10.6f microsec with %4.2f%% chance of clicking after deadline." % (oh, _p))
    ax.set_ylim(0, ymax)
    ax.set_xlabel('overhead [microsec]', fontsize=12)
    ax.set_ylabel('N', fontsize=12)
    print("The minimum overhead calibrated against your computer is %10.6f microsec" % xmin)
    plt.show()

if __name__ == "__main__":
    # use "sudo ntpdate -s time.nist.gov" command to sync your clock first!
    calibrate_overhead_distribution(ntrial=200, delay=0.8, nbin=50)
