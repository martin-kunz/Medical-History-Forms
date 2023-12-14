import os
import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem, QListWidgetItem, QMainWindow

from designerFiles.DesignerMainFrame import Ui_MainWindow
from GUI.Library import Library
from GUI.SaveQuestion import SaveQuestion
from GUI.SaveQuestionnaire import SaveQuestionnaire
from GUI.SaveCategoryQ import SaveCategory
from GUI.SaveCategoryQA import SaveCategoryQA
from GUI.HelpWindow import HelpWindow
from GUI.DBInformation import DBWindow
from GUI.ChooseQA import ChooseQAWindow
from GUI.WarningAbbrv import WarningAbbrv
from Question import Question
from QuestionCategory import QuestionCategory
from Questionnaire import Questionnaire
from QuestionnaireController import QuestionnaireController
from QuestionController import QuestionController
from fileHandler import readConfigFile

# Icon path
iconPicturePath = "./GUI/pictures/icon.png"
arrowLeftPicPath = "GUI/pictures/arrow-left.png"
arrowRightPicPath = "GUI/pictures/arrow-right.png"

MAIN_WINDOW = 1


class CustomTreeItem(QTreeWidgetItem):
    """
    Class custom QTreeWidgetItem with Widgets to represent our Data in TreeWidget
    """

    def __init__(self, parent, parentFrame: QMainWindow, data: Question):
        """
        Constructor
        :param parent       : Item's QTreeWidget or Question.
        :param parentFrame  : The frame where the item gets created, here MainFrame
        :param data         : Question
        """
        # Init super class ( QtGui.QTreeWidgetItem )
        super(CustomTreeItem, self).__init__(parent)

        self.question = data
        self.updateItem()

        self.parentFrame = parentFrame

        if self.parent() is None:
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
        else:
            self.setFlags(Qt.ItemIsEnabled)

    @property
    def returnText(self):
        """
        :return: str
        """
        return self.thisQuestion.text

    def returnQuestion(self):
        """
        :return: question
        """
        return self.question

    def removeAllChildren(self):
        """
        Remove all children of the called QTreeWidgetItem
        """
        for i in reversed(range(self.childCount())):
            self.removeChild(self.child(i))

    def updateItem(self):
        """
        Inserts the text in the right columns and rows(right side)
        """
        self.removeAllChildren()
        if self.parent() is None:
            description = "[" + self.question.abbreviation + "] "
            description += self.question.text
            if self.question.dependent_on != "none":
                description += " (" + self.question.dependent_on + " -> " + self.question.expected_answer + ")"
            self.setText(0, description)

        if self.question.options:
            if len(self.question.options[0]) > 0:
                for answer in self.question.options:
                    item = QTreeWidgetItem(self, ["> " + answer])
                    item.setFlags(Qt.NoItemFlags)
                    self.addChild(item)


class CustomListItem(QListWidgetItem):
    """
    Class custom QListWidgetItem to display our data in our list(left side)
    """

    def __init__(self, data: Question):
        """
        Constructor
        :param data    : Question
        """
        # Init super class ( QtGui.QListWidgetItem )
        super(CustomListItem, self).__init__()

        self.question = data

        self.setText(data.text)

        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

    def returnText(self) -> str:
        """
        :return: str
        """
        return self.text()

    def returnQuestion(self) -> Question:
        """
        :return: Question
        """
        return self.question.text


class MainFrame(QtWidgets.QMainWindow):
    """
    class MainFrame to build GUI and connect GUI elements with variables
    """

    def __init__(self, questionnaireController: QuestionnaireController, questionController: QuestionController):
        """
        Constructor
        :param questionnaireController  : QuestionnaireController from config
        :param questionController       : QuestionController from config
        """
        super().__init__()
        """
        Constructor
        """

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.questionnaireController = questionnaireController
        self.questionController = questionController

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        MainFrame.setWindowIcon(self, icon)
        Library.setWindowIcon(self, icon)

        # Set the default values for the names
        self.setCategoryName()
        self.setQuestionnaireName()

        # Connect buttons to functions
        self.ui.MainNeueFrageButton.clicked.connect(self.newQuestion)
        self.ui.MainImportButton.clicked.connect(self.importQA)
        self.ui.MainExportButton.clicked.connect(self.exportQA)
        self.ui.MainAbbrechenButton.clicked.connect(self.cancelClicked)
        self.ui.MainSpeichernButton.clicked.connect(self.saveClicked)
        self.ui.MainLibraryButton.clicked.connect(self.openLib)
        self.ui.mainAddfromListButton.clicked.connect(self.addQuestionFromListToTree)
        self.ui.mainopenqabutton.clicked.connect(self.openChooseQA)
        self.ui.mainedittreebutton.clicked.connect(self.editQuestionClicked)
        self.ui.mainDelfromTreeButton.clicked.connect(self.removeQuestionClicked)
        self.ui.maindeletetreebutton.clicked.connect(self.deleteSelectedQuestion)

        # Connection MainFrame to library
        self.ui.actionNeue_Frage_erstellen.triggered.connect(lambda: self.newQuestion())
        self.ui.actionNeue_Kategorie_erstellen.triggered.connect(lambda: self.newQCat())
        self.ui.actionNeuen_Fragebogen_erstellen.triggered.connect(lambda: self.saveClicked())
        self.ui.actionNewQuestionnaireCategory.triggered.connect(lambda: self.newQACat())
        self.ui.actionDatenbank_anzeigen_hinzuf_gen.triggered.connect(lambda: self.openDB())
        self.ui.actionDatei_importieren.triggered.connect(lambda: self.importQA())
        self.ui.actionFragebogen_exportieren.triggered.connect(lambda: self.exportQA())
        self.ui.actionProgramm_beenden_2.triggered.connect(lambda: sys.exit())
        self.ui.actionFragenbibliothek.triggered.connect(lambda: self.openFBib())
        self.ui.actionFragenkatalogbibliothek.triggered.connect(lambda: self.openFKBib())
        self.ui.actionKategorien.triggered.connect(lambda: self.openKBib())
        self.ui.actionHilfe_ffnen.triggered.connect(lambda: self.openHelp())
        self.ui.actionFragebogen_Kategorien.triggered.connect(lambda: self.openQAKBib())
        self.ui.actionFragebogen_ffnen.triggered.connect(lambda: self.openChooseQA())

        self.ui.MainSearchLine.textChanged.connect(self.updateQuestionList)

        # Button Designs
        icon_button = QIcon(arrowLeftPicPath)
        self.ui.mainAddfromListButton.setIcon(icon_button)
        self.ui.mainAddfromListButton.setIconSize(QSize(35, 40))

        icon_button = QIcon(arrowRightPicPath)
        self.ui.mainDelfromTreeButton.setIcon(icon_button)
        self.ui.mainDelfromTreeButton.setIconSize(QSize(35, 40))

        """Several important UI Settings for our TreeWidget"""
        self.ui.MaintreeWidgetFK.setColumnCount(1)
        self.ui.MaintreeWidgetFK.setSelectionMode(1)
        self.ui.MaintreeWidgetFK.setSelectionBehavior(1)
        self.ui.MaintreeWidgetFK.header().setStretchLastSection(False)
        self.ui.MaintreeWidgetFK.setIndentation(25)
        self.ui.MaintreeWidgetFK.header().setSectionResizeMode(0, 3)
        self.ui.MaintreeWidgetFK.setDragDropMode(3)
        self.ui.MaintreeWidgetFK.header().setSectionsMovable(True)
        self.ui.MaintreeWidgetFK.setExpandsOnDoubleClick(False)

        self.questionTypes = self.questionController.types

        # Fill Dropdown in MainFrame with Categories
        self.updateCategories()

        # Update the Tree
        self.updateTree()
        self.updateQuestionList()

        # Event filters for user action in tree, list and dropdown
        self.ui.MaintreeWidgetFK.viewport().installEventFilter(self)
        self.ui.mainDropdownQList.currentIndexChanged.connect(self.updateQuestionList)
        self.ui.MainlistWidgetFragen.itemDoubleClicked.connect(self.addQuestionFromListToTree)

    def importQA(self, fileName: str = None):
        """
        Imports the selected questionnaire and shows the questions in the tree
        """
        if not fileName:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Anamnesebögen - Fragebogen importieren", "", "Json Files (*.json)", options=options)

        labelname = os.path.basename(fileName)
        labelname = os.path.splitext(labelname)[0]
        self.setQuestionnaireName()
        self.setCategoryName()
        if fileName:
            try:
                self.questionnaireController.importQuestionnaire(Path(fileName))
                self.saveAfterImport()
            except Exception as e:
                self.popUp("Warnung", "Import ist gescheitert, fehlerhafte Datei")

        self.updateTree()
        self.updateQuestionList()
        self.setQuestionnaireName(labelname)

    def saveAfterImport(self):
        """
        Simple Dialog that asks the user if he wants to
        save all the questions and the questionnaire after the import
        """
        errorQuestionList = []
        if self.popUpDialog("Speichern", "Sollen alle Fragen des importierten Fragebogens bereits gespeichert werden?"):
            for question in self.questionnaireController.questionnaire.questions:
                res = self.questionController.saveQuestion(question)
                if not res[0]:
                    errorQuestionList.append(res[1])

        if len(errorQuestionList) > 0:
            self.dialog = WarningAbbrv(self, errorQuestionList)
            self.dialog.show()

    def newQuestion(self):
        """
        Opens new Question window
        """
        self.dialog = SaveQuestion(self)
        self.dialog.show()

    def editQuestionItem(self, newQuestion: Question):
        """
        Receives the changed question from SaveQuestion window
        and implements the changes in our model
        :param newQuestion: Question we want to edit
        """
        self.questionController.saveQuestion(newQuestion)
        self.updateQuestionList()
        self.updateTree()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Is called when the user closes the window
        :param event: QCloseevent
        """
        close = self.popUpDialog("Warnung", "Sind sie sicher, dass Sie die Applikation schließen möchten? Ungespeicherte " "Änderungen werden nicht übernommen.")
        if close:
            event.accept()
        else:
            event.ignore()

    def updateAll(self):
        """
        Updates the tree, list and the searchText
        """
        self.updateTree()
        self.updateQuestionList()
        self.updateText()

    def updateTree(self):
        """
        Updates the tree (left side MainFrame)
        """
        self.ui.MaintreeWidgetFK.clear()
        for question in self.questionnaireController.questionnaire.questions:
            self.addQuestionTreeWidget(question)

    def updateText(self):
        """
        Updates the names for our labels: Name and category
        """
        self.setQuestionnaireName(self.questionnaireController.questionnaire.name)
        self.setCategoryName(self.questionnaireController.questionnaire.category.category)

    def updateCategories(self):
        """
        Updates the categories in the combobox in Mainframe
        """
        self.ui.mainDropdownQList.clear()
        self.ui.mainDropdownQList.addItem("Alle")
        for category in self.questionController.categories():
            self.ui.mainDropdownQList.addItem(category.category)

    def addQuestionList(self, question: Question):
        """
        Add a question to the list(right side of MainFrame)
        :param question: Question
        """
        item = CustomListItem(question)
        self.ui.MainlistWidgetFragen.addItem(item)

    def updateQuestionList(self):
        """
        Updates the list(Right) with all questions or with selected ones
        Also filters this list with the selected category and searchText
        """
        searchText = self.ui.MainSearchLine.text()
        self.ui.MainlistWidgetFragen.clear()
        currentQuestionCategory = self.findCategory(self.ui.mainDropdownQList.currentText())
        questionsList = self.questionController.findByName(searchText, currentQuestionCategory)
        for question in self.questionnaireController.questionnaire.questions:
            for question2 in questionsList:
                if question.id == question2.id:
                    questionsList.remove(question2)
        for question in questionsList:
            self.addQuestionList(question)

    def addQuestionFromListToTree(self, item: CustomListItem = None, question: Question = None, silentMode: bool = False):
        """
        Item catches the case of mouseDoubleClickEvent, sends CustomListWidgetItem
        Adds the selected question from the List(Right) to the Tree(Left).
        If the selcted question has dependencies they will be added aswell, user has to accept
        :param item         : CustomListItem in case of mouseDoubeClickEvent
        :param question     : Question that we want to transfer
        :param silentMode   : Recursive calls no more popups
        """
        if question:
            addQuestion = question
        else:
            if not isinstance(self.ui.MainlistWidgetFragen.currentItem(), CustomListItem):
                return
            addQuestion = self.ui.MainlistWidgetFragen.currentItem().question

        checkDependency = False
        dependentQuestion = None

        if addQuestion.dependent_on != "none":
            checkDependency = True
            dependentQuestion = self.questionController.getDependentQuestion(addQuestion)

        if checkDependency:
            dependencyFulfilled = False
        else:
            dependencyFulfilled = True

        for question in self.questionnaireController.questionnaire.questions:
            if checkDependency:
                if question.abbreviation == dependentQuestion.abbreviation:
                    dependencyFulfilled = True
            if question.abbreviation == addQuestion.abbreviation:
                if question.id != addQuestion.id:
                    self.popUp(title="Warnung", message="Die Kurzbeschreibung ist bereits im Fragenkatalog vergeben!")
                    return

        if not dependencyFulfilled:
            if not silentMode:
                if self.popUpDialog("Warnung", "Ihre ausgewählte Frage ist abhängig von einer anderen. Abhängige Frage " "hinzufügen? Der Vorgang wird andernfalls abgebrochen."):
                    self.addQuestionFromListToTree(question=dependentQuestion, silentMode=True)
                else:
                    return
            else:
                self.addQuestionFromListToTree(question=dependentQuestion, silentMode=True)

        if not self.questionnaireController.addQuestion(newQuestion=addQuestion):
            self.popUp(title="Warnung", message="Frage befindet sich bereits im Fragenkatalog.")
        self.questionnairePosition()
        self.updateQuestionList()

    def popUp(self, title: str, message: str):
        """
        Creates a simple popup
        :param title: Title of the popup
        :param message: custom message inside the popup
        """
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(message)
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        box.setWindowIcon(icon)
        box.exec_()
        return

    def popUpDialog(self, title: str, message: str) -> bool:
        """
        Creates popup With yes or no buttons
        :param title: Title of the popup
        :param message: Custom message
        :return: bool, yes equals true
        """
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(message)
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
            return True
        if box.clickedButton() == buttonN:
            return False

    def editQuestionClicked(self):
        """
        Edits the current selected question in our TreeWidget(left side)
        """
        if self.ui.MaintreeWidgetFK.currentItem() == None:
            return

        itemToEdit = self.ui.MaintreeWidgetFK.currentItem()
        question = itemToEdit.returnQuestion()

        position = self.ui.MaintreeWidgetFK.currentIndex().row()

        self.dialog = SaveQuestion(self, question=question, position=position)
        self.dialog.ui.label.setText("Frage bearbeiten")
        self.dialog.setWindowTitle("Frage bearbeiten")
        self.dialog.show()

    def removeQuestionClicked(self, question: Question = None, silentMode: bool = False):
        """
        Deletes the current selected question in the QTreeWidget(left side)
        :param question: question we want to remove
        :param silentMode: Recursive call no more popups
        """
        if question:
            removeQuestion = question
        else:
            if not isinstance(self.ui.MaintreeWidgetFK.currentItem(), CustomTreeItem):
                return
            removeQuestion = self.ui.MaintreeWidgetFK.currentItem().question

        dependencies = self.questionnaireController.getDependencies(removeQuestion)
        self.questionnairePosition()

        # Question abbrv already exists, warning!
        for question in self.questionController.questions():
            if question.abbreviation == removeQuestion.abbreviation:
                if question.id != removeQuestion.id:
                    self.popUp("Warnung", "Die Kurzbeschreibung ist in der Datenbank bereits vergeben!")
                    return

        if len(dependencies) > 0:
            if not silentMode:
                if self.popUpDialog("Warnung", "Die zu entfernende Frage besitzt andere abhängige Fragen im Fragebogen. Sollen " "diese entfernt werden? Andernfalls wird der Vorgang abgebrochen."):
                    for dependency in dependencies:
                        self.removeQuestionClicked(dependency, True)
                else:
                    return
            else:
                for dependency in dependencies:
                    self.removeQuestionClicked(dependency, True)

        # Identify the question in our questionnaire and delete the question
        for question in self.questionnaireController.questionnaire.questions:
            if question.abbreviation == removeQuestion.abbreviation:
                self.questionnaireController.removeQuestion(question)

                # Case question is not in database Dialog save? (Import)
                if removeQuestion.id == -1:
                    self.editQuestionItem(removeQuestion)

        self.updateQuestionList()
        self.updateTree()

    def deleteSelectedQuestion(self, question: Question = None, silentMode: bool = False):
        """
        Removes the question in the questionnaire. If the question is not in the database it is completely removed
        """
        if question:
            removeQuestion = question
        else:
            if not isinstance(self.ui.MaintreeWidgetFK.currentItem(), CustomTreeItem):
                return
            removeQuestion = self.ui.MaintreeWidgetFK.currentItem().question

        dependencies = self.questionnaireController.getDependencies(removeQuestion)

        if len(dependencies) > 0:
            if not silentMode:
                if self.popUpDialog("Warnung", "Die zu entfernende Frage besitzt andere abhängige Fragen im Fragebogen. Sollen " "diese entfernt werden? Andernfalls wird der Vorgang abgebrochen."):
                    for dependency in dependencies:
                        self.deleteSelectedQuestion(dependency, True)
                else:
                    return
            else:
                for dependency in dependencies:
                    self.deleteSelectedQuestion(dependency, True)

        # Identify the question in our questionnaire and delete the question
        for question in self.questionnaireController.questionnaire.questions:
            if question.abbreviation == removeQuestion.abbreviation:
                self.questionnaireController.removeQuestion(question)

        self.updateQuestionList()
        self.updateTree()

    def addQuestionTreeWidget(self, data: Question):
        """
        Method to add one question to the Tree
        :param data: Question we want to add the questionnaire(left side)
        """
        item = CustomTreeItem(self.ui.MaintreeWidgetFK, self, data)
        self.ui.MaintreeWidgetFK.collapseAll()

    def editImportedQuestion(self, newQuestion: Question, position: int):
        """
        Invoked if the user wants to change a newly imported question without saving the question into the database
        :param newQuestion: The changed question with new values
        :param position: Position of the question in order to find the old question in the questionnaire
        """
        i = 0
        for question in self.questionnaireController.questionnaire.questions:
            if i == position:
                self.questionnaireController.editQuestion(position, newQuestion)
                self.updateTree()
                return
            i += 1

    def cancelClicked(self):
        """
        Clears tree and open new unsaved Questionnaire in main window
        """
        if self.popUpDialog("Abbrechen", "Alle Änderungen im Fragebogen werden verworfen. \nWirklich abbrechen?"):
            self.questionnaireController.setQuestionnaire(Questionnaire(self.questionnaireController.getCategoryByID(1)))
            self.ui.MaintreeWidgetFK.clear()
            self.updateQuestionList()
            self.setCategoryName()
            self.setQuestionnaireName()

    def saveClicked(self):
        """
        Opens save questionnaire window
        """
        self.questionnairePosition()
        self.dialog = SaveQuestionnaire(self, self.questionnaireController.questionnaire)
        self.dialog.show()

    def saveQuestionnaireRecieve(self, questionnaire: Questionnaire, source: int = 0):
        """
        Saves the received questionnaire
        :param questionnaire: The questionnaire we want to save
        :param source: If source == 1, the method was called from the MainFrame, otherwise from the library
        """
        res = self.questionnaireController.saveQuestionnaire(questionnaire=questionnaire)
        if len(res[1]) > 0:
            questionList = res[1]
            self.dialog = WarningAbbrv(self, questionList)
            self.dialog.show()
            return
        if source == MAIN_WINDOW:
            self.questionnaireController.questionnaire = res[0]

        self.setQuestionnaireName(questionnaire.name)
        self.setCategoryName(questionnaire.category.category)

    def exportQA(self, questionnaire: Questionnaire = None):
        """
        Exports the current questionnaire, if a questionnaire is selected in the library
        the current questionnaire has to be overwritten with this one
        """

        if questionnaire != None and isinstance(questionnaire, Questionnaire):
            self.questionnaireController.questionnaire = questionnaire

        if len(self.questionnaireController.questionnaire.questions) == 0:
            self.popUp("Warning", "Sie können keinen leeren Fragebogen exportieren")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Anamnesebögen - Fragebogen exportieren", "", "Json Files (*.json)", options=options)

        """Add .json if missing"""
        if fileName[-5:] != ".json":
            fileName += ".json"

        if fileName:
            try:
                self.questionnaireController.exportQuestionnaire(Path(fileName))
            except:
                self.popUp("Warnung", "Fragenkatalog konnte nicht exportiert werden.")

    def setQuestionnaireName(self, name="ungespeichert"):
        """
        Sets the name of questionnaire in main window to name of the imported file
        :param name: The name that gets displayed for our questionnaire
        """
        self.ui.MainFragebogenLabel.setText("Fragebogen: " + name)

    def setCategoryName(self, name="ohne Kategorie"):
        """
        method sets name of the category in main window to the given category name
        :param name: Name of the category our questionnaire relates to
        """
        self.ui.MainKategorieLabel.setText("Kategorie: " + name)

    def openLib(self):
        """
        Opens Library through Bibliotheks button in MainFrame in Tab Fragen
        """
        self.dialog = Library(self)
        self.dialog.show()

    # Menubar
    def openFBib(self):
        """
        Opens library with tab 1 Fragen through menu bar point
        """
        self.dialog = Library(self)
        self.dialog.ui.libraryTabs.setCurrentIndex(0)
        self.dialog.show()

    def openFKBib(self):
        """
        Opens library with tab 0 Fragebögen through menu bar point
        """
        self.dialog = Library(self)
        self.dialog.ui.libraryTabs.setCurrentIndex(1)
        self.dialog.show()

    def openKBib(self):
        """
        Opens library with tab 2 Fagen-Kategorien through menu bar point
        """
        self.dialog = Library(self)
        self.dialog.ui.libraryTabs.setCurrentIndex(2)
        self.dialog.show()

    def openQAKBib(self):
        """
        Opens library with tab 4 Fragebogen-Kategorien through menu bar point
        """
        self.dialog = Library(self)
        self.dialog.ui.libraryTabs.setCurrentIndex(3)
        self.dialog.show()

    def openHelp(self):
        """
        Opens help window through menu bar point
        """
        self.dialog = HelpWindow()
        self.dialog.show()

    def openDB(self):
        """
        Opens database window through menu bar point
        """
        self.dialog = DBWindow(self, config=readConfigFile())
        self.dialog.show()

    def openChooseQA(self):
        """
        Opens a window to choose an Questionnaire which will be loaded in tree
        """
        self.dialog = ChooseQAWindow(self)
        self.dialog.show()

    def newQCat(self):
        """
        Opens window to add a new category
        """
        self.dialog = SaveCategory(self)
        self.dialog.show()

    def newQACat(self):
        """
        Opens window to add a new category
        """
        self.dialog = SaveCategoryQA(self)
        self.dialog.show()

    def eventFilter(self, source, event):
        """
        This is a eventfilter for our TreeWidget(left)
        :param source: Where the event came from, here always QTreeWidget
        :Param event: Event either drop or mouseDoubleClicked
        :return: Returns the chosen event
        """
        if event.type() == QEvent.Drop:
            event.setDropAction(Qt.MoveAction)
            super().dropEvent(event)
        if event.type() == QEvent.MouseButtonDblClick:
            self.editQuestionClicked()
        return super(MainFrame, self).eventFilter(source, event)

    def questionnairePosition(self):
        """
        Iterates over all questions in our Tree.
        Then sends the current row position and the id to the controller
        """
        nrOfTreeItems = self.ui.MaintreeWidgetFK.topLevelItemCount()
        for i in range(0, nrOfTreeItems):
            treeItem = self.ui.MaintreeWidgetFK.topLevelItem(i)
            self.questionnaireController.swapQuestionPosition(treeItem.question.abbreviation, i)
        self.updateTree()

    def findCategory(self, name: str) -> QuestionCategory:
        """
        Support method that finds the category
        :param name: Name of the category we want to find
        :return: Returns the category the question belongs to
        """
        if name == "Alle":
            return None
        for category in self.questionController.categories():
            if category.category == name:
                return category


"""Stylesheet-file"""
qss = """

QTreeWidget::Item {margin: 5px;}
QListWidget::Item {margin: 2px;}

QPushButton{ 

    background-color: rgb(220,210,200);

    border-style: outset;
    border-width: 1px;
    border-radius: 5px;
    opacity: 50;
    padding: 6px;
}


QPushButton:hover {
    background-color: lightgray;

}



"""
