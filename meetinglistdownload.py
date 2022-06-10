import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from login_settings import USER, PW


class MeetingListDownload:

    def __init__(self,INST_ID):
        self.INST_ID = INST_ID

    def meeting_list_download(self):
        path = "C:/Users/bpaur/PycharmProjects/webscrap"
        os.chdir(path)

        # establishes web driver
        driver = webdriver.Chrome()
        driver.get("https://sso.net.broadridge.com/cc/proxyedgelogin.do?TYPE=33554433&REALMOID=06-8d1b7c2a-dae5-4a69-a746-d70fe0bef606&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=65422_proxyedge&TARGET=$SM$HTTPS%3a%2f%2fcentral%2eproxyedge%2ecom%2fPEWeb")
        driver.maximize_window()
        # checks website to make sure the title is the pe title page
        # assert "Broadridge - ProxyEdge" in driver.title

        # enters username
        email_elem = driver.find_element(by=By.NAME, value="USER")
        email_elem.clear()
        email_elem.send_keys(USER)

        # enters pw
        pw_elem = driver.find_element(by=By.NAME, value="PASSWORD")
        pw_elem.clear()
        pw_elem.send_keys(PW)
        pw_elem.send_keys(Keys.RETURN)

        # enters int id
        int_id_elem = driver.find_element(by=By.NAME, value="instId")
        int_id_elem.clear()
        int_id_elem.send_keys(self.INST_ID)
        int_id_elem.send_keys(Keys.RETURN)

        # dropdown
        driver.implicitly_wait(20)
        dropdown = driver.find_element(by=By.XPATH, value="/html/body/div/div/nav/div/div[2]/ul[1]/li[2]/a")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()

        # meeting list
        meeting_list = driver.find_element(by=By.XPATH,
                                           value="/html/body/div/div/nav/div/div[2]/ul[1]/li[2]/ul/li[1]/a")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(meeting_list).click(meeting_list).perform()
        driver.implicitly_wait(20)

        # Display Sets Dropdown
        display_dropdown = driver.find_element(by=By.XPATH,
                                               value="/html/body/div[3]/div/div[5]/div[1]/div[2]/div/button/span[1]")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(display_dropdown).click(display_dropdown).perform()

        # Display Sets Press
        display_press = driver.find_element(by=By.XPATH,
                                            value="/html/body/div[3]/div/div[5]/div[1]/div[2]/div/div/ul/li/a/span[1]")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(display_press).click(display_press).perform()

        # waits for new columns to be clickable
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[5]/div[2]/div[2]/div/div[3]/div[1]/div/div[13]/div/div[1]")))

        # meeting list dropdown
        meeting_list_dropdown = driver.find_element(by=By.XPATH,
                                                    value="/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/button")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(meeting_list_dropdown).click(meeting_list_dropdown).perform()

        # download to csv
        download_csv = driver.find_element(by=By.XPATH,
                                           value="/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div/ul/li[3]/a/span[1]")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(download_csv).click(download_csv).perform()

        # needed to complete download
        time.sleep(1)
