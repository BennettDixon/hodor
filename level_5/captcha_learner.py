#!/usr/bin/python3
"""
module for use with getting captcha data.
customize learner for use with different captchas.
"""
import pytesseract
import cv2
from captcha_test import CaptchaTest
from test_alias import TestAlias


class CaptchaLearner():
    """CaptchaLearner class. create one and use over course of ->
        program. It will learn as it progresses to create better ->
        results.
    """
    temp_file_name = 'captcha.png'

    def __init__(self):
        self.__test_cases = []
        self.__test_cases.append(CaptchaTest())
        self.__current_test = self.__test_cases[0]
        self.__prev_test = None
        self.__best_test = None

    @property
    def best_test(self):
        return self.__best_test

    @property
    def current_test(self):
        return self.__current_test

    def test_fail(self):
        """increments current test's failure
        """
        self.__current_test.increment_failure()

    def test_success(self):
        """increments current test's success
        """
        self.__current_test.increment_success()

    @property
    def test_cases(self):
        return self.__test_cases

    def get_iterations(self):
        """gets the amount of iterations learner has been through
        """
        iterations = 0
        for test in self.__test_cases:
            iterations += (test.current_i + 1)
        return iterations
    def get_captcha(self):
        """pulls captcha value from url that points to an image
        """
        self.__current_test.increment_index()
        test = self.__current_test
        prev_test = self.__prev_test
        # reached end of test, or test is failing severely
        if test.current_i >= (test.iterations_per_test) or\
        (prev_test is not None and\
        (test.current_i > test.iterations_per_test / 10 and\
        (self.is_worse_test(test)))):
            self.set_new_test()
        img = cv2.imread(self.temp_file_name)
        img = cv2.medianBlur(img, test.blur_factor)
        cv2.threshold(img, test.base_thresh, 255, cv2.THRESH_BINARY)
        
        if self.__current_test.current_i % 10 == 0:
            print("posted {} requests in test with success rate {}".format(self.__current_test.current_i, self.__current_test.get_success_rate()))
        return pytesseract.image_to_string(img)

    def set_new_test(self):
        """sets a new test based on:
            current and previous's success rate
            whether it was an increase or decrease to filter setting
            which filter setting was effected
            how many times a filter setting has been effected
        """
        test_flip = CaptchaTest.iterations_per_test * 10
        iterations = self.get_iterations()
        print("set_new_test got iterations: {}".format(iterations))

        blur_change = 2
        thresh_change = 1
        test = self.__current_test
        
        if (test.test_alias is None or iterations < test_flip) and not\
            self.constant_failure("BLUR"):
            new_alias = TestAlias("BLUR")
            if test.blur_factor > 255 - blur_change:
                test.blur_factor = 255 - blur_change
            elif test.blur_factor % 2 == 0:
                test.blur_factor + 1
            new_test = CaptchaTest(test.blur_factor + blur_change,\
            test.base_thresh, new_alias)
        elif iterations < test_flip * 2 and not self.constant_failure("THRESH"):
            if test.test_alias.alias == "BLUR":
                print("switching testing type grabbing best value for blur")
                best_blur = self.get_best_test("BLUR")
                self.__current_test.blur_factor = best_blur.blur_factor
            new_alias = TestAlias("THRESH")
            if test.base_thresh > 255 - thresh_change:
                test.base_thresh = 255 - thresh_change
            new_test = CaptchaTest(test.blur_factor, test.base_thresh + thresh_change, new_alias)
        else:
            print("testing done, finding optimal test")
            best_thresh = self.get_best_test("THRESH")
            best_blur = self.get_best_test("BLUR")
            if best_thresh is None or best_blur is None:
                if best_thresh is None:
                    self.__best_test = best_blur
                elif best_blur is None:
                    self.__best_test = best_thresh
                else:
                    raise Exception("Both tests failed all cases with 0 success rates. Exiting.")
                return
            best_thresh.blur_factor = best_blur.blur_factor
            self.__best_test = best_thresh
            return
        self.__test_cases.append(new_test)
        self.__prev_test = test
        self.__current_test = new_test
        print("set new test: {}".format(self.__current_test))

    def get_best_test(self, alias):
        """gets the best test from current tests given an alias
        """
        best_rate = 0
        best_test = None
        if not isinstance(alias, str):
            raise TypeError("'CaptchaLearner' get_best_test() alias must be str type")
        for test in self.__test_cases:
            if test.test_alias.alias == alias and test.get_success_rate() > best_rate:
                best_test = test
                best_rate = test.get_success_rate()
        return best_test

    def constant_failure(self, alias):
        """checks if an alias has failed more than x times in a row
        """
        bottom_rate = 0.1
        failure_max = 3
        if not isinstance(alias, str):
            raise TypeError("'CaptchaLearner' constant_failure() alias must be str type")
        failures = []
        for test in self.__test_cases:
            if test.test_alias.alias == alias and\
            test.get_success_rate() < bottom_rate:
                failures.append(test)
                if len(failures) >= failure_max:
                    return True

    def is_worse_test(self, test):
        """checks if a test is going worse than previous tests by
            large factor.
            Returns true if it is,
            False if not.
        """
        if not isinstance(test, CaptchaTest):
            raise TypeError("'CaptchaLearner' is_worse_test() test value must be of CaptchaTest type")
        if test.current_i < test.iterations_per_test / 10:
            return False # not enough data points yet
        success_rate = test.get_success_rate()
        if success_rate == 0:
            return True
        for test_in_list in self.__test_cases:
            if test_in_list.get_success_rate() > success_rate + 0.2:
                return True
        return False

    def write_tests(self, filename):
        """writes tests to a file for learner instance
        """
        builder = ""
        f = open(filename, "w")

        for test in self.__test_cases:
            builder += repr(test) + '\n'
            builder += "Success Rate: " + str(round(test.get_success_rate(), 3))
            builder += " %\n"
        f.write(builder)
        f.close()
