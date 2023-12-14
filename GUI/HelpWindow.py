from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from designerFiles.DesignerHelpWindow import Ui_HelpWindow

iconPicturePath = "./GUI/pictures/icon.png"


class HelpWindow(QtWidgets.QMainWindow):
    """
    Class HelpWindow to show a window with a html file, that explain the features of the software
    """

    def __init__(self):
        """
        Constructor
        parent (QMainWindow) : MainFrame
        """
        super().__init__()

        self.ui = Ui_HelpWindow()

        self.setWindowModality(Qt.ApplicationModal)

        self.ui.setupUi(self)
        # Fenster schließen
        self.ui.helpbutton.clicked.connect(self.closeHelpWindow)

        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        HelpWindow.setWindowIcon(self, icon)

    def closeHelpWindow(self):
        """
        Method to close the help window through Hilfe schließen button
        """
        self.close()
