import os
from os.path import exists
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from login_settings import USER, PW , GL_PW, GL_USER
import pandas as pd
import logging
from datetime import datetime
import shutil



class GlassLewis:

    def __init__(self, originaldir, newdir, filename, isin_list = [], dataframe = []):
        self.originaldir = originaldir
        self.newdir = newdir
        self.filename = filename
        self.isin_list = isin_list
        self.dataframe = dataframe

    def logger(self):
        if os.path.exists(f"{self.newdir}logs/") == False:
            os.mkdir(f"{self.newdir}logs/")
            os.chdir(f"{self.newdir}logs/")
        else:
            os.chdir(f"{self.newdir}logs/")

    def ISIN_to_list(self):
        # read csv to create list of ISINs
        file_path = (self.newdir + self.filename)
        df = pd.read_csv(file_path, delimiter=',')
        df = df.iloc[:, 2].str.strip()
        self.isin_list = list(set(df.tolist()))
        return self.isin_list

    def data_frames(self):
        # creates dataframe that we can reference when naming files
        # csv file is too hard to parse because of formatting so this is a cleaner solution

        file_path = (self.newdir + self.filename)
        df = pd.read_csv(file_path, delimiter=',')
        df1 = df.iloc[:, 0].str.strip()
        df1 = df1.str.title()
        df2 = df.iloc[:, 2].str.strip()
        df3 = df.iloc[:, 8].str.strip()
        frames = [df1, df2, df3]
        self.dataframe = pd.concat(frames, axis=1, join='inner')
        return self.dataframe

    def pull_down_reports(self):

        ##########################################################################################
        #### Logs into Glass Lewis ###############################################################
        ##########################################################################################

        os.chdir('C:/Users/bpaur/PycharmProjects/webscrap/')

        # use ISIN list to loop through and grab reports
        # login credentials
        driver = webdriver.Chrome()
        driver.get("http://www.glasslewis.net")
        driver.maximize_window()
        assert "Glass Lewis" in driver.title

        # enters UN
        email_elem = driver.find_element(by=By.XPATH,
                                         value="/html/body/table/tbody/tr/td/form/table/tbody/tr[5]/td[2]/input")
        email_elem.clear()
        email_elem.send_keys(GL_USER)

        # enteres PW
        pw_elem = driver.find_element(by=By.XPATH,
                                      value="/html/body/table/tbody/tr/td/form/table/tbody/tr[7]/td[2]/input")
        pw_elem.clear()
        pw_elem.send_keys(GL_PW)
        pw_elem.send_keys(Keys.RETURN)

        for i in self.isin_list:
            # gets ISIN location in dataframe
            comp_name_loc = self.dataframe.loc[self.dataframe['\tISIN'] == i].index.values
            # gets company name based on ISIN location
            comp_name = self.dataframe['\tCompany Name'].values[comp_name_loc]

            # checks to see if file exist in directory
            # ex {C:/Users/bpaur/Desktop/test/} {company name folder} / {company name_Glass_Lewis_Research.pdf}

            if exists(f"{self.newdir}{comp_name[0]}/{comp_name[0]}_Glass_Lewis_Research.pdf") == False:

                try:

                    ##########################################################################################
                    #### searches for ISIN ###################################################################
                    ##########################################################################################

                    sec_search = driver.find_element(by=By.XPATH,
                                                     value="/html/body/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/form/input[1]")
                    sec_search.clear()
                    sec_search.send_keys(i)
                    sec_search.send_keys(Keys.RETURN)

                    proxy_paper = driver.find_element(by=By.XPATH,
                                                      value="/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div[2]/table/tbody/tr[2]/td[3]/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td/a")
                    proxy_paper.click()

                    time.sleep(3)

                    driver.switch_to.window(driver.window_handles[-1])
                    print_pdf = driver.find_element(by=By.CLASS_NAME, value="verdana_small")
                    print_pdf.click()

                    time.sleep(3)

                    driver.switch_to.window(driver.window_handles[0])

                    time.sleep(5)

                    ##########################################################################################
                    #### renames files #######################################################################
                    ##########################################################################################

                    # change directory
                    os.chdir(self.originaldir)

                    # looks for latest downloaded file in defined directory
                    list_of_files = glob.glob(f"{self.originaldir}*pdf")
                    latest_download = max(list_of_files, key=os.path.getctime)

                    # locates ISIN location in dataframe so that we can rename file based on company name
                    comp_name_loc = self.dataframe.loc[self.dataframe['\tISIN'] == i].index.values
                    comp_name = self.dataframe['\tCompany Name'].values[comp_name_loc]

                    # renames file based on company name
                    os.renames(latest_download, f'{comp_name[0]}_Glass_Lewis_Research.pdf')
                    print(f"---------{comp_name[0]} saved down---------")

                    ##########################################################################################
                    #### moves files #########################################################################
                    ##########################################################################################

                    os.chdir(self.originaldir)
                    shutil.move(f"{self.originaldir}{comp_name[0]}_Glass_Lewis_Research.pdf",
                               f"{self.newdir}{comp_name[0]}/{comp_name[0]}_Glass_Lewis_Research.pdf")

                    ##########################################################################################
                    #### Adds to log #########################################################################
                    ##########################################################################################

                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_glass_lewis.log",encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}---------{comp_name[0]} saved down---------")

                except:
                    print(f"{i} not found in search")
                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_glass_lewis.log",encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} {i} not found in search")
            else:
                print(f"||||{comp_name[0]} already exists||||")
                os.chdir(f"{self.newdir}logs/")
                logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_glass_lewis.log",encoding='utf-8', level=logging.INFO)
                logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}||||{comp_name[0]} already exists||||")

