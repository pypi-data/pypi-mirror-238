import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import numpy as np
from typing import Union
from colorama import Fore, init
from .check_func import CheckValue
from .take_file import FileNameT

class StartLoad(CheckValue):
    def __init__(self, logs: bool = False):
        self.logs = logs
        init()


    def load_file_a(self, url_list: list, count: int, save_dir: str):
        """
        :param url_list: list from the url where you need to download files
        :param count: number of open browsers
        :param save_dir: The folder where the files will be saved
        :return:
        """
        self.count = self._check_count(count)
        self.save_dir = self._check_dir(save_dir)
        url_list = self.__made_url(np.array(url_list), self.count)
        t_list = []
        driver_list = []
        for urls in url_list:
            driver = self.__create_driver()
            driver_list.append(driver)
            t_list.append(threading.Thread(target=self.__collecting, args=(urls, driver)))

        for t_start in t_list:
            t_start.start()
        for t_join in t_list:
            t_join.join()
        for dr in driver_list:
            try:
                dr.quit()
            except:
                pass


    def load_file_s(self, url: str, save_dir: str):
        """
        :param url: url
        :param save_dir: The folder where the files will be saved
        :return:
        """
        self.save_dir = self._check_dir(save_dir)
        url = self._check_url(url)
        driver = self.__create_driver()
        self.__load(url, driver)
        try:
            driver.quit()
        except:
            pass

    def __print_log(self, text: str, color: Fore):
        if self.logs:
            print(color + text)

    @staticmethod
    def load_is_ready(save_dir: str, file_name: str):
        for i in range(10):
            time.sleep(1)
            all_file = os.listdir(save_dir)
            if all_file.count(file_name + ".ipynb"):
                break

    @staticmethod
    def __made_url(urls: np.array, c) -> list:
        if c != 1:
            try:
                new_urls = urls.reshape(-1, (len(urls) // c))
                new_urls = new_urls.tolist()
                return new_urls
            except:
                lost_url = list(i for i in urls[:len(urls)%5])
                urls = urls[len(urls)%5:]
                new_urls = urls.reshape(-1, (len(urls) // c))
                # new_urls = np.append(new_urls, [lost_url])
                new_urls = new_urls.tolist()
                new_urls.append(lost_url)
                return new_urls
        else:
            return urls

    def __create_driver(self):
        save_dir = self.save_dir
        abs_path = os.path.abspath(save_dir)
        option = webdriver.ChromeOptions()
        prefs = {"download.default_directory": f"{abs_path}", 'profile.default_content_setting_values.automatic_downloads': 1}
        option.add_experimental_option("prefs", prefs)
        option.add_argument("headless")
        return webdriver.Chrome(options=option)

    def __collecting(self, urls: Union[str, list], driver: webdriver):
        if isinstance(urls, list):
            try:
                for url in urls:
                    try:
                        self._check_url(url)
                    except Exception as e:
                        print(e)
                    self.__load(url, driver)
            except Exception as e:
                raise e
        elif isinstance(urls, str):
            self.__load(urls, driver)
        else:
            raise TypeError("urls is not list or str")


    def __load(self, url, driver: webdriver):
        save_dir = self.save_dir
        try:
            file_name_t = FileNameT(url)
            file_name_t.start()
            driver.get(url)

            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#file-menu-button'))).click()
                wait = WebDriverWait(driver, 20)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#download-submenu-menu-button'))).click()
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#\:l'))).click()
                file_name_t.join()
                if not file_name_t.file_name:
                    self.__print_log(f"No access - {url}", color=Fore.RED)
                    return f"No access - {url}"
            except:
                try:
                    wait = WebDriverWait(driver, 30)
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#file-menu-button'))).click()
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#download-submenu-menu-button'))).click()
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#\:l'))).click()
                    file_name_t.join()
                    if not file_name_t.file_name:
                        self.__print_log(f"No access - {url}", color=Fore.RED)
                    return f"No access - {url}"
                except:
                    self.__print_log(f"No access - {url}", color=Fore.RED)
                    return f"No access - {url}"

            self.load_is_ready(save_dir, file_name_t.file_name)

            self.__print_log(f"File save to - {save_dir}/{file_name_t.file_name}", color=Fore.GREEN)
            return f"File save to - {save_dir}/{file_name_t.file_name}"
        except Exception as e:
            try:
                file_name_t.join()
            except:
                pass
            raise e



