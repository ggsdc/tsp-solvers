"""
This file contains the solution of each method 
"""
import os

# Method to get the files
path_to_tests_dir = os.path.dirname(os.path.abspath(__file__))


def get_test_file(relative_path):
    return os.path.join(path_to_tests_dir, relative_path)


# For the 10 vertex problem
GA_V10_COST = 54.557082002939914
GA_V10_GENES = [3, 0, 6, 9, 2, 8, 4, 5, 7, 1]

# For the 100 vertex problem
GA_V100_COST = 1723.1183843940112
GA_V100_GENES = [
    12,
    54,
    87,
    18,
    49,
    99,
    59,
    16,
    44,
    69,
    74,
    80,
    37,
    78,
    83,
    6,
    97,
    10,
    7,
    73,
    17,
    63,
    14,
    3,
    19,
    65,
    48,
    0,
    51,
    29,
    11,
    40,
    71,
    76,
    70,
    94,
    26,
    58,
    88,
    72,
    9,
    15,
    89,
    39,
    1,
    91,
    23,
    86,
    90,
    60,
    64,
    85,
    42,
    52,
    66,
    79,
    2,
    36,
    61,
    24,
    82,
    20,
    22,
    43,
    8,
    4,
    46,
    68,
    35,
    56,
    57,
    33,
    84,
    77,
    38,
    30,
    81,
    32,
    27,
    34,
    21,
    53,
    25,
    31,
    92,
    75,
    98,
    28,
    93,
    5,
    13,
    50,
    55,
    41,
    67,
    95,
    47,
    96,
    62,
    45,
]

# For the 1000 vertex problem
GA_V1000_COST = 0
GA_v1000_GENES = []
