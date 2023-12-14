class QuestionCategory:
    """
    Class representing the intern structure of question categories.
    """

    def __init__(self, category: str, description: str, id: int = -1):
        """
        Constructor
        :param category: Question category
        :param description: Category description
        :param id: Question ID
        """
        self.category = category
        self.description = description
        self.id = id
