class QuestionType:
    """
    Class representing the type attribute of a question.
    """

    def __init__(self, typeName: str, options: bool, displayName, id: int = -1):
        """
        Constructor
        :param typeName: Question type
        :param options: Indication of whether the question type allows options
        :param displayName: Name that is visible to the user
        :param id: Question ID
        """
        self.typeName = typeName
        self.options = options
        self.displayName = displayName
        self.id = id
