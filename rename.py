import os
import glob

class Rename:

    def __init__(self,filepathdir,filerename,filetype):
        self.filepathdir = filepathdir
        self.filerename = filerename
        self.filetype = filetype

    def rename(self):

        os.chdir(self.filepathdir)
        list_of_files = glob.glob(f"{self.filepathdir}*{self.filetype}")
        latest_download = max(list_of_files, key=os.path.getctime)
        os.renames(latest_download, f'{self.filerename}.{self.filetype}')
