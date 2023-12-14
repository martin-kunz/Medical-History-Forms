from Question import Question
from QuestionController import QuestionController
from QuestionnaireController import QuestionnaireController


class QuestionObserver:
    """
    Class to process changes on single questions for updating the active questionnaire.
    """

    def __init__(self, observedController: QuestionController, questionnaireController: QuestionnaireController):
        """
        Constructor
        :param observedController: the questionController observed by this observer
        :param questionnaireController: the questionnaireController that needs to be informed about changes
        """
        self.observedController = observedController
        self.questionnaireController = questionnaireController

    def update(self, question: Question):
        """
        Method to inform the connected questionnaireController about changes on a certain question
        :param question: the changed question
        :return:
        """
        self.questionnaireController.updateQuestion(question)
