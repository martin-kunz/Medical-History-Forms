# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerSaveQuestion.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 700)
        MainWindow.setMinimumSize(QtCore.QSize(600, 700))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.SpeicherButton = QtWidgets.QPushButton(self.widget)
        self.SpeicherButton.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.SpeicherButton.setFont(font)
        self.SpeicherButton.setObjectName("SpeicherButton")
        self.horizontalLayout.addWidget(self.SpeicherButton)
        self.AbbrechButton = QtWidgets.QPushButton(self.widget)
        self.AbbrechButton.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.AbbrechButton.setFont(font)
        self.AbbrechButton.setObjectName("AbbrechButton")
        self.horizontalLayout.addWidget(self.AbbrechButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 562, 577))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(20, 10, 10, 5)
        self.formLayout.setSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_kategorie = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_kategorie.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.comboBox_kategorie.setFont(font)
        self.comboBox_kategorie.setObjectName("comboBox_kategorie")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_kategorie)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_fragentyp = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_fragentyp.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.comboBox_fragentyp.setFont(font)
        self.comboBox_fragentyp.setObjectName("comboBox_fragentyp")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_fragentyp)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_beschreibung = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.lineEdit_beschreibung.setFont(font)
        self.lineEdit_beschreibung.setObjectName("lineEdit_beschreibung")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_beschreibung)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_kurzbeschreibung = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.lineEdit_kurzbeschreibung.setFont(font)
        self.lineEdit_kurzbeschreibung.setObjectName("lineEdit_kurzbeschreibung")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_kurzbeschreibung)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.checkBox_pflichtfrage = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_pflichtfrage.setText("")
        self.checkBox_pflichtfrage.setObjectName("checkBox_pflichtfrage")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.checkBox_pflichtfrage)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.checkBox_kommentar = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_kommentar.setText("")
        self.checkBox_kommentar.setObjectName("checkBox_kommentar")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.checkBox_kommentar)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.checkBox_auswertbar = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_auswertbar.setText("")
        self.checkBox_auswertbar.setObjectName("checkBox_auswertbar")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.checkBox_auswertbar)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.dropdown_relatedQuestion = ExtendedComboBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.dropdown_relatedQuestion.setFont(font)
        self.dropdown_relatedQuestion.setObjectName("dropdown_relatedQuestion")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dropdown_relatedQuestion)
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.dropdown_necessaryAnswer = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.dropdown_necessaryAnswer.setFont(font)
        self.dropdown_necessaryAnswer.setObjectName("dropdown_necessaryAnswer")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.dropdown_necessaryAnswer)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.formLayout_2.setObjectName("formLayout_2")
        self.verticalLayout.addLayout(self.formLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anamnesebögen - Frage hinzufügen"))
        self.label.setText(_translate("MainWindow", "Frage hinzufügen oder editieren"))
        self.SpeicherButton.setText(_translate("MainWindow", "Speichern"))
        self.AbbrechButton.setText(_translate("MainWindow", "Abbrechen"))
        self.label_2.setText(_translate("MainWindow", "Kategorie:"))
        self.label_3.setText(_translate("MainWindow", "Fragentyp:"))
        self.label_4.setText(_translate("MainWindow", "Fragentext:"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p>Kurzbeschreibung:<br/>(eindeutig)</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Pflichtfrage:"))
        self.label_7.setText(_translate("MainWindow", "Kommentar:"))
        self.label_8.setText(_translate("MainWindow", "Auswertbar:"))
        self.label_9.setText(_translate("MainWindow", "Bezogen auf:"))
        self.label_10.setText(_translate("MainWindow", "Benötigte Antwort:"))


from GUI.ExtendedComboBox import ExtendedComboBox