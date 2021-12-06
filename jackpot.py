import os
import sys
import platform
from datetime import datetime, timedelta
from subprocess import call, check_output
from threading import Timer
import matplotlib.pyplot as plt
import time
import numpy as np


""" Click a button at exactly the right time.

The median reaction time of human being is 254 milliseconds, but this script
will get your reaction time to 350 microseconds, a thousand times faster.

"""

class CustomTimer(Timer):
    """ a custom timer for returning the execution time of a input function, from
    http://stackoverflow.com/a/28636221/560844
    """
    def __init__(self, interval, function, args=[], kwargs={}):
        self._original_function = function
        super(CustomTimer, self).__init__(
            interval, self._do_execute, args, kwargs)

    def _do_execute(self, *a, **kw):
        self.result = self._original_function(*a, **kw)

    def join(self):
        super(CustomTimer, self).join()
        return self.result

def submit(run_at="2015-05-7 16:00:00.000000", timer="Custom", overhead_sec=0.0):
    """

    Main function to submit the task, e.g., to click on the astro-ph button.

    Parameters
    ---
    run_at: str
        targeted time to click, in format like "2015-05-7 16:00:00.000000".

    timer: str
        which timer to use, default to use the Custom Timer instead of the default Timer.

    overhead_sec: float
        Estimate for the overhead time in seconds, so that the click is aimed at 'run_at - overhead_sec'.
        Note that the code has a prevention mechanism so that even if you input an absurd overhead_sec the
        execution time would still be after 'run_at'.

    Returns
    ---
    goal: datetime
        Actual targeted time (without the overhead)

    real: datetime
        Real execution time

    """
    now = datetime.now()
    goal = datetime.strptime(run_at, "%Y-%m-%d %H:%M:%S.%f")
    delay = (goal - now).total_seconds() - overhead_sec
    if timer == 'Custom':
        c = CustomTimer(delay, click, [goal])
        c.start()
        real = c.join()
    elif timer == 'Simple':
        Timer(delay, click, [goal]).start()
        real = None
    return(goal, real)

def click(goal, mysys=None):
    """ click at 'goal' time

    Parameters
    ---
    goal: datetime
        targeted run time

    Returns
    ---
    real: datetime
        real run time

    """
    if mysys is None:
        mysys = platform.system()
    real = datetime.now()
    while(real < goal):
        # too early!
        wait = goal - real
        # convert wait to seconds
        waitsec = wait.seconds + wait.microseconds/1000000.0
        time.sleep(waitsec)
        real = datetime.now()
    if mysys == "Darwin":
        call(["./cliclick", "c:."])
    elif mysys == "Linux":
        call(["xdotool", "click", "1"])
    return(real)

def click_to_win(run_at="2015-05-7 16:00:00.000000", overhead_sec=0.0):
    print(("Will click at %s with %10.6f seconds of overhead" % (run_at, overhead_sec)))
    goal, real = submit(run_at, timer='Custom', overhead_sec=overhead_sec)
    overhead = real - goal
    _overhead = overhead.microseconds
    print(("Success! The overhead [microseconds] is \n %10.6f" % _overhead))
    return(_overhead)

if __name__ == "__main__":
    try:
        run_at = sys.argv[1]
        overhead_microsec = float(sys.argv[2])
    except IndexError:
        print("python jackpot.py '2017-03-31 13:08:00.000000' overhead_microsec")
        quit()
    click_to_win(run_at, overhead_sec=overhead_microsec/1.0e6)
