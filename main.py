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
        Rename('Files original directory',
               'Files new directory',
               i,
               'filetype').rename()
        FileMover('cwd',
                  'Files original directory',
                  'Files new directory',
                  i,
                  'filetype').move_file()

    #################################################################################
    ##### Creates folders based on company names in file defined ####################
    #################################################################################

    a = FolderCreator('file to read from',
                  'Files original directory')
    a.logger()
    a.write_folder()

    #################################################################################
    ##### Downloads Glass Lewis research and saves in correct folder ################
    #################################################################################

    b = GlassLewis('Files original directory',
                   'Files new directory',
                   'file to read from',
                   [],
                   'placeholder dataframe')

    b.logger()
    b.ISIN_to_list()
    b.data_frames()
    b.pull_down_reports()

    #################################################################################
    ##### Downloads ProxyEdge ballot and saves in correct folder ####################
    #################################################################################

    c = MeetingBallotDownload('Institution ID',
                              'Files original directory',
                              'Files new directory',
                              [],
                              'placeholder dataframe')

    c.logger()
    c.comp_name_to_list()
    c.data_frames()
    c.meeting_ballot_download()

    #################################################################################
    ##### Downloads ProxyEdge pdf ballot and saves in correct folder ################
    #################################################################################

    d = MeetingPDFBallotDownload('Institution ID',
                                 'Files original directory',
                                 'Files new directory',
                                 [],
                                 'placeholder dataframe')

    d.logger()
    d.comp_name_to_list()
    d.data_frames()
    d.meeting_voted_ballot_download()
