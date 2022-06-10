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
import shutil


class MeetingPDFBallotDownload:
    def __init__(self, institutionID, originaldir, newdir, comp_list=[], dataframe='placeholder dataframe'):
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

    def meeting_voted_ballot_download(self):

        for i in self.comp_list:

            comp_isin_loc = self.dataframe.loc[self.dataframe['\tCompany Name'] == i.title()].index.values
            vote_status = self.dataframe['\tVote Status'].values[comp_isin_loc]

            if vote_status[0] == 'Voted':

                if exists(f"{self.newdir}{i.title()}/{i.title()}_voted_ballot_page.pdf") == False:

                    try:
                        # needed to establish web driver
                        path = "C:/Users/bpaur/PycharmProjects/webscrap"
                        os.chdir(path)

                        # establishes web driver
                        driver = webdriver.Chrome()
                        driver.get(
                            "https://sso.net.broadridge.com/cc/proxyedgelogin.do?TYPE=33554433&REALMOID=06-8d1b7c2a-dae5-4a69-a746-d70fe0bef606&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=65422_proxyedge&TARGET=$SM$HTTPS%3a%2f%2fcentral%2eproxyedge%2ecom%2fPEWeb")
                        driver.maximize_window()
                        # checks website to make sure the title is the pe title page
                        assert "Broadridge - ProxyEdge" in driver.title

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
                        int_id_elem.send_keys(self.institutionID)
                        int_id_elem.send_keys(Keys.RETURN)

                        # dropdown
                        dropdown = driver.find_element(by=By.XPATH,
                                                       value="/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/a")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()

                        time.sleep(2)

                        # standardized reports
                        standardized_reports = driver.find_element(by=By.XPATH,
                                                                   value="/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/ul/li[1]/a")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(standardized_reports).click(standardized_reports).perform()

                        time.sleep(2)

                        # manage reports
                        manage_reports = driver.find_element(by=By.XPATH,
                                                             value="/html/body/div[1]/div/div[5]/form/div/div[1]/ul/li[2]/a")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(manage_reports).click(manage_reports).perform()

                        time.sleep(2)

                        # create new dropdown
                        create_new_dropdown = driver.find_element(by=By.XPATH,
                                                                  value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[2]/div[1]/div/div[2]/button")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(create_new_dropdown).click(create_new_dropdown).perform()

                        time.sleep(2)

                        # one time report
                        one_time_report = driver.find_element(by=By.XPATH,
                                                              value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/a/span[1]")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(one_time_report).click(one_time_report).perform()

                        time.sleep(2)

                        # report type
                        report_type = driver.find_element(by=By.XPATH,
                                                          value="/html/body/div[1]/div/div[5]/form/div/div[1]/div[1]/div/div/button/span[1]")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(report_type).click(report_type).perform()

                        time.sleep(2)

                        # vote summary
                        vote_summary = driver.find_element(by=By.XPATH,
                                                           value="/html/body/div[1]/div/div[5]/form/div/div[1]/div[1]/div/div/div/ul/li[1]/a/span[1]")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(vote_summary).click(vote_summary).perform()

                        time.sleep(2)

                        # specific meeting
                        specific_meeting = driver.find_element(by=By.XPATH,
                                                               value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[1]/div[2]/div[1]/div")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(specific_meeting).click(specific_meeting).perform()
                        time.sleep(1)

                        # enters ISIN
                        comp_isin_loc = self.dataframe.loc[self.dataframe['\tCompany Name'] == i.title()].index.values
                        comp_isin = self.dataframe['\tISIN'].values[comp_isin_loc]

                        isin = driver.find_element(by=By.XPATH,
                                                   value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[3]/div[1]/div[2]/div[3]/input")
                        isin.clear()
                        isin.send_keys(comp_isin)
                        isin.send_keys(Keys.RETURN)

                        # click search
                        click_search = driver.find_element(by=By.XPATH,
                                                           value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[3]/div[3]/div[1]/button[1]/span[1]")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(click_search).click(click_search).perform()
                        time.sleep(1)

                        # account dropdown
                        account_dropdown = driver.find_element(by=By.XPATH,
                                                               value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[4]/div[2]/fieldset/div[1]/div/div[2]/div/button")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(account_dropdown).click(account_dropdown).perform()

                        # all accounts
                        all_accounts = driver.find_element(by=By.XPATH,
                                                           value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[4]/div[2]/fieldset/div[1]/div/div[2]/div/div/ul/li[1]/a")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(all_accounts).click(all_accounts).perform()

                        # submit
                        submit = driver.find_element(by=By.XPATH,
                                                     value="/html/body/div[1]/div/div[5]/form/div/div[3]/button[1]")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(submit).click(submit).perform()

                        time.sleep(6)

                        # handles new window pop up
                        new_window = driver.window_handles[-1]
                        driver.switch_to.window(new_window)
                        # this is why proxyedge is a terrible website...
                        driver.switch_to.frame("toolbarframe")

                        # download
                        download = driver.find_element(by=By.XPATH,
                                                       value="/html/body/div/form/table/tbody/tr/td[12]/b/a")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(download).click(download).perform()

                        time.sleep(3)

                        # handles new window pop up
                        new_window = driver.window_handles[-1]
                        driver.switch_to.window(new_window)

                        # save_report
                        save_report = driver.find_element(by=By.XPATH,
                                                          value="/html/body/form[2]/table/tbody/tr/td[2]/center/div/input")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(save_report).click(save_report).perform()
                        time.sleep(1)

                        ##########################################################################################
                        #### renames files #######################################################################
                        ##########################################################################################

                        os.chdir(self.originaldir)
                        list_of_files = glob.glob(f"{self.originaldir}*pdf")
                        latest_download = max(list_of_files, key=os.path.getctime)
                        os.renames(latest_download, f'{i.title()}_voted_ballot_page.pdf')

                        ##########################################################################################
                        #### moves files #########################################################################
                        ##########################################################################################

                        os.replace(f"{self.originaldir}{i.title()}_voted_ballot_page.pdf",
                                   f"{self.newdir}{i.title()}/{i.title()}_voted_ballot_page.pdf")

                        print(f"---------{i.title()} successfully saved down---------")

                        ##########################################################################################
                        #### Adds to log #########################################################################
                        ##########################################################################################

                        os.chdir(f"{self.newdir}logs/")
                        logging.basicConfig(
                            filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                            encoding='utf-8', level=logging.INFO)
                        logging.info(
                            f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}---------{i.title()} successfully saved down---------")

                    except:
                        print(f"unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")
                        os.chdir(f"{self.newdir}logs/")
                        logging.basicConfig(
                            filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                            encoding='utf-8', level=logging.INFO)
                        logging.info(
                            f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")

                else:
                    print(f"||||{i} already exists||||")
                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(
                        filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                        encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}||||{i} already exists||||")

            else:

                if vote_status[0] == 'Unvoted':

                    if exists(f"{self.newdir}{i.title()}/{i.title()}_unvoted_ballot_page.pdf") == False:

                        try:
                            # needed to establish web driver
                            path = "C:/Users/bpaur/PycharmProjects/webscrap"
                            os.chdir(path)

                            # establishes web driver
                            driver = webdriver.Chrome()
                            driver.get(
                                "https://sso.net.broadridge.com/cc/proxyedgelogin.do?TYPE=33554433&REALMOID=06-8d1b7c2a-dae5-4a69-a746-d70fe0bef606&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=65422_proxyedge&TARGET=$SM$HTTPS%3a%2f%2fcentral%2eproxyedge%2ecom%2fPEWeb")
                            driver.maximize_window()
                            # checks website to make sure the title is the pe title page
                            assert "Broadridge - ProxyEdge" in driver.title

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
                            int_id_elem.send_keys(self.institutionID)
                            int_id_elem.send_keys(Keys.RETURN)

                            # dropdown
                            dropdown = driver.find_element(by=By.XPATH,
                                                           value="/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/a")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()

                            time.sleep(2)

                            # standardized reports
                            standardized_reports = driver.find_element(by=By.XPATH,
                                                                       value="/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/ul/li[1]/a")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(standardized_reports).click(
                                standardized_reports).perform()

                            time.sleep(2)

                            # manage reports
                            manage_reports = driver.find_element(by=By.XPATH,
                                                                 value="/html/body/div[1]/div/div[5]/form/div/div[1]/ul/li[2]/a")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(manage_reports).click(manage_reports).perform()

                            time.sleep(2)

                            # create new dropdown
                            create_new_dropdown = driver.find_element(by=By.XPATH,
                                                                      value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[2]/div[1]/div/div[2]/button")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(create_new_dropdown).click(
                                create_new_dropdown).perform()

                            time.sleep(2)

                            # one time report
                            one_time_report = driver.find_element(by=By.XPATH,
                                                                  value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/a/span[1]")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(one_time_report).click(one_time_report).perform()

                            time.sleep(2)

                            # report type
                            report_type = driver.find_element(by=By.XPATH,
                                                              value="/html/body/div[1]/div/div[5]/form/div/div[1]/div[1]/div/div/button/span[1]")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(report_type).click(report_type).perform()

                            time.sleep(2)

                            # vote summary
                            vote_summary = driver.find_element(by=By.XPATH,
                                                               value="/html/body/div[1]/div/div[5]/form/div/div[1]/div[1]/div/div/div/ul/li[1]/a/span[1]")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(vote_summary).click(vote_summary).perform()

                            time.sleep(2)

                            # specific meeting
                            specific_meeting = driver.find_element(by=By.XPATH,
                                                                   value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[1]/div[2]/div[1]/div")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(specific_meeting).click(specific_meeting).perform()
                            time.sleep(1)

                            # enters ISIN
                            comp_isin_loc = self.dataframe.loc[
                                self.dataframe['\tCompany Name'] == i.title()].index.values
                            comp_isin = self.dataframe['\tISIN'].values[comp_isin_loc]

                            isin = driver.find_element(by=By.XPATH,
                                                       value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[3]/div[1]/div[2]/div[3]/input")
                            isin.clear()
                            isin.send_keys(comp_isin)
                            isin.send_keys(Keys.RETURN)

                            # click search
                            click_search = driver.find_element(by=By.XPATH,
                                                               value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[3]/div[2]/fieldset/div[3]/div[3]/div[1]/button[1]/span[1]")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(click_search).click(click_search).perform()
                            time.sleep(1)

                            # account dropdown
                            account_dropdown = driver.find_element(by=By.XPATH,
                                                                   value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[4]/div[2]/fieldset/div[1]/div/div[2]/div/button")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(account_dropdown).click(account_dropdown).perform()

                            # all accounts
                            all_accounts = driver.find_element(by=By.XPATH,
                                                               value="/html/body/div[1]/div/div[5]/form/div/div[2]/div/div[4]/div[2]/fieldset/div[1]/div/div[2]/div/div/ul/li[1]/a")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(all_accounts).click(all_accounts).perform()

                            # submit
                            submit = driver.find_element(by=By.XPATH,
                                                         value="/html/body/div[1]/div/div[5]/form/div/div[3]/button[1]")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(submit).click(submit).perform()

                            time.sleep(6)

                            # handles new window pop up
                            new_window = driver.window_handles[-1]
                            driver.switch_to.window(new_window)
                            # this is why proxyedge is a terrible website...
                            driver.switch_to.frame("toolbarframe")

                            # download
                            download = driver.find_element(by=By.XPATH,
                                                           value="/html/body/div/form/table/tbody/tr/td[12]/b/a")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(download).click(download).perform()

                            time.sleep(3)

                            # handles new window pop up
                            new_window = driver.window_handles[-1]
                            driver.switch_to.window(new_window)

                            # save_report
                            save_report = driver.find_element(by=By.XPATH,
                                                              value="/html/body/form[2]/table/tbody/tr/td[2]/center/div/input")
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(save_report).click(save_report).perform()
                            time.sleep(1)

                            # renames report
                            os.chdir(self.originaldir)
                            list_of_files = glob.glob(f"{self.originaldir}*pdf")
                            latest_download = max(list_of_files, key=os.path.getctime)
                            os.renames(latest_download, f'{i.title()}_unvoted_ballot_page.pdf')

                            os.chdir(f"{self.newdir}logs/")
                            logging.basicConfig(
                                filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                                encoding='utf-8', level=logging.INFO)
                            logging.info(
                                f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}---------{i.title()} successfully saved down---------")

                            # moves files
                            shutil.move(f"{self.originaldir}{i.title()}_unvoted_ballot_page.pdf",
                                       f"{self.newdir}{i.title()}/{i.title()}_unvoted_ballot_page.pdf")

                            print(f"---------{i.title()} successfully saved down---------")

                        except:
                            print(f"unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")
                            os.chdir(f"{self.newdir}logs/")
                            logging.basicConfig(
                                filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                                encoding='utf-8', level=logging.INFO)
                            logging.info(
                                f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} unable to save down {i}'s meeting ballot. PLEASE REVIEW. Moving on...")

                else:
                    print(f"||||{i} already exists||||")
                    os.chdir(f"{self.newdir}logs/")
                    logging.basicConfig(
                        filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_voted_ballot_download.log",
                        encoding='utf-8', level=logging.INFO)
                    logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}||||{i} already exists||||")


