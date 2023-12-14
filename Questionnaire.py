import json
import time
from QuestionnaireCategory import QuestionnaireCategory


class Questionnaire:
    """
    Class representing the intern structure of a questionnaire.
    """

    def __init__(
        self, category: QuestionnaireCategory, name: str = "NEU", id: int = -1, description: str = "", questions=None, creationDate=time.strftime("%Y:%m:%d"), lastEdited=time.strftime("%Y:%m:%d")
    ):
        """
        Constructor
        :param category: Questionnaire category
        :param name: Name of the Questionnaire
        :param id: ID of the Questionnaire
        :param description: Description of the Questionnaire
        :param questions: Questions contained in the questionnaire
        :param creationDate: Creation Date
        :param lastEdited: Date of the last change
        """
        if questions is None:
            questions = []
        self.name = name
        self.id = id
        self.description = description
        self.creationDate = creationDate
        self.lastEdited = lastEdited
        self.questions = questions
        self.category = category

    def toJSON(self):
        """
        Questionnaire in JSON
        :return: JSON object
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
