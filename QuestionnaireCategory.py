class QuestionnaireCategory:
    """
    Class represents the intern structure for questionnaire categories
    """

    def __init__(self, name: str, description: str, id: int = -1):
        """
        Constructor
        :param name: the name of the category
        :param description: Description of the category
        :param id: the ID of the category
        """
        self.category = name
        self.description = description
        self.id = id
