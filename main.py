from login_settings import INST_ID
from meetinglistdownload import MeetingListDownload
from rename import Rename
from filemover import FileMover
from foldercreator import FolderCreator
from glasslewis import GlassLewis
from ballotdownload import MeetingBallotDownload
from ballotsheetdownload import MeetingPDFBallotDownload


if __name__ == '__main__':

    #################################################################################
    ##### Downloads meeting list based on ProxyEdge institution IDs defined #########
    #################################################################################

    for i in INST_ID:
        MeetingListDownload(i).meeting_list_download()
        Rename('C:/Users/bpaur/Downloads/',
               i,
               'csv').rename()
        FileMover('C:/Users/bpaur/Downloads/',
                  'C:/Users/bpaur/Desktop/test/',
                  i,
                  'csv').move_file()

    #################################################################################
    ##### Creates folders based on company names in file defined ####################
    #################################################################################

    a = FolderCreator('ID',
                  'C:/Users/bpaur/Desktop/test/')
    a.write_folder()

    #################################################################################
    ##### Downloads Glass Lewis research and saves in correct folder ################
    #################################################################################

    b = GlassLewis('C:/Users/bpaur/Downloads/',
                   'C:/Users/bpaur/Desktop/test/',
                   'ID.csv')

    b.ISIN_to_list()
    b.data_frames()
    b.pull_down_reports()

    #################################################################################
    ##### Downloads ProxyEdge ballot and saves in correct folder ####################
    #################################################################################

    c = MeetingBallotDownload('ID',
                              'C:/Users/bpaur/Downloads/',
                              'C:/Users/bpaur/Desktop/test/')

    c.comp_name_to_list()
    c.data_frames()
    c.meeting_ballot_download()

    #################################################################################
    ##### Downloads ProxyEdge pdf ballot and saves in correct folder ################
    #################################################################################

    d = MeetingPDFBallotDownload('ID',
                                   'C:/Users/bpaur/Downloads/',
                                   'C:/Users/bpaur/Desktop/test/')

    d.comp_name_to_list()
    d.data_frames()
    d.meeting_voted_ballot_download()



