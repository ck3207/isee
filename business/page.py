# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 11:23
# @Author  : chenkang19736
# @File    : login_page.py
# @Software: PyCharm

import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Time:
    SLEEP_TIME = 2


class HomepageDict:
    homepage_dict = {"first_level_page": ["标签管理", "个体画像", "客群画像", "应用管理", "报表管理",
                                          "权限管理", "客群营销", "API管理"],
                     "no_secondary_page": ["个体画像"],
                     "secondary_page": {"标签管理": ["标签查询", "标签审批", "数据字典", "标签开发", "标签审批状态"]}
                     }
    LABEL_MANAGE = ("标签管理", ("标签查询", "标签审批", "标签开发", "标签审批状态", "数据字典"))
    PERSONALITY_MANAGE = ("个体画像", )
    CUSTOMER_GROUP_MANAGE = "客群画像"
    APPLICATION_MANAGE = "应用管理"


class ScreenshotIndex:
    def __init__(self):
        self.screenshot_index = 0

    def get_screenshot(self):
        return self.__set_screenshot(self.screenshot_index)

    def __set_screenshot(self, screenshot_index):
        new_screenshot_index = screenshot_index + 1
        self.set_screenshot(new_screenshot_index)
        return str(screenshot_index)

    def set_screenshot(self, screenshot_index):
        self.screenshot_index = screenshot_index


class Page:
    def __init__(self, home_page):
        self.driver = webdriver.Chrome(executable_path="../config/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(url=home_page)
        self.driver.implicitly_wait(time_to_wait=3)
        self.prefix_file_save_path = "../static/"
        self.prefix_file_name = "screenshort_"

    def login(self, account, password):
        self.driver.find_element_by_name("account").send_keys(account)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_tag_name("button").click()

    def homepage(self, target_link, secondary_page):
        first_level_page = HomepageDict.homepage_dict.get("first_level_page")
        no_secondary_page = HomepageDict.homepage_dict.get("no_secondary_page")
        try:
            time.sleep(Time.SLEEP_TIME)
            if target_link in first_level_page:
                WebDriverWait(driver=self.driver, timeout=5).\
                    until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))\
                    [first_level_page.index(target_link)].click()
            else:
                raise "当前可操作的菜单栏为：{}".format(first_level_page)
            # 存在子菜单与不存在子菜单分别处理
            # if target_link in no_secondary_page:
            #     # elements = WebDriverWait(driver=self.driver, timeout=5).\
            #     #     until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-menu-item")))
            #     # elements = WebDriverWait(driver=self.driver, timeout=5).\
            #     #     until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))
            #     time.sleep(3)
            #     elements = self.driver.find_elements_by_tag_name("span")
            #     elements[no_secondary_page.index(target_link)].click()
            # elif target_link in first_level_page:
            #     WebDriverWait(driver=self.driver, timeout=5).\
            #         until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-submenu")))\
            #         [first_level_page.index(target_link)].click()
            # self.driver.find_elements_by_class_name("el-submenu")[first_level_page.index(target_link)].click()
        except Exception as e:
            # print(self.driver.page_source)
            print(str(e))

    def sencodary_page(self, name):
        screenshot_index = ScreenshotIndex()
        # 搜索
        WebDriverWait(driver=self.driver, timeout=5).\
            until(EC.presence_of_element_located((By.TAG_NAME, "input"))).send_keys("77")
        self.driver.find_element_by_class_name("el-input__suffix-inner").click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           screenshot_index.get_screenshot()))

        # 查看个体画像详情
        time.sleep(Time.SLEEP_TIME)
        # self.driver.find_elements_by_tag_name("button")[1].click()
        WebDriverWait(driver=self.driver, timeout=5).\
            until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, "button")))[1].click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           screenshot_index.get_screenshot()))
        time.sleep(Time.SLEEP_TIME)

        # 修改搜索条件
        self.driver.back()
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=self.driver, timeout=5).\
            until(EC.presence_of_element_located((By.CLASS_NAME, "mod-selected-conditions"))).click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           screenshot_index.get_screenshot()))

        # 用户信息基本类与交易属性类随意选择
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=self.driver, timeout=5).\
            until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-checkbox-button")))[random.randint(0, 19)].click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           screenshot_index.get_screenshot()))

        # 搜索
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=self.driver, timeout=5).\
            until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))[1].click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           screenshot_index.get_screenshot()))

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()



if __name__ == "__main__":
    page = Page(home_page="http://127.0.0.1/h5-isee-manage/#/login")
    page.login(account="1", password="2")
    page.homepage("个体画像", None)
    page.sencodary_page(name="name")
    # page.homepage("标签管理", None)
    time.sleep(100)
    page.quit()