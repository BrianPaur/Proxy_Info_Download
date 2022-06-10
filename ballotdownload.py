import os
from os.path import exists
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from login_settings import USER, PW
import pandas as pd
import logging
from datetime import datetime


class MeetingBallotDownload:
    def __init__(self, institutionID,originaldir,newdir,comp_list=[],dataframe='placeholder'):
        self.institutionID = institutionID
        self.originaldir = originaldir
        self.newdir = newdir
        self.comp_list = comp_list
        self.dataframe = dataframe

    def logger(self):
        if os.path.exists(f"{self.newdir}logs/") == False:
            os.mkdir(f"{self.newdir}logs/")
            os.chdir(f"{self.newdir}logs/")
        else:
            os.chdir(f"{self.newdir}logs/")

    def comp_name_to_list(self):
        df = pd.read_csv(f'{self.newdir}{self.institutionID}.csv', delimiter=',')
        df = df.iloc[:, 0].str.strip()
        self.comp_list = list(set(df.tolist()))
        return self.comp_list

    def data_frames(self):
        df = pd.read_csv(f'{self.newdir}{self.institutionID}.csv', delimiter=',')
        df1 = df.iloc[:, 0].str.strip()
        df1 = df1.str.title()
        df2 = df.iloc[:, 2].str.strip()
        df3 = df.iloc[:, 8].str.strip()
        frames = [df1, df2, df3]
        self.dataframe = pd.concat(frames, axis=1, join='inner')
        return self.dataframe

    def meeting_ballot_download(self):

        for i in self.comp_list:

            if exists(f"{self.newdir}{i}/{i.title()}_ballot_page.xls") == False:

                try:
                    #needed to establish web driver
                    path = "C:/Users/bpaur/PycharmProjects/webscrap"
                    os.chdir(path)

                    #establishes web driver
                    driver = webdriver.Chrome()
                    driver.get("https://sso.net.broadridge.com/cc/proxyedgelogin.do?TYPE=33554433&REALMOID=06-8d1b7c2a-dae5-4a69-a746-d70fe0bef606&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=65422_proxyedge&TARGET=$SM$HTTPS%3a%2f%2fcentral%2eproxyedge%2ecom%2fPEWeb")
                    driver.maximize_window()
                    #checks website to make sure the title is the pe title page
                    assert "Broadridge - ProxyEdge" in driver.title

                    #enters username
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
                    int_id_elem.send_keys(self.institutionID)
                    int_id_elem.send_keys(Keys.RETURN)

                    #dropdown
                    dropdown = driver.find_element(by=By.XPATH,value="/html/body/div/div/nav/div/div[2]/ul[1]/li[2]/a")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()

                    #meeting list
                    meeting_list = driver.find_element(by=By.XPATH,value="/html/body/div/div/nav/div/div[2]/ul[1]/li[2]/ul/li[1]/a")
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
                    driver.implicitly_wait(20)

                    #search
                    search_icon = driver.find_element(by=By.XPATH,value="/html/body/div[3]/div/div[5]/div[1]/div[1]/button[1]/span")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(search_icon).click(search_icon).perform()

                    driver.implicitly_wait(20)

                    #search for company
                    comp_isin_loc = self.dataframe.loc[self.dataframe['\tCompany Name'] == i.title()].index.values
                    comp_isin = self.dataframe['\tISIN'].values[comp_isin_loc]

                    comp_name_search = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div/div[2]/div/div[2]/form/div[3]/input")
                    comp_name_search.clear()
                    comp_name_search.send_keys(comp_isin)
                    driver.implicitly_wait(20)
                    comp_name_search.send_keys(Keys.RETURN)

                    time.sleep(3)

                    #find meeting
                    meeting = driver.find_element(by=By.XPATH,value="/html/body/div[3]/div/div[5]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div[2]/div/a")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(meeting).click(meeting).perform()

                    #get to print ballot page
                    ballot = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div[6]/div[2]/div[1]/button[8]")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(ballot).click(ballot).perform()
                    time.sleep(1)

                    #handles new window pop up
                    new_window = driver.window_handles[1]
                    driver.switch_to.window(new_window)

                    #print the ballot page
                    print_ballot_page = driver.find_element(by=By.XPATH,value="//button[@id='exportExcel']")
                    driver.implicitly_wait(10)
                    ActionChains(driver).move_to_element(print_ballot_page).click(print_ballot_page).perform()
                    time.sleep(1)

                    #rename file that was downloaded

                    os.chdir(self.originaldir)
                    list_of_files = glob.glob(f"{self.originaldir}*xls")
                    latest_download = max(list_of_files, key=os.path.getctime)
                    os.renames(latest_download, f'{i.title()}_ballot_page.xls')

                    ##########################################################################################
                    #### moves files #########################################################################
                    ##########################################################################################

                    os.chdir(self.originaldir)
                    os.replace(f"{self.originaldir}{i.title()}_ballot_page.xls",
                               f"{self.newdir}{i.title()}/{i.title()}_ballot_page.xls")

                    print(f'---------{i.title()} successfully saved down---------')

                    ##########################################################################################
                    #### log files ###########################################################################
                    ##########################################################################################

                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_ballot_download.log",encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}---------{i.title()} successfully saved down---------")

                except:
                    print(f"unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")
                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_ballot_download.log",encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")

            else:
                print(f"||||{i} already exists||||")
                os.chdir(f"{self.newdir}logs/")
                logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_ballot_download.log",encoding='utf-8', level=logging.INFO)
                logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}||||{i} already exists||||")