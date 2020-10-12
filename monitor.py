from datetime import datetime


def stop_watch(func, *args, **kwargs):
    start_time = datetime.now()
    func(*args, **kwargs)
    end_time = datetime.now()
    time_delta = end_time - start_time
    seconds=time_delta.seconds+time_delta.microseconds/10e6
    print("it takes {0:.3f} seconds".format(seconds))
