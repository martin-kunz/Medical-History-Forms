# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerDBInformation.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DBWindow(object):
    def setupUi(self, DBWindow):
        DBWindow.setObjectName("DBWindow")
        DBWindow.resize(900, 352)
        DBWindow.setMinimumSize(QtCore.QSize(900, 352))
        DBWindow.setMaximumSize(QtCore.QSize(900, 352))
        DBWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(DBWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 1)
        self.notlicensedlabel = QtWidgets.QLabel(self.centralwidget)
        self.notlicensedlabel.setObjectName("notlicensedlabel")
        self.gridLayout.addWidget(self.notlicensedlabel, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.dbactive_namelabel = QtWidgets.QLabel(self.frame)
        self.dbactive_namelabel.setMinimumSize(QtCore.QSize(0, 10))
        self.dbactive_namelabel.setText("")
        self.dbactive_namelabel.setObjectName("dbactive_namelabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dbactive_namelabel)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dbactive_adresslabel = QtWidgets.QLabel(self.frame)
        self.dbactive_adresslabel.setText("")
        self.dbactive_adresslabel.setObjectName("dbactive_adresslabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dbactive_adresslabel)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dbactive_portlabel = QtWidgets.QLabel(self.frame)
        self.dbactive_portlabel.setMinimumSize(QtCore.QSize(10, 0))
        self.dbactive_portlabel.setText("")
        self.dbactive_portlabel.setObjectName("dbactive_portlabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dbactive_portlabel)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.dbactive_userlabel = QtWidgets.QLabel(self.frame)
        self.dbactive_userlabel.setText("")
        self.dbactive_userlabel.setObjectName("dbactive_userlabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dbactive_userlabel)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.gridLayout_3.addLayout(self.formLayout, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.dbwindowdeletebutton = QtWidgets.QPushButton(self.frame)
        self.dbwindowdeletebutton.setObjectName("dbwindowdeletebutton")
        self.horizontalLayout.addWidget(self.dbwindowdeletebutton)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.savedbbutton = QtWidgets.QPushButton(self.frame)
        self.savedbbutton.setObjectName("savedbbutton")
        self.horizontalLayout.addWidget(self.savedbbutton)
        self.abbrechdbbutton = QtWidgets.QPushButton(self.frame)
        self.abbrechdbbutton.setObjectName("abbrechdbbutton")
        self.horizontalLayout.addWidget(self.abbrechdbbutton)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(0, 10, 10, 10)
        self.formLayout_2.setSpacing(20)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.dbdatabaseinput = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbdatabaseinput.sizePolicy().hasHeightForWidth())
        self.dbdatabaseinput.setSizePolicy(sizePolicy)
        self.dbdatabaseinput.setObjectName("dbdatabaseinput")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dbdatabaseinput)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.dbhostinput = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbhostinput.sizePolicy().hasHeightForWidth())
        self.dbhostinput.setSizePolicy(sizePolicy)
        self.dbhostinput.setMinimumSize(QtCore.QSize(10, 0))
        self.dbhostinput.setObjectName("dbhostinput")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dbhostinput)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.dbportinput = QtWidgets.QLineEdit(self.frame)
        self.dbportinput.setObjectName("dbportinput")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dbportinput)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.dbuserinput = QtWidgets.QLineEdit(self.frame)
        self.dbuserinput.setObjectName("dbuserinput")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dbuserinput)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.dbpasswordinput = QtWidgets.QLineEdit(self.frame)
        self.dbpasswordinput.setInputMask("")
        self.dbpasswordinput.setObjectName("dbpasswordinput")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dbpasswordinput)
        self.gridLayout_3.addLayout(self.formLayout_2, 1, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 2)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout.addWidget(self.frame, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.savelicenselabel = QtWidgets.QLabel(self.centralwidget)
        self.savelicenselabel.setObjectName("savelicenselabel")
        self.horizontalLayout_2.addWidget(self.savelicenselabel)
        self.savelicenselineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.savelicenselineedit.setObjectName("savelicenselineedit")
        self.horizontalLayout_2.addWidget(self.savelicenselineedit)
        self.savelicensebutton = QtWidgets.QPushButton(self.centralwidget)
        self.savelicensebutton.setObjectName("savelicensebutton")
        self.horizontalLayout_2.addWidget(self.savelicensebutton)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem11)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        DBWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DBWindow)
        QtCore.QMetaObject.connectSlotsByName(DBWindow)

    def retranslateUi(self, DBWindow):
        _translate = QtCore.QCoreApplication.translate
        DBWindow.setWindowTitle(_translate("DBWindow", "Anamnesebögen - Datenbank"))
        self.notlicensedlabel.setText(
            _translate("DBWindow", '<html><head/><body><p align="center"><span style=" font-weight:600;">Dieses Feature ist in Ihrer Version derzeit nicht freigeschaltet.</span></p></body></html>')
        )
        self.label_5.setText(_translate("DBWindow", "DB-Name:"))
        self.label.setText(_translate("DBWindow", "Adresse:"))
        self.label_2.setText(_translate("DBWindow", "Port:"))
        self.label_3.setText(_translate("DBWindow", "Benutzer:"))
        self.label_4.setText(_translate("DBWindow", "Passwort:"))
        self.label_7.setText(
            _translate(
                "DBWindow",
                '<html><head/><body><p align="center"><span style=" font-weight:600;">Ist eine Datenbank aktiv,</span></p><p align="center"><span style=" font-weight:600;">werden die Daten untenstehend angezeigt:</span></p></body></html>',
            )
        )
        self.label_8.setText(
            _translate(
                "DBWindow",
                '<html><head/><body><p align="center"><span style=" font-weight:600;">Andernfalls können hier Daten </span></p><p align="center"><span style=" font-weight:600;">zum Aktivieren eingetragen werden:</span></p></body></html>',
            )
        )
        self.dbwindowdeletebutton.setText(_translate("DBWindow", "Zurücksetzen"))
        self.savedbbutton.setText(_translate("DBWindow", "Speichern"))
        self.abbrechdbbutton.setText(_translate("DBWindow", "Abbrechen"))
        self.label_9.setText(_translate("DBWindow", "DB-Name:"))
        self.label_10.setText(_translate("DBWindow", "Adresse:"))
        self.label_11.setText(_translate("DBWindow", "Port:"))
        self.label_12.setText(_translate("DBWindow", "Benutzer:"))
        self.label_13.setText(_translate("DBWindow", "Passwort:"))
        self.label_6.setText(_translate("DBWindow", "Informationen zu einer externen Datenbank"))
        self.savelicenselabel.setText(_translate("DBWindow", "Lizenz hinterlegen:"))
        self.savelicensebutton.setText(_translate("DBWindow", "Aktivieren"))
