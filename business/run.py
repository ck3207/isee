# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 11:21
# @Author  : chenkang19736
# @File    : run.py
# @Software: PyCharm

class ScreenshotIndex:
    def __init__(self):
        self.screenshot_index = 0

    def get_screenshot(self):
        return self.__set_screenshot(self.screenshot_index)

    def __set_screenshot(self, screenshot_index):
        new_screenshot_index = screenshot_index + 1
        self.set_screenshot(new_screenshot_index)
        return screenshot_index

    def set_screenshot(self, screenshot_index):
        self.screenshot_index = screenshot_index

if __name__ == "__main__":
    s = ScreenshotIndex()
    count = 10
    while count:
        print(s.get_screenshot())
        count -= 1
