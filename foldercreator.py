import os
import pandas as pd
import logging
from datetime import datetime

class FolderCreator:

    def __init__(self,filename,dir):
        self.filename = filename
        self.dir = dir
        
    def logger(self):
        if os.path.exists(f"{self.dir}logs/") == False:
            os.mkdir(f"{self.dir}logs/")
            os.chdir(f"{self.dir}logs/")
        else:
            os.chdir(f"{self.dir}logs/")

    def create_list(self):
        # reads csv then creates list based on first column
        # empties empty space and formats list names to each be capitalized
        os.chdir(self.dir)
        try:
            df = pd.read_csv(self.filename, delimiter=',')
            df = df.iloc[:, 0].str.strip()
            df = df.str.title()
            folders = list(set(df.tolist()))
            return folders
        except:
            print(f"no {self.filename} file found")
            close = int(input("press enter to close"))

            os.chdir(f"{self.dir}logs/")
            logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_folder_creator.log",encoding='utf-8', level=logging.INFO)
            logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} no {self.filename} file found")


    def write_folder(self):
        # uses create_list() and loops through list to create folders
        # if folder already exists it skips to the next item on the list
        folder_names = self.create_list()
        try:
            for items in folder_names:
                if os.path.exists(os.path.join(self.dir, items)) == True:
                    pass
                else:
                    path = os.path.join(self.dir, items)
                    os.mkdir(path)
            print(f'folder list successfully created/updated')
            
            os.chdir(f"{self.dir}logs/")
            logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_folder_creator.log",
                                encoding='utf-8', level=logging.INFO)
            logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} folder list successfully created/updated")

        except:
            print('unable to create/update folders')
            
            os.chdir(f"{self.dir}logs/")
            logging.basicConfig(filename=f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')}_folder_creator.log",
                                encoding='utf-8', level=logging.INFO)
            logging.info(f"{datetime.now().strftime('[%m_%d_%Y_%H_%M_%S]')} unable to create/update folders")
            
            close = int(input("press enter to close"))






