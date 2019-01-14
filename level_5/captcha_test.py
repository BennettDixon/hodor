#!/usr/bin/python3


from test_alias import TestAlias
class CaptchaTest():
    """class for use in CaptchaLearner objects.
    holds data about the test
    """
    iterations_per_test = 100

    def __init__(self, start_blur=1, start_thresh=5, test_alias=None):
        """insatiates class instance
        """
        self.blur_factor = start_blur
        self.base_thresh = start_thresh
        if test_alias is None:
            self.test_alias = TestAlias("BLUR")
        else:
            self.test_alias = test_alias
        self.__failure = 0
        self.__success = 0
        self.__current_i = 0

    def __str__(self):
        """custom method for use with print and str on captchatest objejcts
        """
        string = ""
        string += "TestAlias:"
        string += self.test_alias.alias + '\n'
        string += "blur_factor:"
        string += str(self.blur_factor) + '\n'
        string += "base_thresh:"
        string += str(self.base_thresh) + '\n'
        return string

    def get_success_rate(self):
        """gets the current success rate
        """
        if self.current_i == 0:
            return 0
        return float(self.success / self.current_i)

    @property
    def success(self):
        return self.__success

    def increment_success(self):
        self.__success += 1

    @property
    def failure(self):
        return self.__failure

    def increment_failure(self):
        self.__failure += 1

    @property
    def current_i(self):
        return self.__current_i

    def increment_index(self):
        self.__current_i += 1

    @property
    def test_alias(self):
        return self.__test_alias

    @test_alias.setter
    def test_alias(self, value):
        if not isinstance(value, TestAlias):
            raise TypeError("'CaptchaTest' test_alias must be of TestAlias type")
        self.__test_alias = value

    @property
    def blur_factor(self):
        return self.__blur_factor

    @blur_factor.setter
    def blur_factor(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("'CaptchaTest': blur_factor must be int or float")
        elif value <= 0:
            raise ValueError("'CaptchaTest': blur_factor must be > 0")
        self.__blur_factor = value

    @property
    def base_thresh(self):
        return self.__base_thresh

    @base_thresh.setter
    def base_thresh(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("'CaptchaTest': base_thresh must be int or float")
        elif value <= 0:
            raise ValueError("'CaptchaTest': base_thresh must be > 0")
        self.__base_thresh = value
