# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'management.ui'
#
# Created: Sat Mar  2 22:53:08 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(438, 372)
        Dialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.authBtn = QtGui.QPushButton(self.tab)
        self.authBtn.setObjectName("authBtn")
        self.gridLayout.addWidget(self.authBtn, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.syncDelayBox = QtGui.QComboBox(self.tab)
        self.syncDelayBox.setObjectName("syncDelayBox")
        self.gridLayout.addWidget(self.syncDelayBox, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.autoStart = QtGui.QCheckBox(self.tab)
        self.autoStart.setText("")
        self.autoStart.setObjectName("autoStart")
        self.gridLayout.addWidget(self.autoStart, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.noteFont = QtGui.QFontComboBox(self.tab_2)
        self.noteFont.setObjectName("noteFont")
        self.gridLayout_2.addWidget(self.noteFont, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.noteSize = QtGui.QSpinBox(self.tab_2)
        self.noteSize.setObjectName("noteSize")
        self.gridLayout_2.addWidget(self.noteSize, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.blackTray = QtGui.QCheckBox(self.tab_2)
        self.blackTray.setText("")
        self.blackTray.setObjectName("blackTray")
        self.gridLayout_2.addWidget(self.blackTray, 2, 1, 1, 1)
        self.progressLabel = QtGui.QLabel(self.tab_2)
        self.progressLabel.setObjectName("progressLabel")
        self.gridLayout_2.addWidget(self.progressLabel, 3, 0, 1, 1)
        self.progressCheckBox = QtGui.QCheckBox(self.tab_2)
        self.progressCheckBox.setText("")
        self.progressCheckBox.setObjectName("progressCheckBox")
        self.gridLayout_2.addWidget(self.progressCheckBox, 3, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.searchOnHome = QtGui.QCheckBox(self.tab_2)
        self.searchOnHome.setText("")
        self.searchOnHome.setObjectName("searchOnHome")
        self.gridLayout_2.addWidget(self.searchOnHome, 4, 1, 1, 1)
        self.label_indLayout = QtGui.QLabel(self.tab_2)
        self.label_indLayout.setObjectName("label_indLayout")
        self.gridLayout_2.addWidget(self.label_indLayout, 5, 0, 1, 1)
        self.listWidget_indLayout = QtGui.QListWidget(self.tab_2)
        self.listWidget_indLayout.setMinimumSize(QtCore.QSize(0, 96))
        self.listWidget_indLayout.setMaximumSize(QtCore.QSize(16777215, 96))
        self.listWidget_indLayout.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget_indLayout.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listWidget_indLayout.setObjectName("listWidget_indLayout")
        self.gridLayout_2.addWidget(self.listWidget_indLayout, 5, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Everpad / Settings and Management", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Authorisation", None, QtGui.QApplication.UnicodeUTF8))
        self.authBtn.setText(QtGui.QApplication.translate("Dialog", "Authorise", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Sync delay", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Start with system", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Note font family", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Note font size", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Black tray icon", None, QtGui.QApplication.UnicodeUTF8))
        self.progressLabel.setText(QtGui.QApplication.translate("Dialog", "Launcher progress bar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Search on the home lens", None, QtGui.QApplication.UnicodeUTF8))
        self.label_indLayout.setText(QtGui.QApplication.translate("Dialog", "Indicator Layout", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_indLayout.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Drag and drop items to change layout.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Appearance", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
