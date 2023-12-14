from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from Questionnaire import Questionnaire
from QuestionnaireCategory import QuestionnaireCategory
from designerFiles.DesignerSaveQuestionnaire import Ui_MainWindow

iconPicturePath = "./GUI/pictures/icon.png"


class SaveQuestionnaire(QtWidgets.QMainWindow):
    """
    Class SaveQuestionnaire to show a dialog window to save a new Questionnaire
    """

    def __init__(self, parent: QtWidgets.QMainWindow, questionnaire: Questionnaire = None, parentLibrary: QtWidgets.QMainWindow = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Constructor
        :param parent: Here MainFrame
        :param questionnaire: Questionnaire we want to save
        :param parentLibrary: Library
        """

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)

        self.parent = parent
        if questionnaire:
            self.questionnaire = questionnaire
        else:
            self.questionnaire = Questionnaire(parent.questionnaireController.getDefaultCategory())

        self.library = parentLibrary

        self.ui.abbrechButton.clicked.connect(self.cancelClicked)
        self.ui.speicherButton.clicked.connect(self.saveClicked)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        SaveQuestionnaire.setWindowIcon(self, icon)

        self.ui.lineEdit_name.setPlaceholderText("Pflichtfeld")

        for category in self.parent.questionnaireController.categories():
            self.ui.comboBox_kategorie.addItem(category.category)

        if self.questionnaire is not None:
            self.ui.comboBox_kategorie.setCurrentIndex(self.questionnaire.category.id - 1)
            self.ui.lineEdit_name.setText(self.questionnaire.name)
            self.ui.lineEdit_beschreibung.setText(self.questionnaire.description)

    def cancelClicked(self):
        """
        Method that closes window and warns before closing, because of unsaved changes
        """
        self.close()

    def saveClicked(self):
        """
        When the user clicks save this method is called. It then reads the necessary data and
        sends the new questionnaire to our Mainframe to save it. Our library will get updated if
        necessary.
        """
        self.questionnaire.name = self.ui.lineEdit_name.text()
        self.questionnaire.description = self.ui.lineEdit_beschreibung.text()

        if not self.questionnaire.name:
            box = QtWidgets.QMessageBox()
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setWindowTitle("Anamnesebögen - Warnung")
            box.setText("Zum Speichern muss ein Name eingeben werden.")
            icon = QIcon()
            icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
            box.setWindowIcon(icon)
            box.exec_()
            return

        self.questionnaire.category = self.findCategory(self.ui.comboBox_kategorie.currentText())
        if self.library != None:
            self.parent.saveQuestionnaireRecieve(self.questionnaire)
            self.library.updateAll()
        else:
            self.parent.saveQuestionnaireRecieve(self.questionnaire, 1)
        self.close()

    def findCategory(self, name: str) -> QuestionnaireCategory:
        """
        Finds the corresponding category to a given name
        :param name: The name of the questionnaire category we want to find
        :return: The QuestionCategory inside our database with the given name
        """
        for category in self.parent.questionnaireController.categories():
            if category.category == name:
                return category
