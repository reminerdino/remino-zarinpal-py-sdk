class Fillable:
    """
    Mixin class that provides the functionality of the PHP trait Fillable.
    """

    def __init__(self, inputs: dict[str, str] | None = None) -> None:
        """
        Constructor that optionally fills the instance with given inputs.

        :param inputs: Optional dictionary of inputs to set as instance attributes.
        """
        if inputs is not None:
            self.fill(inputs)

    def fill(self, inputs: dict[str, str]) -> 'Fillable':
        """
        Fills the instance's attributes with values from the inputs dictionary.

        :param inputs: A dictionary of attributes to set on the instance.
        :return: The current instance (for method chaining).
        """
        for key, value in inputs.items():
            if self.__isset(key):
                setattr(self, key, value)
        return self

    def __isset(self, name: str) -> bool:
        """
        Checks if the given property exists in the instance.

        :param name: The name of the property to check.
        :return: True if the property exists, otherwise False.
        """
        return hasattr(self, name)

    def __getattr__(self, name: str) -> str:
        """
        Gets the value of the given attribute.

        :param name: The name of the attribute to get.
        :return: The value of the attribute.
        """
        if self.__isset(name):
            return getattr(self, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: str) -> None:
        """
        Sets the value of the given attribute.

        :param name: The name of the attribute to set.
        :param value: The value to set for the attribute.
        """
        super().__setattr__(name, value)
