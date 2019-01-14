class TestAlias():
    """Class for use in CaptchaTests, used as an alias for the test
    """
    def __init__(self, alias):
        self.alias = alias
        self.__tests_ran = 0

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

    @property
    def tests_ran(self):
        return self.__tests_ran

    def increment_tests_ran(self):
        self.__tests_ran += 1
