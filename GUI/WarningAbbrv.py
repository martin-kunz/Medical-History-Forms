from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTreeWidgetItem

from designerFiles.DesignerWarningAbbrv import Ui_ChooseDBWindow

iconPicturePath = "./GUI/pictures/icon.png"


class WarningAbbrv(QtWidgets.QMainWindow):
    """
    Class WarningAbbrv to show all the questions in case they have to be changed
    """

    def __init__(self, parent: QtWidgets.QMainWindow, questionList: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Constructor
        :param parent: Here MainFrame
        :param questinList: List of all questions with conflicting abbreviation 
        """

        self.ui = Ui_ChooseDBWindow()

        self.ui.setupUi(self)
        self.parent = parent

        self.questionnaire = questionList

        self.ui.closechoosedbbutton.clicked.connect(self.closeClicked)

        self.ui.tableQuestionList.header().setSectionResizeMode(0, 1)
        self.ui.tableQuestionList.header().setSectionResizeMode(1, 1)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        WarningAbbrv.setWindowIcon(self, icon)

        self.setWindowTitle("Anamnesebögen - Warnung")
        self.setTitle(self.questionnaire)
        self.insertQuestions(self.questionnaire)

    def closeClicked(self):
        """
        Method that closes the window
        """
        self.close()

    def setTitle(self, questionList: list):
        """
        Sets the title of the window depending if its one or more questions
        :param questionList: List of questions
        """
        if len(questionList) == 1:
            self.ui.label.setText("Doppelungen gefunden. Ändern sie folgende Kurzbeschreibung, um die Frage zu speichern.")
        else:
            self.ui.label.setText("Doppelungen gefunden. Ändern sie folgende Kurzbeschreibungen, um die Fragen zu speichern.")

    def insertQuestions(self, questionList: list):
        """
        Inserts all the questions in our list
        :param questionList: List of all questions
        """
        for question in questionList:
            item = QTreeWidgetItem()
            item.setText(0, question.text)
            item.setText(1, question.abbreviation)
            self.ui.tableQuestionList.addTopLevelItem(item)
