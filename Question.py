from QuestionCategory import QuestionCategory
from QuestionType import QuestionType


class Question:
    """
    Class representing the intern structure of questions.
    """

    def __init__(
        self,
        text: str,
        type: QuestionType,
        options: list,
        required: bool,
        dependent_on: str,
        expected_answer: str,
        abbreviation: str,
        score: bool,
        comment: bool,
        id: int = -1,
        category: QuestionCategory = None,
    ):
        """
        Constructor
        :param text: Question text, representing the words forming the question
        :param type: Question type
        :param options: Options if question type "select" or "radio"
        :param required: Indication of whether it is a mandatory question
        :param dependent_on: The question this question is dependent on (as abbrv)
        :param expected_answer: The answer on the dependent_on question on which this question is shown
        :param abbreviation: Abbreviation of a question
        :param score: Indication of whether the question can be evaluated
        :param comment: Indication of whether the question can be commented on
        :param id: ID of question
        :param category: Question category
        """
        self.text = text
        self.type = type
        self.options = options
        self.required = required
        self.dependent_on = dependent_on
        self.expected_answer = expected_answer
        self.abbreviation = abbreviation
        self.score = score
        self.comment = comment
        self.id = id
        self.category = category
