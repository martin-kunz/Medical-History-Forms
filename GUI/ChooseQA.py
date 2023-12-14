from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem

from Questionnaire import Questionnaire
from designerFiles.DesignerChooseQA import Ui_ChooseQAWindow

iconPicturePath = "./GUI/pictures/icon.png"


class ChooseQAWindow(QtWidgets.QMainWindow):
    """
    Class ChooseDBwindow to show a window through Öffnen button in MainFrame in whom a Questionnaire can be chosen and opened in Tree
    """

    def __init__(self, parent: QtWidgets.QMainWindow):
        """
        Constructor
        :param parent  : MainFrame
        """
        super().__init__()

        self.ui = Ui_ChooseQAWindow()
        self.parent = parent
        self.setWindowModality(Qt.ApplicationModal)
        self.ui.setupUi(self)

        self.ui.closechoosedbbutton.clicked.connect(self.closeChooseQAWindow)
        self.ui.choosedbintreebutton.clicked.connect(self.openQAInTree)

        self.ui.tableChooseQA.header().setSectionResizeMode(0, 3)
        self.ui.tableChooseQA.header().setSectionResizeMode(1, 3)
        self.ui.tableChooseQA.header().setSectionResizeMode(2, 1)

        self.insertQA()

        self.setWindowTitle("Anamnesebögen - Fragebogen öffnen")

        # Event filter list
        self.ui.tableChooseQA.doubleClicked.connect(self.openQAInTree)

        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        ChooseQAWindow.setWindowIcon(self, icon)

    def insertQA(self):
        """
        Method that fills the table in the window with questionnaires from db
        """
        self.ui.tableChooseQA.clear()
        questionnaires = self.parent.questionnaireController.getAllQuestionnaires()

        if questionnaires != None:
            for qa in questionnaires:
                item = CustomQATabItem(parent=self.ui.tableChooseQA, parentFrame=self, data=qa)

    def openQAInTree(self):
        """
        Method that opens the selected questionnaire in our MainFrame
        """
        if self.ui.tableChooseQA.currentItem() == None:
            return

        selectedQuestionnaire = self.ui.tableChooseQA.currentItem().returnQuestionnaire()

        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Warning)
        box.setWindowTitle("Achtung")
        box.setText("Ungespeicherte Änderungen am derzeitigen Fragebogen werden verworfen. Fortfahren?")
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
            for questionnaire in self.parent.questionnaireController.getAllQuestionnaires():
                if questionnaire.id == selectedQuestionnaire.id:
                    self.parent.questionnaireController.questionnaire = selectedQuestionnaire

        self.parent.updateAll()
        self.close()

    def closeChooseQAWindow(self):
        """
        Method that closes the ChooseQA window through Abbrechen button
        """
        self.close()


class CustomQATabItem(QTreeWidgetItem):
    """
    Custom QTreeWidgetItem with Widgets to represent our Data in ChooseQA Table Fragebogen
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: Questionnaire):
        """
        Constructor
        parent (QTreeWidget)        : Item's QTreeWidget or Questionnaire.
        parentFrame (QMainWindow)   : MainWindow
        data (Questionnaire)        : Questionnaire
        """
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomQATabItem, self).__init__(parent)

        self.questionnaire = data

        self.parentFrame = parentFrame

        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.updateItem()

        self.setTextAlignment(0, 1)
        self.setTextAlignment(1, 1)
        self.setTextAlignment(2, 1)

    def returnQuestionnaire(self):
        """
        Return questionnaire
        """
        return self.questionnaire

    def updateItem(self):
        """
        Updates the text and buttons in our lists
        """
        category = self.questionnaire.category.category
        self.setText(0, category)

        name = self.questionnaire.name
        self.setText(1, name)

        description = self.questionnaire.description
        self.setText(2, description)
