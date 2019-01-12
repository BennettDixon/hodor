#!/usr/bin/python3
"""
module for use with getting captcha data.
customize learner for use with different captchas.
"""
import pytesseract
import cv2

class CaptchaLearner():
    """CaptchaLearner class. create one and use over course of ->
        program. It will learn as it progresses to create better ->
        results.
    """
    temp_file_name = 'captcha.png'

    def __init__(self, start_blur=3, start_thresh=40):
        """insatiates class instance
        """
        self.blur_factor = start_blur
        self.base_thresh = start_thresh

    @property
    def blur_factor(self):
        return self.__blur_factor

    @blur_factor.setter
    def blur_factor(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("'CaptchaLearner': start_blur must be int or float")
        elif value <= 0:
            raise ValueError("'CaptchaLearner': start_blur must be > 0")
        self.__blur_factor = value

    @property
    def base_thresh(self):
        return self.__base_thresh

    @base_thresh.setter
    def base_thresh(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("'CaptchaLearner': start_blur must be int or float")
        elif value <= 0:
            raise ValueError("'CaptchaLearner': start_blur must be > 0")
        self.__base_thresh = value

    def get_captcha(self):
        """pulls captcha value from url that points to an image
        """
        img = cv2.imread(self.temp_file_name)
        img = cv2.medianBlur(img, 3)
        cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
        return pytesseract.image_to_string(img)
