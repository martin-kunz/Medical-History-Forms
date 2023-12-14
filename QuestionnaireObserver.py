import QuestionnaireController
from fileHandler import writeToSessionFile


class QuestionnaireObserver:
    """
    Class to process changes on connected questionnaireController's questionnaire. Used for session back ups.
    """

    def __init__(self, observedController: QuestionnaireController):
        self.observedController = observedController

    def update(self):
        """
        Method to redirect changes of the observed questionnaire to the fileHandler for the session file.
        :return:
        """
        writeToSessionFile(self.observedController.questionnaire)
