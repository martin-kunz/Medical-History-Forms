import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout

import QuestionType
from Question import Question
from QuestionCategory import QuestionCategory
from designerFiles.DesignerSaveQuestion import Ui_MainWindow

iconPicturePath = "./GUI/pictures/icon.png"
plusPicturePath = "GUI/pictures/plus.png"
xPicturePath = "GUI/pictures/x.png"


class SaveQuestion(QtWidgets.QMainWindow):
    """
    Class SaveQuestion to show window where a new question can be created or an existing one can be edited

    """

    RowPositionOptions = 4

    def __init__(self, parent: QtWidgets.QMainWindow, question: Question = None, parentLibrary: QtWidgets.QMainWindow = None, position: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Constructor
        :param parent: Here MainFrame
        :param question: Question we want to save
        :param parentLibrary: Library
        :param position: If the user wants to edit an unsaved question we need this position to find the related question later
        """

        self.setWindowModality(Qt.ApplicationModal)

        self.parent = parent
        self.library = parentLibrary
        self.position = position

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.allQuestionTypes = self.parent.questionTypes

        self.currentQuestion = question

        self.btnadd = QPushButton()
        self.icon_button = QIcon(plusPicturePath)
        self.btnadd.setIcon(self.icon_button)

        self.icon_button = QIcon(xPicturePath)
        self.btnremove = QPushButton()
        self.btnremove.setIcon(self.icon_button)

        self.btnadd.clicked.connect(self.add_field)

        self.ui.AbbrechButton.clicked.connect(self.cancelClicked)
        self.ui.SpeicherButton.clicked.connect(self.saveQuestion)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        SaveQuestion.setWindowIcon(self, icon)

        self.ui.lineEdit_beschreibung.setPlaceholderText("Pflichtfeld")
        self.ui.lineEdit_kurzbeschreibung.setPlaceholderText("Pflichtfeld")

        # Fill questiontypes combobox
        for types in self.parent.questionController.types:
            self.ui.comboBox_fragentyp.addItem(types.displayName)

        # Fill categories combobox
        for category in self.parent.questionController.categories():
            self.ui.comboBox_kategorie.addItem(category.category)

        # Fill relatedQuestioncombobox
        self.ui.dropdown_relatedQuestion.addItem("")
        for relatedQuestion in self.parent.questionController.questions():
            if len(relatedQuestion.options) != 0:
                self.ui.dropdown_relatedQuestion.addItem(relatedQuestion.abbreviation)

        # InstallEventFilter on relatedquestion combobox
        self.ui.dropdown_relatedQuestion.currentIndexChanged.connect(self.relatedQuestionChanged)
        self.ui.comboBox_fragentyp.currentIndexChanged.connect(self.questionTypeChanged)

        if self.currentQuestion is None:
            self.createNoOptions()
            self.ui.comboBox_fragentyp.setCurrentIndex(2)
        else:
            self.ui.comboBox_kategorie.setCurrentIndex(self.currentQuestion.category.id - 1)
            self.ui.comboBox_fragentyp.setCurrentIndex(self.currentQuestion.type.id - 1)
            self.ui.lineEdit_beschreibung.setText(question.text)
            self.ui.lineEdit_kurzbeschreibung.setText(question.abbreviation)

            if len(self.currentQuestion.options) > 0:
                self.createWithOptions()
                # Insert first text
                self.options[0].setText(self.currentQuestion.options[0])
                # Add options field and insert text
                for i in range(1, len(self.currentQuestion.options)):
                    self.add_field()
                    self.options[i].setText(self.currentQuestion.options[i])
            # Question necessary
            if self.currentQuestion.required:
                self.ui.checkBox_pflichtfrage.setChecked(True)
            else:
                self.ui.checkBox_pflichtfrage.setChecked(False)
            # Question allows comment
            if self.currentQuestion.comment:
                self.ui.checkBox_kommentar.setChecked(True)
            else:
                self.ui.checkBox_kommentar.setChecked(False)
            # Question allows score
            if self.currentQuestion.score:
                self.ui.checkBox_auswertbar.setChecked(True)
            else:
                self.ui.checkBox_auswertbar.setChecked(False)
            # Dependent on Question
            if self.currentQuestion.dependent_on != "none":
                index = self.ui.dropdown_relatedQuestion.findText(self.currentQuestion.dependent_on)
                self.ui.dropdown_relatedQuestion.setCurrentIndex(index)
                self.relatedQuestionChanged()

                # Set the right index for expected answer
                index = self.ui.dropdown_necessaryAnswer.findText(self.currentQuestion.expected_answer)
                self.ui.dropdown_necessaryAnswer.setCurrentIndex(index)
            else:
                self.ui.dropdown_relatedQuestion.setCurrentIndex(0)

    def createNoOptions(self):
        """
        Changes the design to fit a selection without options
        """
        length = self.ui.formLayout.rowCount()
        # Delete all entries in options
        self.options = []
        # Delte all rows with options
        while length > 9:
            self.ui.formLayout.removeRow(4)
            length -= 1

    def createWithOptions(self):
        """
        Changes the design to fit a selection with options
        """
        # Clear everything to be sure
        self.createNoOptions()
        # List to save the QLineEdits for options
        self.options = []

        self.btnadd = QPushButton()
        self.icon_button = QIcon(plusPicturePath)
        self.btnadd.setIcon(self.icon_button)

        # First option without minus
        self.optiontext = QLineEdit(self)
        self.options.append(self.optiontext)

        self.btnadd.clicked.connect(self.add_field)

        self.layout_first_option = QHBoxLayout()
        self.layout_first_option.addWidget(self.optiontext)
        self.layout_first_option.addWidget(self.btnadd)

        self.ui.formLayout.insertRow(self.RowPositionOptions, "Optionen:", self.layout_first_option)

    def cancelClicked(self):
        """
        Closes the window
        """
        self.close()

    def questionTypeChanged(self):
        """
        If the questiontype combobox is changed a signal is emitted and this function is called
        it then changes our design to support our user
        """
        currentQuestionType = self.findQuestionType(self.allQuestionTypes, self.ui.comboBox_fragentyp.currentIndex() + 1)
        if currentQuestionType.options == 1:
            self.createWithOptions()
        else:
            self.createNoOptions()

    def relatedQuestionChanged(self):
        """
        If the related question combobox is changed a signal is emitted and this function is called.
        It then iterates over all questions and finds the possible answers in our answer combobox
        """
        abbrv = self.ui.dropdown_relatedQuestion.currentText()

        questions = self.parent.questionController.questions()

        self.ui.dropdown_necessaryAnswer.clear()

        for question in questions:
            if question.abbreviation == abbrv:
                if question.abbreviation == self.ui.lineEdit_kurzbeschreibung.text():
                    self.parent.popUp("Warnung", "Sie können nicht auf die Frage selbst verweisen!")
                    return
                else:
                    self.ui.dropdown_necessaryAnswer.addItems(question.options)
                    return

    def saveQuestion(self):
        """
        Collects all data from our window and stores them
        into a new question object. Later sends this to its parent
        MainFrame so our Data can be changed there aswell
        """
        description = self.ui.lineEdit_beschreibung.text()
        abbrevation = self.ui.lineEdit_kurzbeschreibung.text()
        requiered = self.ui.checkBox_pflichtfrage.isChecked()
        comment = self.ui.checkBox_kommentar.isChecked()
        score = self.ui.checkBox_auswertbar.isChecked()
        dependent_on = self.ui.dropdown_relatedQuestion.currentText()
        expected_answer = self.ui.dropdown_necessaryAnswer.currentText()

        if (not description) | (not abbrevation):
            self.parent.popUp("Warnung", "Notwendige Felder nicht gefüllt")
            return

        options = []
        for option in self.options:
            if not option.text():
                self.parent.popUp("Warnung", "Eins der Optionsfelder ist derzeitig leer!")
                return
            else:
                options.append(option.text())

        # Fill empty fields with None
        if not dependent_on:
            dependent_on = "none"
        # Fill empty fields with None
        if not expected_answer:
            expected_answer = "none"

        # Question = None -> no ID -> -1
        if self.currentQuestion is None:
            ids = -1
        else:
            ids = self.currentQuestion.id

        newQuestionType = self.findQuestionType(self.allQuestionTypes, self.ui.comboBox_fragentyp.currentIndex() + 1)
        newQuestionCategory = self.findCategory(self.ui.comboBox_kategorie.currentText())
        newQuestion = Question(
            text=description,
            type=newQuestionType,
            options=options,
            required=requiered,
            dependent_on=dependent_on,
            expected_answer=expected_answer,
            abbreviation=abbrevation,
            score=score,
            comment=comment,
            id=ids,
            category=newQuestionCategory,
        )

        # If the question is imported but not saved
        if self.currentQuestion is not None:
            if self.currentQuestion.id == -1:
                self.parent.editImportedQuestion(newQuestion, self.position)
                self.close()
                return

        self.parent.editQuestionItem(newQuestion)
        if self.library is not None:
            self.library.updateAll()
        self.close()

    def add_field(self):
        # Insert first Row with delete Button and delete prior row
        priorOption = self.options.pop(self.RowPositionOptions - 4)
        priorOptionText = priorOption.text()
        self.ui.formLayout.removeRow(self.RowPositionOptions)

        # Layoutoptions with minus, objects have to be recreated because of removeRow
        btnremove = QPushButton()
        btnremove.clicked.connect(self.remove_field)
        icon_button = QIcon(xPicturePath)
        btnremove.setIcon(icon_button)

        option = QLineEdit()
        option.setText(priorOptionText)

        layout_options_minus = QHBoxLayout()
        layout_options_minus.addWidget(option)
        layout_options_minus.addWidget(btnremove)

        self.options.append(option)

        self.ui.formLayout.insertRow(self.RowPositionOptions, "Optionen:", layout_options_minus)

        # Increase the rowCount and create the necessary layoutoption with plus and minus
        self.RowPositionOptions += 1

        icon_button = QIcon(xPicturePath)
        btnremove = QPushButton()
        btnremove.setIcon(icon_button)
        btnremove.clicked.connect(self.remove_field)

        btnadd = QPushButton()
        icon_button = QIcon(plusPicturePath)
        btnadd.setIcon(icon_button)

        option = QLineEdit()

        layout_last_options = QHBoxLayout()
        layout_last_options.addWidget(option)
        layout_last_options.addWidget(btnadd)
        layout_last_options.addWidget(btnremove)
        btnadd.clicked.connect(self.add_field)

        self.ui.formLayout.insertRow(self.RowPositionOptions, "Optionen:", layout_last_options)

        self.options.append(option)

    def remove_field(self):
        """
        3 Cases:
        Delete with only 2 rows left -> Start again
        Delete row in the middle -> delteRow
        Delte lowest row -> second lowest row has to be updated
        """
        sender = self.sender()
        rowToDelete = int(round((sender.pos().y() - 135) / 50)) + 3

        if len(self.options) > 1:
            # Delete last row
            if (rowToDelete == 5) & (len(self.options) == 2) | ((rowToDelete == 4) & (len(self.options) == 2)):
                priorPreOption = self.options.pop(1)
                priorOption = self.options.pop(0)
                priorPreOptionText = priorPreOption.text()
                priorOptionText = priorOption.text()

                btnadd = QPushButton()
                icon_button = QIcon(plusPicturePath)
                btnadd.setIcon(icon_button)

                option = QLineEdit()
                # Add first or last line depending on what line was removed
                if rowToDelete == 5:
                    option.setText(priorOptionText)
                else:
                    option.setText(priorPreOptionText)
                self.options.append(option)

                layout_last_options = QHBoxLayout()
                layout_last_options.addWidget(option)
                layout_last_options.addWidget(btnadd)
                btnadd.clicked.connect(self.add_field)

                # Remove the 2 rows
                self.ui.formLayout.removeRow(self.RowPositionOptions)
                self.ui.formLayout.removeRow(self.RowPositionOptions - 1)

                self.RowPositionOptions -= 1
                self.ui.formLayout.insertRow(self.RowPositionOptions, "Optionen:", layout_last_options)

            elif len(self.options) == rowToDelete - 3:
                icon_button = QIcon(xPicturePath)

                icon_button = QIcon(xPicturePath)
                btnremove = QPushButton()
                btnremove.setIcon(icon_button)
                btnremove.clicked.connect(self.remove_field)

                btnadd = QPushButton()
                icon_button = QIcon(plusPicturePath)
                btnadd.setIcon(icon_button)

                self.options.pop(len(self.options) - 1)
                priorOption = self.options.pop(len(self.options) - 1)
                priorText = priorOption.text()
                option = QLineEdit()
                option.setText(priorText)
                self.options.append(option)

                layout_last_options = QHBoxLayout()
                layout_last_options.addWidget(option)
                layout_last_options.addWidget(btnadd)
                layout_last_options.addWidget(btnremove)
                btnadd.clicked.connect(self.add_field)

                self.ui.formLayout.removeRow(self.RowPositionOptions)
                self.RowPositionOptions -= 1
                self.ui.formLayout.removeRow(self.RowPositionOptions)
                self.ui.formLayout.insertRow(self.RowPositionOptions, "Optionen:", layout_last_options)

            else:
                self.RowPositionOptions -= 1
                self.options.pop(rowToDelete - 4)
                self.ui.formLayout.removeRow(rowToDelete)

    def findQuestionType(self, questionTypes: list, id: int) -> QuestionType:
        """
        Finds the fitting questionType for the id
        :param questionTypes: Types of all questions in our database
        :param id: The index that is selected in our frame
        :return: Returns the type of question
        """
        for type in questionTypes:
            if type.id == id:
                return type

    def findCategory(self, searchedCategory: str) -> QuestionCategory:
        """
        Finds the fitting category
        :param id: The index that is selected in our frame
        :return: Returns the type of question category
        """
        for category in self.parent.questionController.categories():
            if category.category == searchedCategory:
                return category
