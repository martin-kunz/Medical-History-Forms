from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from QuestionCategory import QuestionCategory
from designerFiles.DesignerSaveCategoryQ import Ui_MainWindow

iconPicturePath = "./GUI/pictures/icon.png"


class SaveCategory(QtWidgets.QMainWindow):
    """
    Class SaveCategory to show window that asks to save a new Category
    """

    def __init__(self, parent: QtWidgets.QMainWindow, parentLibrary: QtWidgets.QMainWindow = None, category: QuestionCategory = None, *args, **kwargs):
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
            self.ui.label.setText("Kategorie für Fragen bearbeiten")
        else:
            self.ui.label.setText("Neue Kategorie für Fragen hinzufügen")

        self.currentCategory = category

        self.parent = parent

        self.library = parentLibrary

        self.categories = self.parent.questionController.categories()

        self.ui.abbrechButton.clicked.connect(self.abbrechenClicked)

        self.ui.speicherButton.clicked.connect(self.speichernClicked)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        SaveCategory.setWindowIcon(self, icon)

        self.ui.lineEdit_name.setPlaceholderText("Pflichtfeld")

        if self.currentCategory != None:
            self.ui.lineEdit_beschreibung.setText(self.currentCategory.description)
            self.ui.lineEdit_name.setText(self.currentCategory.category)

    def abbrechenClicked(self):
        """
        Method that closes the window
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
                newQuestionCategory = QuestionCategory(category=name, description=description)
                self.parent.questionController.addQuestionCategory(newQuestionCategory)
            else:
                newQuestionCategory = QuestionCategory(category=name, description=description, id=id)
                self.parent.questionController.editQuestionCategory(newQuestionCategory)

            self.parent.updateCategories()
            if self.library is not None:
                self.library.updateAll()

            self.close()
        else:
            box = QtWidgets.QMessageBox()
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.setWindowTitle("physioForms - Warnung")
            box.setText("Bitte geben Sie einen gültigen Namen ein!")
            icon = QIcon()
            icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
            box.setWindowIcon(icon)
            box.exec_()
            return
