from .pricing_constants import NECK_TYPE_PRICES, SLEEVE_LENGTH_PRICES, DESIGN_PREFERENCES_PRICES

class CustomApparel:
    """Class representing custom apparel with pricing."""    

    def __init__(self, base_price):
        """
        Initialize a CustomApparel instance.

        Parameters:
        - base_price (float): The base price of the apparel.
        """
        self._base_price = self._validate_positive_float(base_price)
        self._color = None
        self._size = None
        self._neck_type = None
        self._sleeve_length = None
        self._design_preference = None
        self._custom_design_details = None
        
    @property
    def base_price(self):
        """Get the base price of the apparel."""
        return self._base_price

    @property
    def color(self):
        """Get the color of the apparel."""
        return self._color

    @property
    def size(self):
        """Get the size of the apparel."""
        return self._size

    @property
    def neck_type(self):
        """Get the neck type of the apparel."""
        return self._neck_type

    @property
    def sleeve_length(self):
        """Get the sleeve length of the apparel."""
        return self._sleeve_length

    @property
    def design_preference(self):
        """Get the design preference of the apparel."""
        return self._design_preference

    @property
    def custom_design_details(self):
        """Get the custom design details of the apparel."""
        return self._custom_design_details

    def set_color(self, color):
        """
        Set the color of the apparel.

        Parameters:
        - color (str): The color of the apparel.
        """
        self._color = str(color)

    def set_size(self, size):
        """
        Set the size of the apparel.

        Parameters:
        - size (str): The size of the apparel.
        """
        self._size = str(size)

    def set_neck_type(self, neck_type):
        """
        Set the neck type of the apparel.

        Parameters:
        - neck_type (str): The neck type of the apparel.
        """
        if neck_type not in NECK_TYPE_PRICES:
            raise ValueError(f"Invalid neck type: {neck_type}")
        self._neck_type = neck_type

    def set_sleeve_length(self, sleeve_length):
        """
        Set the sleeve length of the apparel.

        Parameters:
        - sleeve_length (str): The sleeve length of the apparel.
        """
        if sleeve_length not in SLEEVE_LENGTH_PRICES:
            raise ValueError(f"Invalid sleeve length: {sleeve_length}")
        self._sleeve_length = sleeve_length

    def set_design_preference(self, design_preference):
        """
        Set the design preference of the apparel.

        Parameters:
        - design_preference (str): The design preference of the apparel.
        """
        if design_preference not in DESIGN_PREFERENCES_PRICES:
            raise ValueError(f"Invalid design preference: {design_preference}")
        self._design_preference = design_preference

    def set_custom_design_details(self, custom_design_details):
        """
        Set the custom design details of the apparel.

        Parameters:
        - custom_design_details (str): The custom design details of the apparel.
        """
        self._custom_design_details = str(custom_design_details)

    def calculate_total_price(self, quantity):
        """
        Calculate the total price of the apparel.

        Parameters:
        - quantity (int): The quantity of the apparel.

        Returns:
        - float: The total price of the apparel.
        """
        quantity = self._validate_positive_integer(quantity)
        
        if self.base_price is None or quantity is None:
            raise ValueError("Base price and quantity must be set before calculating the total price.")

        # Calculate additional prices based on neck type and sleeve length
        neck_type_price = NECK_TYPE_PRICES.get(self.neck_type, 0)
        sleeve_length_price = SLEEVE_LENGTH_PRICES.get(self.sleeve_length, 0)
        design_preference_price = DESIGN_PREFERENCES_PRICES.get(self.design_preference, 0)

        # Calculate total price
        total_price = (self.base_price + neck_type_price + sleeve_length_price + design_preference_price) * quantity

        return total_price
    
    def _validate_positive_float(self, value):
        """
        Validate that a value is a positive float.

        Parameters:
        - value: The value to validate.

        Returns:
        - float: The validated value.

        Raises:
        - ValueError: If the value is not a positive float.
        """
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Value must be a positive float.")
            return value
        except (ValueError, TypeError):
            raise ValueError("Invalid value. Must be a positive float.")

    def _validate_positive_integer(self, value):
        """
        Validate that a value is a positive integer.

        Parameters:
        - value: The value to validate.

        Returns:
        - int: The validated value.

        Raises:
        - ValueError: If the value is not a positive integer.
        """
        try:
            value = int(value)
            if value < 0:
                raise ValueError("Value must be a positive integer.")
            return value
        except (ValueError, TypeError):
            raise ValueError("Invalid value. Must be a positive integer.")
