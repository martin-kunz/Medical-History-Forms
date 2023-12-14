import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog

from designerFiles.DesignerRestoreSession import Ui_RestoreSession

iconPicturePath = "./GUI/pictures/icon.png"


class RestoreSession(QDialog):
    """
    class RestoreSession to show a window that pops up on program start when there exists a session file and asks if the old session should be restored or not
    """

    def __init__(self):
        """
        Constructor
        :param parent QDialog
        """
        super().__init__()

        self.ui = Ui_RestoreSession()
        self.ui.setupUi(self)

        self.ui.sessionrestoreButtonYes.clicked.connect(self.restoreSession)
        self.ui.sessionrestoreButtonNo.clicked.connect(self.resumeNormalStart)

        # Import Icon
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPicturePath), QIcon.Normal, QIcon.Off)
        RestoreSession.setWindowIcon(self, icon)

    def restoreSession(self):
        """
        Method returns true if Ja button is clicked
        """
        self.setResult(1)
        self.accept()
        return True

    def resumeNormalStart(self):
        """
        Method returns false if No button is clicked
        """
        self.setResult(0)
        self.done(self.result())
        return False
