import time
import re

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebElement


class Browser(webdriver.Chrome):
    def __init__(self):
        super().__init__()
        self.default_wait_time = 10
        self.by = By

    def wait_and_locate_element(self, by, element, wait_time=None) -> WebElement:
        if wait_time is None:
            wait_time = self.default_wait_time

        wait = WebDriverWait(self, wait_time)
        return wait.until(ec.presence_of_element_located((by, element)))

    def element(self, by, element, wait_time=None):
        located_element = self.wait_and_locate_element(by, element, wait_time)
        return self.find_element(located_element)

    def element_text(self, by, element, wait_time=None):
        located_element = self.wait_and_locate_element(by, element, wait_time)
        return located_element.text

    def element_exists(self, by, element, wait_time=None):
        try:
            self.wait_and_locate_element(by, element, wait_time)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False
        except selenium.common.exceptions.TimeoutException:
            return False

    def click(self, by, element, wait_time=None):
        located_element = self.wait_and_locate_element(by, element, wait_time)
        ActionChains(self).click(located_element).perform()
        time.sleep(0.5)

    def select(self, by, element, text):
        select = Select(self.find_element(by, element))
        select.select_by_visible_text(text)

    def select_by_index(self, by, element, index):
        select = Select(self.find_element(by, element))
        select.select_by_index(index)

    def select_ul_by_value(self, by, element, value):
        if self.element_exists(by, element):
            element = self.wait_and_locate_element(by, element)
            li_items = element.find_elements(By.TAG_NAME, 'li')
            for li in li_items:
                if li.text == value:
                    li.click()

    def get_select_options(self, by, element):
        select = Select(self.find_element(by, element))
        return select.options

    def send_keys(self, by, element, keys, wait_time=None, clear_first=False, enter=False):
        self.click(by, element, wait_time)
        if clear_first:
            self.find_element(by, element).clear()
        if enter:
            self.find_element(by, element).send_keys(keys)
            time.sleep(1)
            self.find_element(by, element).send_keys(Keys.ENTER)
        else:
            self.find_element(by, element).send_keys(keys)

    def clear_field(self, by, element, wait_time=None):
        located_element = self.wait_and_locate_element(by, element, wait_time)
        self.click(by, element, wait_time)
        located_element.clear()

    def text_on_page(self, text):
        if text in self.page_source:
            return True
        else:
            src = self.page_source
            text_found = re.search(fr"{text}", src)
            return text_found

    def switch_tab(self, page_index: int):
        child = self.window_handles[page_index]
        self.switch_to.window(child)
