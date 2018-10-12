import time


def time_of_execute_decorator(func):

    def time_measurement(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print("time of execute: " + str(time.time() - start_time) + ' seconds')

    return time_measurement


@time_of_execute_decorator
def sleep_for_five_sec():
    time.sleep(5)


sleep_for_five_sec()
