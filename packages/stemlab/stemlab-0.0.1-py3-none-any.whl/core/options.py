from pandas import set_option
from numpy import set_printoptions

def display_options(decimals=14, nrows=50, ncols=50):
    """
    Set display options for Pandas DataFrame display.
    """
    set_printoptions(precision=decimals)
    set_option('display.precision', decimals)
