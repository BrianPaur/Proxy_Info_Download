import os
import shutil

class FileMover:

    def __init__(self, original_file_path, new_file_path, filename, filetype):
        self.original_file_path = original_file_path
        self.new_file_path = new_file_path
        self.filename = filename
        self.filetype = filetype

    def move_file(self):
        try:
            os.chdir(self.original_file_path)
            shutil.move(f"{self.original_file_path}{self.filename}.{self.filetype}", f"{self.new_file_path}{self.filename}.{self.filetype}")
            print(f'successfully moved {self.filename} meeting list')

        except:
            print(f'unable to move {self.filename} meeting list')
            close = int(input("press enter to close"))

