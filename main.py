import sys

from PyQt5.QtCore import *

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui


from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QToolTip, QMessageBox, QLabel)

'''everytime resource change
pyrcc5 -o qrc_resources.py resources.qrc'''
import qrc_resource

#


# main window class
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # double click on tab bar will create a new tab using this funtuon: tab_open_doubleclick()
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        self.tabs.currentChanged.connect(self.current_tab_changed)
        # cross sign on tab
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)


        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()

        self.setStatusBar(self.status)

        # geometry of window (left,top,width,height)
        self.setGeometry(20, 50, 1300, 650)
        # window will open in maximum size of your laptop/computer screen
        self.showMaximized()

        # navigation tab containing back, forward, reload, home, urlbar, new tab, stop
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # this will break the toolbar and another toolbar can be added
        self.addToolBarBreak()

        # another toolbar named toolbar 2 is declared
        toolbar2 = self.addToolBar("BookMark")

        # components of toolbar2
        #reload_btn = QAction(QIcon(":refresh.svg"), "Reload", self)
        #reload_btn.setStatusTip("Reload page")
        #reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        #toolbar2.addAction(reload_btn)

        # components of toolbar 1
        back_btn = QAction(QIcon(":back-arrow.svg"), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(":forward-arrow.svg"), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(":refresh.svg"), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(":home.svg"), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        navtb.addSeparator()

        newtab_btn = QAction(QIcon(":add.svg"), "New Tab", self)
        newtab_btn.setStatusTip("Adds a new tab")
        newtab_btn.triggered.connect(lambda: self.add_new_tab())
        navtb.addAction(newtab_btn)

        stop_btn = QAction(QIcon(":stop.svg"), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        # End of components of toolbar 1 i.e navtb

        # this will start with a new tab with particular link
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        #self.bookmarks_load()

        self.show()

        # browser icon
        self.setWindowIcon(QIcon(":icon.svg"))
        # browser title
        self.setWindowTitle("Web Browser")

    # for bookmark
    #     def Bookmark(self):
    #     try:
    #         qurl = QUrl(self.urlbar.text())
    #         print('Here we are using the QUrl toString method: %s ---> Type: %s' % (qurl.toString(), type(qurl)))
    #         url = qurl.toString()
    #         print('Here we are storing the new string to a new variable: %s ---> Type: %s' % (url, type(url)))
    #         b = open(os.path.join('bookmarks', 'bookmarks.txt'), "wb")
    #         self.bookmarks_write = pickle.dump(url, b)
    #         b.close()
    #     except:
    #         print("Crash - Bookmarks not stored")

    #     self.bookmark_btn.setText("★")


    # This is for history
    def on_pushButton_clicked(self):
        self.dialog.show()

    # this will add new tab()
    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):

        qurl = self.tabs.currentWidget().url()

        self.update_urlbar(qurl, self.tabs.currentWidget())

        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):

        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):

        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

        self.setWindowTitle("% s Search" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):

        q = QUrl(self.urlbar.text())
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + q, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")
        #str = q.toString()

        #f = open("bookmarks.txt", "w+")
        #f.write(str + "Append\n")
        #filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".conf")
        #f.close()

        if q.scheme() == "":

            # set scheme
            q.setScheme("http")


        self.tabs.currentWidget().setUrl(q)


    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Group")
window = MainWindow()
window.setStyleSheet("""QWidget{
           background-color: rgb(0, 13, 26);
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            top: -0.5em;
            color: rgb(255, 255, 255);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(64, 191, 64);
            border: 2px solid rgb(90, 90, 90);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(255, 255, 255);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(255,255,255);
            border: 2px solid rgb(0, 36, 36);
            color:rgb(0,0,0);

        }

        QLineEdit {
            border: 2px solid rgb(0, 36, 36);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(0, 36, 36);
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(103, 93, 105);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")
app.exec_()
