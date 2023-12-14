# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerWarningAbbrv.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChooseDBWindow(object):
    def setupUi(self, ChooseDBWindow):
        ChooseDBWindow.setObjectName("ChooseQAWindow")
        ChooseDBWindow.resize(803, 306)
        self.centralwidget = QtWidgets.QWidget(ChooseDBWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableQuestionList = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.tableQuestionList.setFont(font)
        self.tableQuestionList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableQuestionList.setLineWidth(2)
        self.tableQuestionList.setMidLineWidth(1)
        self.tableQuestionList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableQuestionList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableQuestionList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableQuestionList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableQuestionList.setTextElideMode(QtCore.Qt.ElideLeft)
        self.tableQuestionList.setIndentation(0)
        self.tableQuestionList.setColumnCount(2)
        self.tableQuestionList.setObjectName("tableQuestionList")
        self.tableQuestionList.header().setDefaultSectionSize(50)
        self.tableQuestionList.header().setMinimumSectionSize(0)
        self.tableQuestionList.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableQuestionList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(680, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.closechoosedbbutton = QtWidgets.QPushButton(self.centralwidget)
        self.closechoosedbbutton.setObjectName("closechoosedbbutton")
        self.horizontalLayout.addWidget(self.closechoosedbbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        ChooseDBWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChooseDBWindow)
        QtCore.QMetaObject.connectSlotsByName(ChooseDBWindow)

    def retranslateUi(self, ChooseDBWindow):
        _translate = QtCore.QCoreApplication.translate
        ChooseDBWindow.setWindowTitle(_translate("ChooseQAWindow", "MainWindow"))
        self.label.setText(
            _translate(
                "ChooseQAWindow",
                '<html><head/><body><p align="center"><span style=" font-size:12pt;">Die folgenden Kurzbeschreibungen sind bereits vergeben, bitte überarbeiten sie diese Fragen</span></p></body></html>',
            )
        )
        self.tableQuestionList.headerItem().setText(0, _translate("ChooseQAWindow", "Fragentext"))
        self.tableQuestionList.headerItem().setText(1, _translate("ChooseQAWindow", "Kurzbeschreibung"))
        self.closechoosedbbutton.setText(_translate("ChooseQAWindow", "Schließen"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ChooseDBWindow = QtWidgets.QMainWindow()
    ui = Ui_ChooseDBWindow()
    ui.setupUi(ChooseDBWindow)
    ChooseDBWindow.show()
    sys.exit(app.exec_())
