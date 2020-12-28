import random
import time


def sleep_with_jitter(base_sleep_seconds: int):
    jitter_range = int(base_sleep_seconds / 5)
    sleep_seconds = base_sleep_seconds + random.randrange(-jitter_range, jitter_range)
    time.sleep(sleep_seconds)
