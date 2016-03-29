# Copyright 2015 Environment Systems
# All rights reserved

""" Contains additional "Expected Conditions" for selenium webdriver elements
"""

class more_windows_than(object):
    """ An expectation checking the window count against the desired
        window count.
    """
    def __init__(self, window_count):
        self.window_count = window_count

    def __call__(self, driver):
        return len(driver.window_handles) > self.window_count

class new_window_created(object):
    """ An expectation checking whether a new window has been created.
        It checks this against the list of previous windows, passed as a parameter
        If more than one new window is found, it returns the name of the first one
    """

    def __init__(self, previous_windows):
        self.previous_windows = previous_windows

    def __call__(self, driver):
        if len(driver.window_handles) > len(self.previous_windows):
            wins = [x for x in driver.window_handles if x not in self.previous_windows]
            if len(wins):
                return wins[0]
        return False
