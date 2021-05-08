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
from selenium.webdriver.common.action_chains import ActionChains

from isee.public import logging

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
        new_screenshot_index = self.screenshot_index + 1
        self.set_screenshot(new_screenshot_index)
        return str(self.screenshot_index)

    def set_screenshot(self, screenshot_index):
        self.screenshot_index = screenshot_index


class Page:
    def __init__(self, home_page):
        self.driver = webdriver.Chrome(executable_path="../config/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(url=home_page)
        # self.driver.implicitly_wait(time_to_wait=3)
        self.prefix_file_save_path = "../static/"
        self.prefix_file_name = "screenshort_"
        self.screenshot_index = ScreenshotIndex()

    def login(self, account, password):
        self.driver.find_element_by_name("account").send_keys(account)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_tag_name("button").click()

    def get_page(self, url):
        time.sleep(Time.SLEEP_TIME)
        self.driver.get(url=url)
        time.sleep(Time.SLEEP_TIME)
        return self.driver

    def homepage(self, driver=None, name="首页"):
        """登录后，进入的主页面"""
        self.screenshot_index = ScreenshotIndex()
        if not driver:
            driver = self.driver
        first_level_page = HomepageDict.homepage_dict.get("first_level_page")
        no_secondary_page = HomepageDict.homepage_dict.get("no_secondary_page")
        time.sleep(Time.SLEEP_TIME)
        for i, element in enumerate(WebDriverWait(driver=driver, timeout=5). \
                               until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))[:8]):
            first_level_page_name = HomepageDict.homepage_dict.get("first_level_page")[i]
            logging.info("Operator Menu: {}".format(first_level_page_name))
            ActionChains(driver).move_to_element(to_element=element).perform()
            time.sleep(Time.SLEEP_TIME)

            # 一级菜单选中状态
            sub_elements = driver.find_elements_by_class_name("el-menu--horizontal")
            for sub_element in sub_elements:
                elment_style = sub_element.get_attribute("style")
                logging.info("The ClassName[el-menu--horizontal]'s Style Attribute Is: {}".format(elment_style))
                # 判断一级菜单是否选中
                if elment_style.strip() != "" and "display: none" not in elment_style:
                    # 选中后，轮询点击此一级菜单下的所有二级菜单
                    for click_element in sub_element.find_elements_by_class_name("el-menu-item"):
                        try:
                            ActionChains(driver).click(on_element=click_element).perform()
                            time.sleep(Time.SLEEP_TIME)
                            sencondary_page_name = driver.find_elements_by_class_name("no-redirect")[-1].text
                            # 命名格式： {路径}{一级菜单名}-{二级菜单名}-{图片序号}.png
                            driver.save_screenshot("{0}{1}-{2}-{3}.png".format(self.prefix_file_save_path,
                                                                                  first_level_page_name,
                                                                                  sencondary_page_name,
                                                                                  self.screenshot_index.get_screenshot()))
                            ActionChains(driver).move_to_element(to_element=element).perform()
                            logging.info("Get Into Secondary Menu: {}".format(sencondary_page_name))
                            time.sleep(0.5)
                        except Exception as e:
                            logging.error("二级菜单跳转出错：{}-{}".format(first_level_page, sencondary_page_name))
                            logging.error(str(e))

    def sencodary_page(self, driver, name):
        """主页面可以点击进入的二级页面"""
        self.screenshot_index = ScreenshotIndex()

        time.sleep(Time.SLEEP_TIME)
        elements = WebDriverWait(driver=driver, timeout=5). \
            until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "el-menu-item")))
        time.sleep(Time.SLEEP_TIME)
        for element in elements:
            element.click()
            driver.save_screenshot("{3}{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                          self.screenshot_index.get_screenshot(), name))
            time.sleep(Time.SLEEP_TIME)

    def personality_sencondary_page(self, driver, name):
        self.screenshot_index = ScreenshotIndex()
        # 搜索
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_element_located((By.TAG_NAME, "input"))).send_keys("77")
        driver.find_element_by_class_name("el-input__suffix-inner").click()
        driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           self.screenshot_index.get_screenshot()))

        # 查看个体画像详情
        time.sleep(Time.SLEEP_TIME)
        # self.driver.find_elements_by_tag_name("button")[1].click()
        WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, "button")))[1].click()
        self.driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           self.screenshot_index.get_screenshot()))
        time.sleep(Time.SLEEP_TIME)

        # 修改搜索条件
        driver.back()
        # time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_element_located((By.CLASS_NAME, "mod-selected-conditions"))).click()
        driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           self.screenshot_index.get_screenshot()))

        # 用户信息基本类与交易属性类随意选择
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-checkbox-button")))[random.randint(0, 10)].click()
        driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           self.screenshot_index.get_screenshot()))

        # 搜索
        time.sleep(Time.SLEEP_TIME)
        WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))[1].click()
        driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                           self.screenshot_index.get_screenshot()))

        # 搜索结果分页
        time.sleep(Time.SLEEP_TIME)
        num = driver.find_element_by_class_name("num").text
        elements = WebDriverWait(driver=driver, timeout=5).\
            until(EC.presence_of_all_elements_located((By.CLASS_NAME, "number")))
        # 分页大于1页

        if num > "10":
            # 随机点击分页
            elements[random.randint(1, len(elements))].click()
            driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                               self.screenshot_index.get_screenshot()))

            # 点击上一页
            WebDriverWait(driver=driver, timeout=5). \
                until(EC.presence_of_element_located((By.CLASS_NAME, "btn-prev"))).click()
            driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                               self.screenshot_index.get_screenshot()))

            # 点击下一页
            WebDriverWait(driver=driver, timeout=5). \
                until(EC.presence_of_element_located((By.CLASS_NAME, "btn-next"))).click()
            driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                               self.screenshot_index.get_screenshot()))
        else:
            driver.save_screenshot("{0}{1}{2}.png".format(self.prefix_file_save_path, self.prefix_file_name,
                                                               self.screenshot_index.get_screenshot()))

    def close(self):
        self.driver.close()

    def quit(self, driver=None):
        if not driver:
            self.driver.quit()
        else:
            driver.quit()



if __name__ == "__main__":
    page = Page(home_page="http://127.0.0.1//h5-isee-manage/#/login")
    page.login(account="1", password="2")
    # page.homepage("个体画像", None)
    # personality_page_driver = page.get_page(url="http://dmp.winner123.cn/h5-isee-manage/#/individualPicture/userSelect")
    # page.personality_sencondary_page(driver=personality_page_driver, name="个体画像")
    # page.quit(driver=personality_page_driver)

    homepage_driver = page.get_page(url="http://127.0.0.1/h5-isee-manage/#/home")
    # page.sencodary_page(driver=homepage_driver, name="首页点击事件")
    page.homepage(driver=homepage_driver, name="首页")
    time.sleep(30)
    page.quit(driver=homepage_driver)
    page.quit()