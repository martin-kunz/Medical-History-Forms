import os
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTreeWidgetItem

from GUI.SaveCategoryQA import SaveCategoryQA
from GUI.SaveQuestion import SaveQuestion
from GUI.SaveQuestionnaire import SaveQuestionnaire
from Question import Question
from QuestionCategory import QuestionCategory
from Questionnaire import Questionnaire
from QuestionnaireCategory import QuestionnaireCategory
from designerFiles.DesignerLibrary import Ui_MainWindow
from GUI.SaveCategoryQ import SaveCategory

iconPicturePath = "./GUI/pictures/icon.png"


class Library(QtWidgets.QMainWindow):
    """
    Constructor
    Library window of our GUI-application
    """

    def __init__(self, parent: QtWidgets.QMainWindow):
        """
        :param parent: Here MainFrame
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)

        self.parent = parent

        # event filter
        self.ui.LibSearchLine.textChanged.connect(self.searchLine)
        self.ui.libraryTabs.currentChanged.connect(self.onChange)

        # Connect buttons with functions
        self.ui.buttonRemoveQTab.clicked.connect(self.removeQ)
        self.ui.buttonEditQTab.clicked.connect(self.editQ)
        self.ui.libNewQeBtn.clicked.connect(self.newQuestion)

        self.ui.buttonRemoveQATab.clicked.connect(self.removeQA)
        self.ui.buttoneditQATab.clicked.connect(self.editQA)
        self.ui.buttonImportQATab.clicked.connect(self.importQA)
        self.ui.buttonExportQATab.clicked.connect(self.export)
        self.ui.libNewQABtn.clicked.connect(self.newQuestionnaire)
        self.ui.buttonOpenQATab.clicked.connect(self.openQAInTree)

        self.ui.buttonRemoveCatTab.clicked.connect(self.removeCat)
        self.ui.buttonEditCatQTab.clicked.connect(self.editCat)
        self.ui.libNewCatBtn.clicked.connect(self.newCategory)

        self.ui.buttonRemoveCatQATab.clicked.connect(self.removeCatQA)
        self.ui.buttonEditCatQATab.clicked.connect(self.editCatQA)
        self.ui.libNewQACatBtn.clicked.connect(self.newCategoryQA)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        Library.setWindowIcon(self, icon)

        # Question Tab UI Settings
        self.ui.tableQTab.setColumnCount(7)
        self.ui.tableQTab.header().setStretchLastSection(False)
        self.ui.tableQTab.doubleClicked.connect(self.editQ)

        self.ui.tableQTab.header().setSectionResizeMode(0, 3)
        self.ui.tableQTab.header().setSectionResizeMode(1, 3)
        self.ui.tableQTab.header().setSectionResizeMode(2, 1)
        self.ui.tableQTab.header().setSectionResizeMode(3, 3)
        self.ui.tableQTab.header().setSectionResizeMode(4, 3)
        self.ui.tableQTab.header().setSectionResizeMode(5, 3)
        self.ui.tableQTab.header().setSectionResizeMode(6, 3)

        # Questionnaire Tab UI Settings
        self.ui.tableQATab.setColumnCount(5)
        self.ui.tableQATab.doubleClicked.connect(self.editQA)

        self.ui.tableQATab.header().setSectionResizeMode(0, 3)
        self.ui.tableQATab.header().setSectionResizeMode(1, 3)
        self.ui.tableQATab.header().setSectionResizeMode(2, 1)
        self.ui.tableQATab.header().setSectionResizeMode(3, 3)
        self.ui.tableQATab.header().setSectionResizeMode(4, 3)

        # Question Category Tab UI Settings
        self.ui.tableCatTab.setColumnCount(2)
        self.ui.tableCatTab.doubleClicked.connect(self.editCat)

        self.ui.tableCatTab.header().setSectionResizeMode(0, 3)
        self.ui.tableCatTab.header().setSectionResizeMode(1, 1)

        # Questionnaire Category Tab UI Settings
        self.ui.tableQACatTab.setColumnCount(2)
        self.ui.tableQACatTab.doubleClicked.connect(self.editCatQA)

        self.ui.tableQACatTab.header().setSectionResizeMode(0, 3)
        self.ui.tableQACatTab.header().setSectionResizeMode(1, 1)

        self.updateAll()

    def onChange(self):
        """
        When the tab is changed the text in the searchLine gets reset.
        Also the automatic selection of items in our lists will get reset after changing a tab.
        """
        self.ui.LibSearchLine.setText("")
        self.ui.tableCatTab.selectionModel().clear()
        self.ui.tableQACatTab.selectionModel().clear()

    # Tab question
    def newQuestion(self):
        """
        Method that opens window to save a new question
        """
        self.dialog = SaveQuestion(self.parent, None, self)
        self.dialog.show()

    def editQ(self):
        """
        Is called when the user wants to edit a question
        """
        if self.ui.libraryTabs.currentIndex() != 0:
            return
        if self.ui.tableQTab.currentItem() is None:
            return

        item = self.ui.tableQTab.currentItem()
        question = item.returnQuestion()

        self.dialog = SaveQuestion(self.parent, question, self)
        self.dialog.show()

    def removeQ(self):
        """
        Called when the user wants to delete a question
        """
        if self.ui.tableQTab.currentItem() is not None:
            removeQuestion = self.ui.tableQTab.currentItem().question
            dependencies = self.parent.questionController.getDependencies(removeQuestion)

            if dependencies:
                if not self.parent.popUpDialog("Warnung", "Die zu entfernende Frage besitzt andere abhängige Fragen. Die Verbindungen werden hiermit entfernt, fortfahren?"):
                    return
            else:
                if not self.parent.popUpDialog("Warnung", "Sind Sie sicher, dass Sie diese Frage löschen möchten?"):
                    return
            for question in self.parent.questionController.questions():
                if question.id == removeQuestion.id:
                    self.parent.questionController.removeQuestion(removeQuestion)
                    self.parent.questionnaireController.removeQuestion(removeQuestion)

                    self.updateAll()
                    self.parent.updateQuestionList()

    # Tab Questionnaire
    def openQAInTree(self):
        """
        Opens the selected questionnaire in our MainFrame
        """
        if self.ui.tableQATab.currentItem() is None:
            return

        selectedQuestionnaire = self.ui.tableQATab.currentItem().returnQuestionnaire()

        if self.parent.popUpDialog("Achtung", "Ungespeicherte Änderungen am derzeitigen Fragebogen werden verworfen. Trotzdem " "Fortfahren?"):
            for questionnaire in self.parent.questionnaireController.getAllQuestionnaires():
                if questionnaire.id == selectedQuestionnaire.id:
                    self.parent.questionnaireController.questionnaire = selectedQuestionnaire
                    # Update MainFrame
                    self.parent.updateAll()
                    self.close()

    def newQuestionnaire(self, questionnaire: Questionnaire = None):
        """
        Opens the new questionnaireWindow
        """
        if questionnaire:
            self.dialog = SaveQuestionnaire(self.parent, questionnaire, self)
        else:
            self.dialog = SaveQuestionnaire(self.parent, None, self)
        self.dialog.show()

    def importQA(self):
        """
        Imports a selected questionnaire into the database
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Anamnesebögen - Fragebogen importieren", "", "Json Files (*.json)", options=options)
        if fileName:
            self.close()
            self.parent.importQA(fileName)

    def export(self):
        """
        Exports a questionnaire to the seleceted path
        """
        if self.ui.tableQATab.currentItem() is not None:
            self.parent.popUp("Warnung", "Der derzeitig offene Fragenkatalog in der Hauptanzeige wird hiermit überschrieben")
            exportQuestionnaire = self.ui.tableQATab.currentItem()
            questionnaire = exportQuestionnaire.returnQuestionnaire()
            self.parent.exportQA(questionnaire)

    def editQA(self):
        """
        Opens the window to edit the selected questionnaire
        """
        if self.ui.libraryTabs.currentIndex() != 1:
            return
        if self.ui.tableQATab.currentItem() is None:
            return

        itemToEdit = self.ui.tableQATab.currentItem()
        questionnaire = itemToEdit.returnQuestionnaire()

        self.dialog = SaveQuestionnaire(self.parent, questionnaire, self)
        self.dialog.show()

    def removeQA(self):
        """
        Removes the selected questionnaire
        """
        if self.ui.tableQATab.currentItem() is None:
            return

        itemToDelte = self.ui.tableQATab.currentItem()
        deleteQuesitonnaire = itemToDelte.returnQuestionnaire()

        if self.parent.popUpDialog("Löschen", "Sind Sie sicher, dass Sie diesen Fragenkatalog löschen möchten?"):
            for questionnaire in self.parent.questionnaireController.getAllQuestionnaires():
                if questionnaire.id == deleteQuesitonnaire.id:
                    self.parent.questionnaireController.remove(questionnaire)

            self.updateAll()
            self.parent.updateTree()
            self.parent.updateQuestionList()

    # Tab categories
    def newCategory(self):
        """
        Opens window to add a new category
        """
        self.dialog = SaveCategory(self.parent, self)
        self.dialog.show()

    def editCat(self):
        """
        Edits the selected questionCategory
        """
        if self.ui.libraryTabs.currentIndex() != 2:
            return
        if self.ui.tableCatTab.currentItem() is None:
            return

        item = self.ui.tableCatTab.currentItem()
        category = item.returnQuestioncategory()

        if category.id == 1:
            self.parent.popUp("Warnung", "Diese Fragenkategorie kann nicht verändert oder entfernt werden.")
            return

        self.dialog = SaveCategory(self.parent, self, category)
        self.dialog.show()

    def removeCat(self):
        """
        Removes the selected questionCategory
        """
        if self.ui.tableCatTab.currentItem() is None:
            return

        itemToDelte = self.ui.tableCatTab.currentItem()
        selectedCategory = itemToDelte.returnQuestioncategory()

        if selectedCategory.id == 1:
            self.parent.popUp("Warnung", "Diese Fragenkategorie kann nicht verändert oder entfernt werden.")
            return
        if self.parent.popUpDialog("Löschen", "Sind Sie sicher, dass Sie diese Kategorie löschen möchten? Alle zugehörigen Fragen werden auf Kategorie Allgemein gesetzt."):
            self.parent.questionController.removeQuestionCategory(selectedCategory)

            self.parent.updateCategories()
            self.updateAll()

    # Tab questionnaireCategories
    def newCategoryQA(self):
        """
        Opens window to add a new category for questionnaires
        """
        self.dialog = SaveCategoryQA(self.parent, self)
        self.dialog.show()

    def editCatQA(self):
        """
        Opens the edit questionnaireCategory window
        """
        if self.ui.libraryTabs.currentIndex() != 3:
            return
        if self.ui.tableQACatTab.currentItem() is None:
            return

        item = self.ui.tableQACatTab.currentItem()
        category = item.returnQuestionnairencategory()

        if category.id == 1:
            self.parent.popUp("Warnung", "Diese Fragebogenkategorie kann nicht verändert oder entfernt werden.")
            return

        self.dialog = SaveCategoryQA(self.parent, self, category)
        self.dialog.show()

    def removeCatQA(self):
        """
        Removes the selceted questionnaireCategory
        """
        if self.ui.tableQACatTab.currentItem() == None:
            return

        itemToDelte = self.ui.tableQACatTab.currentItem()
        selectedCategory = itemToDelte.returnQuestionnairencategory()

        if selectedCategory.id == 1:
            self.parent.popUp("Warnung", "Sind Sie sicher, dass Sie diese Kategorie löschen möchten? Alle zugehörigen Fragen werden auf Kategorie Allgemein gesetzt.")
            return

        if self.parent.popUpDialog("Löschen", "Sind Sie sicher, dass Sie diese Kategorie löschen möchten?"):
            self.parent.questionnaireController.removeQuestionnaireCategory(selectedCategory)
            # Update all necessary windows
            self.updateAll()

    def searchLine(self) -> None:
        """
        Searches in the current selected Tab and adjusts content, based on the data in the list
        """
        searchText = self.ui.LibSearchLine.text()
        if self.ui.libraryTabs.currentIndex() == 0:
            # Search inside questions
            self.searchQTab(searchText)
        elif self.ui.libraryTabs.currentIndex() == 1:
            # Search inside questionnaries
            self.searchQATab(searchText)
        elif self.ui.libraryTabs.currentIndex() == 2:
            # Search inside questionCategories
            self.searchQCategoryTab(searchText)
        else:
            # Search inside questionnaireCategories
            self.searchQACategoryTab(searchText)

    def searchQTab(self, searchText=""):
        """
        Search inside the questionsTab
        """
        if not searchText:
            self.updateAll()
            return

        # Use set to avoid duplicates and improve runTime with larger dataset.
        questions = set()

        # Find all Questions where text fits in one of the first four columns
        items = self.ui.tableQTab.findItems(searchText, QtCore.Qt.MatchContains, 0)
        for item in items:
            questions.add(item.returnQuestion())
        itemTyp = self.ui.tableQTab.findItems(searchText, QtCore.Qt.MatchContains, 1)
        for item in itemTyp:
            questions.add(item.returnQuestion())
        itemDescription = self.ui.tableQTab.findItems(searchText, QtCore.Qt.MatchContains, 2)
        for item in itemDescription:
            questions.add(item.returnQuestion())
        itemAbbrv = self.ui.tableQTab.findItems(searchText, QtCore.Qt.MatchContains, 3)
        for item in itemAbbrv:
            questions.add(item.returnQuestion())

        # cast in order to use our functions (list necessary)
        questions = list(questions)
        self.updateQTab(questions)

    def updateQTab(self, questions: list):
        """
        Updates the question tab after search
        :param questions: List of quesitons we want to update
        """
        self.ui.tableQTab.clear()
        for question in questions:
            item = CustomQTabItem(parent=self.ui.tableQTab, parentFrame=self, data=question)

    def searchQATab(self, searchText=""):
        """
        Search inside the questionnaire tab
        :param searchText: The text we want to filter our list
        """
        if not searchText:
            self.updateAll()
            return

        questionnaires = set()

        items = self.ui.tableQATab.findItems(searchText, QtCore.Qt.MatchContains, 0)
        for item in items:
            questionnaires.add(item.returnQuestionnaire())
        itemName = self.ui.tableQATab.findItems(searchText, QtCore.Qt.MatchContains, 1)
        for item in itemName:
            questionnaires.add(item.returnQuestionnaire())
        itemDescription = self.ui.tableQATab.findItems(searchText, QtCore.Qt.MatchContains, 2)
        for item in itemDescription:
            questionnaires.add(item.returnQuestionnaire())

        questionnaires = list(questionnaires)

        self.updateQATab(questionnaires)

    def updateQATab(self, questionnaires: list):
        """
        Updates the questionnaire tab after search
        :param questionnaires: Questionnaires we want to display
        """
        self.ui.tableQATab.clear()
        for questionnaire in questionnaires:
            item = CustomQATabItem(parent=self.ui.tableQATab, parentFrame=self, data=questionnaire)

    def searchQCategoryTab(self, searchText=""):
        """
        Search inside the questionnaire tab
        :param searchText: The text we want to filter our list
        """
        if not searchText:
            self.updateAll()
            return

        questionCategories = set()

        items = self.ui.tableCatTab.findItems(searchText, QtCore.Qt.MatchContains, 0)
        for item in items:
            questionCategories.add(item.returnQuestioncategory())
        itemName = self.ui.tableCatTab.findItems(searchText, QtCore.Qt.MatchContains, 1)
        for item in itemName:
            questionCategories.add(item.returnQuestioncategory())
        itemDescription = self.ui.tableCatTab.findItems(searchText, QtCore.Qt.MatchContains, 2)
        for item in itemDescription:
            questionCategories.add(item.returnQuestioncategory())

        questionCategories = list(questionCategories)

        self.updateQCategoryTab(questionCategories)

    def updateQCategoryTab(self, questionCategories: list):
        """
        Updates the questionCategory tab after search
        :param questionCategories: Categories of questions we want to display
        """
        self.ui.tableCatTab.clear()
        for questionCategory in questionCategories:
            item = CustomQCatTabItem(parent=self.ui.tableCatTab, parentFrame=self, data=questionCategory)

    def searchQACategoryTab(self, searchText=""):
        """
        Search inside the questionnaire tab
        :param searchText: The text we want to filter our list
        """
        if not searchText:
            self.updateAll()
            return
        questionnaireCategories = set()

        items = self.ui.tableQACatTab.findItems(searchText, QtCore.Qt.MatchContains, 0)
        for item in items:
            questionnaireCategories.add(item.returnQuestionnairencategory())
        itemName = self.ui.tableQACatTab.findItems(searchText, QtCore.Qt.MatchContains, 1)
        for item in itemName:
            questionnaireCategories.add(item.returnQuestionnairencategory())
        itemDescription = self.ui.tableQACatTab.findItems(searchText, QtCore.Qt.MatchContains, 2)
        for item in itemDescription:
            questionnaireCategories.add(item.returnQuestionnairencategory())

        questionnaireCategories = list(questionnaireCategories)
        self.updateQACategoryTab(questionnaireCategories)

    def updateQACategoryTab(self, questionnaireCategories: list):
        """
        Updates the questionCategory tab after search
        :param questionnaireCategories: List of questionnaires categories we want to display
        """
        self.ui.tableQACatTab.clear()
        for questionnaireCategory in questionnaireCategories:
            item = CustomQACatTabItem(parent=self.ui.tableQACatTab, parentFrame=self, data=questionnaireCategory)

    def updateAll(self):
        """
        Updates all the lists
        """
        self.ui.tableQTab.clear()
        questions = self.parent.questionController.questions()

        if questions is not None:
            for question in questions:
                item = CustomQTabItem(parent=self.ui.tableQTab, parentFrame=self, data=question)

        self.ui.tableQATab.clear()
        questionnaires = self.parent.questionnaireController.getAllQuestionnaires()

        if questionnaires is not None:
            for qa in questionnaires:
                item = CustomQATabItem(parent=self.ui.tableQATab, parentFrame=self, data=qa)

        self.ui.tableCatTab.clear()
        qCategories = self.parent.questionController.categories()

        if qCategories is not None:
            for qc in qCategories:
                item = CustomQCatTabItem(parent=self.ui.tableCatTab, parentFrame=self, data=qc)

        self.ui.tableQACatTab.clear()
        qacategories = self.parent.questionnaireController.categories()

        if qacategories is not None:
            for qac in qacategories:
                item = CustomQACatTabItem(parent=self.ui.tableQACatTab, parentFrame=self, data=qac)


class CustomQTabItem(QTreeWidgetItem):
    """
    Custom QTreeWidgetItem with Widgets to represent our Data in Library Tab Fragen
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: Question):
        """
        Constructor
        parent (QTreeWidget)        : Item's QTreeWidget or Question.
        parentFrame (QMainWindow)   : Library
        data (Question)             : Question
        """
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomQTabItem, self).__init__(parent)

        self.question = data

        self.parentFrame = parentFrame

        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.updateItem()

        self.setTextAlignment(0, 1)
        self.setTextAlignment(1, 1)
        self.setTextAlignment(2, 1)
        self.setTextAlignment(3, 1)
        self.setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.setTextAlignment(5, QtCore.Qt.AlignCenter)
        self.setTextAlignment(6, QtCore.Qt.AlignCenter)

    def returnQuestion(self):
        """
        :return: Question
        """
        return self.question

    def updateItem(self):
        """
        Updates the text in our lists
        """
        category = self.question.category.category
        self.setText(0, category)

        qtype = self.question.type.displayName
        self.setText(1, qtype)

        description = self.question.text
        self.setText(2, description)

        abbrv = self.question.abbreviation
        self.setText(3, abbrv)

        if self.question.required:
            required = "X"
        else:
            required = ""
        self.setText(4, required)

        if self.question.comment:
            comment = "X"
        else:
            comment = ""
        self.setText(5, comment)

        if self.question.score:
            score = "X"
        else:
            score = ""
        self.setText(6, score)


class CustomQATabItem(QTreeWidgetItem):
    """
    Custom QTreeWidgetItem to represent our Data in Library Tab Fragebogen
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: Questionnaire):
        """
        Constructor
        parent (QTreeWidget)        : Item's QTreeWidget or Questionnaire.
        parentFrame (QMainWindow)   : Library
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
        self.setTextAlignment(3, 1)
        self.setTextAlignment(4, 1)

    def returnQuestionnaire(self):
        """
        :return: questionnaire
        """
        return self.questionnaire

    def updateItem(self):
        """
        Updates the text in our lists
        """
        category = self.questionnaire.category.category
        self.setText(0, category)

        name = self.questionnaire.name
        self.setText(1, name)

        description = self.questionnaire.description
        self.setText(2, description)

        creationdate = self.questionnaire.creationDate
        self.setText(3, creationdate)

        lastedited = self.questionnaire.lastEdited
        self.setText(4, lastedited)


class CustomQCatTabItem(QTreeWidgetItem):
    """
    Custom QTreeWidgetItem to represent our Data in Library Tab Fragenkategorien
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: QuestionCategory):
        """
        Constructor
        parent (QTreeWidget)        : Item's QTreeWidget or QuestionCategory.
        parentFrame (QMainWindow)   : Library
        data (QuestionCategory)     : QuestionCategory
        """
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomQCatTabItem, self).__init__(parent)

        self.questioncategory = data

        self.parentFrame = parentFrame

        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.updateItem()

        self.setTextAlignment(0, 1)
        self.setTextAlignment(1, 1)

    def returnQuestioncategory(self):
        """
        :return: questioncategory
        """
        return self.questioncategory

    def updateItem(self):
        """
        Updates the text in our lists
        """
        name = self.questioncategory.category
        self.setText(0, name)

        description = self.questioncategory.description
        self.setText(1, description)


class CustomQACatTabItem(QTreeWidgetItem):
    """
    Custom QTreeWidgetItem with Widgets to represent our Data in Library Tab Fragebogenkategorien
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: QuestionnaireCategory):
        """
        Constructor
        parent (QTreeWidget)        : Item's QTreeWidget or QuestionnaireCategory.
        parentFrame (QMainWindow)   : Library
        data (QuestionnaireCategory)     : QuestionnaireCategory
        """
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomQACatTabItem, self).__init__(parent)

        self.questionnairecategory = data

        self.parentFrame = parentFrame

        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.updateItem()

        self.setTextAlignment(0, 1)
        self.setTextAlignment(1, 1)

    def returnQuestionnairencategory(self):
        """
        :return: questionnairecategory
        """
        return self.questionnairecategory

    def updateItem(self):
        """
        Updates the text and buttons in our lists
        """
        name = self.questionnairecategory.category
        self.setText(0, name)

        description = self.questionnairecategory.description
        self.setText(1, description)
