from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from QuestionnaireCategory import QuestionnaireCategory
from designerFiles.DesignerSaveCategoryQA import Ui_MainWindow

iconPicturePath = "./GUI/pictures/icon.png"


class SaveCategoryQA(QtWidgets.QMainWindow):
    """
    Class SaveCategory to show window that asks to save a new Category
    """

    def __init__(self, parent: QtWidgets.QMainWindow, parentLibrary: QtWidgets.QMainWindow = None, category: QuestionnaireCategory = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Constructor
        :param parent: Here MainFrame
        :param parentLibrary: Library
        :param category: All categories in our database
        """
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)

        if category:
            self.ui.label.setText("Kategorie für Fragenkataloge bearbeiten")
        else:
            self.ui.label.setText("Neue Kategorie für Fragenkataloge hinzufügen")

        self.currentCategory = category

        self.parent = parent

        self.library = parentLibrary

        self.categories = self.parent.questionController.categories()

        self.ui.abbrechButton.clicked.connect(self.abbrechenClicked)
        self.ui.speicherButton.clicked.connect(self.speichernClicked)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        SaveCategoryQA.setWindowIcon(self, icon)

        self.ui.lineEdit_name.setPlaceholderText("Pflichtfeld")

        if self.currentCategory != None:
            self.ui.lineEdit_beschreibung.setText(self.currentCategory.description)
            self.ui.lineEdit_name.setText(self.currentCategory.category)

    def abbrechenClicked(self):
        """
        Method that closes window and warns before closing, because of unsaved changes
        """
        self.close()

    def speichernClicked(self):
        """
        Method to save a new category and close the window
        """
        name = self.ui.lineEdit_name.text()
        description = self.ui.lineEdit_beschreibung.text()
        id = None
        if self.currentCategory != None:
            id = self.currentCategory.id

        if name:
            if name == "Allgemein":
                self.parent.popUp("Warnung", "Es darf keine Kategorie mit dem Namen Allgemein gespeichert werden.")
                return
            if id is None:
                newQuestionnaireCategory = QuestionnaireCategory(name=name, description=description)
                self.parent.questionnaireController.addQuestionnaireCategory(newQuestionnaireCategory)
            else:
                newQuestionnaireCategory = QuestionnaireCategory(name=name, description=description, id=id)
                self.parent.questionnaireController.editQuestionnaireCategory(newQuestionnaireCategory)

            self.library.updateAll()
            self.close()
        else:
            self.parent.popUp()
            box = QtWidgets.QMessageBox("Anamnesebögen - Warnung", "Bitte geben Sie einen gültigen Namen ein!")
            return
