#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import const


class YoyakuAPI:
    def __init__(self):
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument("start-maximized")
        self.__options.add_argument("disable-infobars")
        self.__options.add_argument("--disable-extensions")
        self.__options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.__driver = driver = webdriver.Chrome(chrome_options=self.__options,
                                                  executable_path=ChromeDriverManager().install())

    # product_data = []
    def yoyakuLogin(self):
        try:
            self.__driver.get(const.URL)
            self.__driver.maximize_window()

            ### login -start- ###
            # check box
            check_box = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.NAME, 'prio_tgt')))
            self.__driver.execute_script("arguments[0].click();", check_box)

            # input ID/PASS
            id = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'login_id')))
            id.send_keys(const.ID)
            password = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'login_pwd')))
            password.send_keys(const.PASWD)

            # login button click
            login_button = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'btn_login')))
            self.__driver.execute_script("arguments[0].click();", login_button)
            ### log in - end - ###

            # click yoyaku link
            yoyaku_link = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mypage_accept"]/a')))
            self.__driver.execute_script("arguments[0].click();", yoyaku_link)

            # click place check btn
            WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'btn_Search_Medical'))).click()

            ### 接種会場を検索 -start- ###

            # time.sleep(1)
            # basyou = self.__driver.find_element_by_id(
            #     "medical_institution_name")
            # basyou.send_keys(const.BASYOU)

            # click place check btn
            time.sleep(1) # wait to avalible click
            pop_basyo_button = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'btn_search_medical')))
            pop_basyo_button.click()

            # check search result
            cnt = WebDriverWait(self.__driver, const.DELAY).until(EC.visibility_of_element_located((By.ID, 'count_all'))).text

            while True:
                if cnt == '0件':
                    pop_basyo_button.click()
                    cnt = WebDriverWait(self.__driver, const.DELAY).until(EC.visibility_of_element_located((By.ID, 'count_all'))).text
                elif cnt != '0件':
                    break
            ### 接種会場を検索 -end- ###

            ## 接種会場を予約 - start - ###
            # select place
            basyou_select = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'search_medical_table_radio_1')))
            basyou_select.click()

            basyou_select_button = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.ID, 'btn_select_medical')))
            basyou_select_button.click()

            # date select
            date_select = WebDriverWait(self.__driver, const.DELAY).until(EC.presence_of_element_located((By.XPATH, '//*[@data-date="{0}"]'.format(const.DATE))))
            date_select.click()

            while True:
                try:
                    WebDriverWait(self.__driver, 2).until(EC.alert_is_present(),
                                                          'Timed out waiting for PA creation ' +
                                                          'confirmation popup to appear.')

                    alert = self.__driver.switch_to.alert
                    print(alert.text)
                    alert.accept()

                    time.sleep(1)
                    date_select.click()
                except TimeoutException:
                    break

            # 接種会場を予約 - end - ###

        except Exception as e:
            print('error: ', e)

        # self.__driver.close()


if __name__ == '__main__':
    yoyakuAPI = YoyakuAPI()
    yoyakuAPI.yoyakuLogin()
