# pricing_constants.py

# Additional pricing factors based on neck types
NECK_TYPE_PRICES = {
    'round': 2,   # Additional price 2 for round neck
    'v': 3,       # Additional price 3 for V-neck
    'collar': 5   # Additional price 5 for collar
}

# Additional pricing factors based on sleeve lengths
SLEEVE_LENGTH_PRICES = {
    'no': 0,       # No Additional price for sleeveless
    'short': 2,    # Additional price 2 for short sleeves
    'long': 4      # Additional price 4 for long sleeves
}

# Additional pricing factors based on design preference
DESIGN_PREFERENCES_PRICES = {
    'plain': 0,    # No Additional price for plain design
    'custom_design': 20    # Additional price 20 for custom_design
}