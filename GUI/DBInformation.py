from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLineEdit

from Config import Config
from designerFiles.DesignerDBInformation import Ui_DBWindow
from fileHandler import updateConfig, readConfigFile

# Constante to check License feature
license = "externaldb"

iconPicturePath = "./GUI/pictures/icon.png"


class DBWindow(QtWidgets.QMainWindow):
    """
    Class DBInformation to show a window where a database connection can be saved or reset
    """

    def __init__(self, parent: QtWidgets.QMainWindow, config: Config):
        """
         Constructor
        :param   : MainWindow
        """
        super().__init__()

        self.parent = parent
        self.ui = Ui_DBWindow()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.ui.dbhostinput.setText(config.networkDatabaseAddress)
        self.ui.dbdatabaseinput.setText(config.networkDatabase)
        self.ui.dbpasswordinput.setText(config.networkDatabasePassword)
        self.ui.dbportinput.setText(str(config.networkDatabasePort))
        self.ui.dbuserinput.setText(config.networkDatabaseUser)

        self.ui.abbrechdbbutton.clicked.connect(self.closeDBWindow)
        self.ui.savedbbutton.clicked.connect(self.speichernClicked)
        self.ui.savelicensebutton.clicked.connect(self.activateLicense)

        self.ui.dbpasswordinput.setEchoMode(QLineEdit.Password)

        # License feature, everything inside Frame will be hidden
        frame = self.ui.frame
        hiddenlayout = self.ui.gridLayout_3
        frame.setLayout(hiddenlayout)
        self.ui.gridLayout.addWidget(frame)

        if license == "externaldb":
            # Feature acquired
            frame.show()
            self.ui.notlicensedlabel.setVisible(False)
            self.ui.savelicenselineedit.setVisible(False)
            self.ui.savelicenselabel.setVisible(False)
            self.ui.savelicensebutton.setVisible(False)

        else:
            # Feature denied
            frame.hide()
            self.ui.notlicensedlabel.setVisible(True)
            self.ui.savelicenselabel.setVisible(True)
            self.ui.savelicenselineedit.setVisible(True)
            self.ui.savelicensebutton.setVisible(True)

        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        DBWindow.setWindowIcon(self, icon)

    def speichernClicked(self):
        """
        Method to save inputs and send it to database controller
        """
        config = readConfigFile()

        host = self.ui.dbhostinput.text()
        port = self.ui.dbportinput.text()
        user = self.ui.dbuserinput.text()
        password = self.ui.dbpasswordinput.text()
        database = self.ui.dbdatabaseinput.text()

        if (
            config.networkDatabaseAddress == host
            and config.networkDatabaseUser == user
            and config.networkDatabase == database
            and str(config.networkDatabasePort) == port
            and config.networkDatabasePassword == password
        ):
            self.close()
            return

        if self.parent.questionnaireController.database.databaseMySQL:
            if self.parent.questionnaireController.database.databaseMySQL.connected:
                self.parent.questionnaireController.database.disconnectFromExtern()

        if host and port and user and password and database:
            updateConfig("NetworkDatabaseAddress", host, "DATABASE")
            updateConfig("NetworkDatabasePort", port, "DATABASE")
            updateConfig("NetworkDatabaseUser", user, "DATABASE")
            updateConfig("NetworkDatabasePassword", password, "DATABASE")
            updateConfig("NetworkDatabase", database, "DATABASE")
            config = updateConfig("UseNetworkDatabase", "yes", "DATABASE")
            try:
                self.parent.questionnaireController.database.connectToExtern(
                    host=config.networkDatabaseAddress, port=config.networkDatabasePort, user=config.networkDatabaseUser, password=config.networkDatabasePassword, database=config.networkDatabase
                )
                success = True
            except Exception as e:
                self.parent.popUp("Warnung", "Konnte keine Verbindung zur Datenbank aufbauen.")
                success = False
            if success:
                self.close()
        else:
            box = QtWidgets.QMessageBox()
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setWindowTitle("Anamnesebögen - Warnung")
            box.setText("Es wurden nicht alle benötigten Informationen eingegeben.")
            icon = QIcon()
            icon.addPixmap(QPixmap("GUI/icon.png"), QIcon.Normal, QIcon.Off)
            box.setWindowIcon(icon)
            box.exec_()

    def closeDBWindow(self):
        """
        Method to close the window if Abbrechen button is pushed
        """
        host = self.ui.dbhostinput.text()
        port = self.ui.dbportinput.text()
        user = self.ui.dbuserinput.text()
        password = self.ui.dbpasswordinput.text()
        database = self.ui.dbdatabaseinput.text()

        if host or port or user or password or database:
            box = QtWidgets.QMessageBox()
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setWindowTitle("Anamnesebögen - Abbrechen")
            box.setText("Alle Änderungen werden verworfen.\nWirklich abbrechen?")
            box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            icon = QIcon()
            icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
            box.setWindowIcon(icon)
            buttonY = box.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText("Ja")
            buttonN = box.button(QtWidgets.QMessageBox.No)
            buttonN.setText("Nein")
            box.exec_()

            if box.clickedButton() == buttonY:
                self.close()
        else:
            self.close()

    def showDBInfo(self, config: Config):
        """
        Method that shows the saved database information in the left part of DBWindow
        """
        self.ui.dbactive_namelabel.setText(config.networkDatabase)
        self.ui.dbactive_adresslabel.setText(config.networkDatabaseAddress)
        self.ui.dbactive_portlabel.setText(config.networkDatabasePort)
        self.ui.dbactive_userlabel.setText(config.networkDatabaseUser)

    def activateLicense(self, license):
        """
        Method to save license input
        """
        license = self.ui.savelicenselineedit

        return license
