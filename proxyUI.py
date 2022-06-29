from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect
from login_settings import INST_ID
from meetinglistdownload import MeetingListDownload
from rename import Rename
from filemover import FileMover
from foldercreator import FolderCreator
from glasslewis import GlassLewis
from ballotdownload import MeetingBallotDownload
from ballotsheetdownload import MeetingPDFBallotDownload


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(472, 172)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.meetingListDownload = QtWidgets.QPushButton(self.centralwidget)
        self.meetingListDownload.setGeometry(QtCore.QRect(10, 10, 161, 23))
        self.meetingListDownload.setObjectName("meetingListDownload")
        self.meetingListDownload.clicked.connect(self._mettingListDownload)

        self.folderCreator = QtWidgets.QPushButton(self.centralwidget)
        self.folderCreator.setGeometry(QtCore.QRect(10, 40, 161, 23))
        self.folderCreator.setObjectName("folderCreator")
        self.folderCreator.clicked.connect(self._folderCreator)


        self.glassLewisResearchDownload = QtWidgets.QPushButton(self.centralwidget)
        self.glassLewisResearchDownload.setGeometry(QtCore.QRect(10, 70, 161, 23))
        self.glassLewisResearchDownload.setObjectName("glassLewisResearchDownload")
        self.glassLewisResearchDownload.clicked.connect(self._glassLewisResearch)

        self.proxyEdgeDownload = QtWidgets.QPushButton(self.centralwidget)
        self.proxyEdgeDownload.setGeometry(QtCore.QRect(10, 100, 161, 23))
        self.proxyEdgeDownload.setObjectName("proxyEdgeDownload")
        self.proxyEdgeDownload.clicked.connect(self._proxyEdgeDownload)

        self.proxyEdgePdfDownload = QtWidgets.QPushButton(self.centralwidget)
        self.proxyEdgePdfDownload.setGeometry(QtCore.QRect(10, 130, 161, 23))
        self.proxyEdgePdfDownload.setObjectName("proxyEdgePdfDownload")
        self.proxyEdgePdfDownload.clicked.connect(self._proxyEdgePdfDownload)

        self.outputLine = QLabel(self.centralwidget)
        self.outputLine.setObjectName(u"outputLine")
        self.outputLine.setGeometry(QRect(190, 10, 271, 141))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Proxy Document Downloader"))
        self.meetingListDownload.setText(_translate("MainWindow", "Meeting List Download"))
        self.folderCreator.setText(_translate("MainWindow", "Folder Creator"))
        self.glassLewisResearchDownload.setText(_translate("MainWindow", "Glass Lewis Research Download"))
        self.proxyEdgeDownload.setText(_translate("MainWindow", "ProxyEdge Download"))
        self.proxyEdgePdfDownload.setText(_translate("MainWindow", "ProxyEdge PDF Download"))

    def _mettingListDownload(self):
        for i in INST_ID:
            MeetingListDownload(i).meeting_list_download()
            Rename('Files original directory',
                   i,
                   'csv').rename()
            FileMover('Files original directory',
                      'Files new directory',
                      i,
                      'csv').move_file()
        self.outputLine.setText("meeting lists downloaded successfully")


    def _folderCreator(self):
        FolderCreator('file to read from',
                      'Files original directory').write_folder()
        self.outputLine.setText("folders created successfully")

    def _glassLewisResearch(self):
        b = GlassLewis('Files original directory',
                       'Files new directory',
                       'file to read from',)

        b.ISIN_to_list()
        b.data_frames()
        b.pull_down_reports()

        self.outputLine.setText("glass lewis research downloaded successfully")

    def _proxyEdgeDownload(self):
        c = MeetingBallotDownload('Institution ID',
                                  'Files original directory',
                                  'Files new directory')

        c.comp_name_to_list()
        c.data_frames()
        c.meeting_ballot_download()

        self.outputLine.setText("proxyedge xls downloaded successfully")

    def _proxyEdgePdfDownload(self):
        d = MeetingPDFBallotDownload('Institution ID',
                                     'Files original directory',
                                     'Files new directory')

        d.comp_name_to_list()
        d.data_frames()
        d.meeting_voted_ballot_download()

        self.outputLine.setText("proxyedge pdf downloaded successfully")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
