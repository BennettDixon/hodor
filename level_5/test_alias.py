class TestAlias():
    """Class for use in CaptchaTests, used as an alias for the test
    """
    def __init__(self, alias):
        self.alias = alias

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        if not isinstance(value, str):
            raise TypeError("'TestAlias' alias must be a string")
        if not value.isupper():
            raise ValueError("'TestAlias' alias must be all uppercase")
        self.__alias = value
