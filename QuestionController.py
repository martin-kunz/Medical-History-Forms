import logging
from Question import Question
from QuestionCategory import QuestionCategory
from DatabaseController import DatabaseController


class QuestionController:
    """
    Class providing all operations connected to question objects
    """

    def __init__(self, database: DatabaseController, logger: logging.Logger, path=None):
        """
        Constructor
        :param database: database
        :param logger: Logger
        :param path: Path
        """
        self.observer = None
        self.database = database
        self.logger = logger
        self.path = path
        self.types = self.database.getTypes()

    def addQuestionCategory(self, newCategory: QuestionCategory) -> [bool, QuestionCategory]:
        """
        Method to add given question category to the database
        :param newCategory: New question category object to be added
        :return: Tuple consisting of True and the new question category if saving was successful
        """
        try:
            cat = self.database.addQuestionCategory(category=newCategory)
            return True, cat
        except Exception as exp:
            self.logger.error(f"Error while adding new question category: {exp}")
            raise

    def editQuestionCategory(self, categoryToBeEdited: QuestionCategory) -> [bool, QuestionCategory]:
        """
        Method to edit a question category
        :param categoryToBeEdited: Question category to be edited
        :return: Tuple consisting of True and the edited question category if editing was successful
        """
        try:
            cat = self.database.editQuestionCategory(category=categoryToBeEdited)
            return True, cat
        except Exception as exp:
            self.logger.error(f"Error while editing a question category: {exp}")
            raise

    def categories(self) -> list:
        """
        Method to get all question categories from the database
        :return: List of question categories from database
        """
        return self.database.getQuestionCategories()

    def findByName(self, key: str, category: QuestionCategory = None) -> list:
        """
        Method to search for a substring / keyword in the question text of questions.
        Also checks if passed for category.
        :param category: If present the category which is filtered else looking in all questions.
        :param key: Keyword that should appear in the question text
        :return: List of questions that contain the keyword
        """
        try:
            filteredQuestions: list = []
            for question in self.questions():
                if category:
                    if key:
                        if question.category.id == category.id:
                            if key.lower() in question.text.lower():
                                filteredQuestions.append(question)
                    else:
                        if question.category.id == category.id:
                            filteredQuestions.append(question)
                else:
                    if key:
                        if key.lower() in question.text.lower():
                            filteredQuestions.append(question)
                    else:
                        filteredQuestions = self.questions()
            return filteredQuestions
        except Exception as exp:
            self.logger.error(f"Error while finding question: {exp}")
            raise

    def getCategoryByID(self, catID: int) -> QuestionCategory:
        """
        Method to get the question category with given id.
        :param catID: Category ID
        :return: Specific category with the associated ID
        """
        try:
            for category in self.categories():
                if category.id == catID:
                    return category
        except Exception as exp:
            self.logger.error(f"Error while getting Question category: {exp}")
            raise

    def getDependencies(self, questionToCheck: Question) -> bool:
        """
        Method to check for existing questions depend on the given one.
        :param questionToCheck: the question to check
        :return: True or False depending on the existence of a depending question
        """
        for question in self.questions():
            if questionToCheck.abbreviation == question.dependent_on:
                return True
        return False

    def getDependentQuestion(self, questionToCheck: Question):
        """
        Method to get a question that given question is dependent on
        :param questionToCheck: the question to check the dependency
        :return: the object of the question or None object
        """
        if questionToCheck.dependent_on != "none":
            for question in self.questions():
                if question.abbreviation == questionToCheck.dependent_on:
                    return question
        else:
            return None

    def notify(self, data: Question):
        """
        Method to inform connected observer about changes
        :param data: the object changed
        :return:
        """
        self.observer.update(data)

    def questions(self) -> list:
        """
        Method to get all questions from the database
        :return: List of questions from database
        """
        return self.database.getQuestions()

    def removeQuestion(self, data: Question) -> bool:
        """
        Method to remove given question from the database
        :param data: Question to be removed
        :return: True, if removing the question was successful, False otherwise
        """
        try:
            self.database.removeQuestion(question=data)
            return True
        except Exception as exp:
            self.logger.error(f"Error while removing question: {exp}")
            return False

    def removeQuestionCategory(self, questionCategory: QuestionCategory) -> bool:
        """
        Method to remove a question category from the database.
        :param questionCategory: Question category to be deleted from the database
        :return: True if the deletion was successful, False otherwise
        """
        try:
            self.database.removeQuestionCategory(category=questionCategory)
            return True
        except Exception as exp:
            self.logger.error(f"Error while getting Question category: {exp}")
            return False

    def saveQuestion(self, data: Question) -> [bool, Question]:
        """
        Method to save given question to the database. Checks if the question has been saved before taking the id.
        :param data: Question to be saved
        :return: Tuple of boolean and question ID
        """
        if data.id != -1:
            res = self.database.editQuestion(question=data)
            self.notify(data)
            return res, data
        else:
            try:
                target = self.database.addQuestion(question=data)
                return True, target
            except Exception as exp:
                self.logger.error(f"Error while saving question: {exp}")
                return False, data

    def setObserver(self, observer):
        """
        Method to set the observer for the controller
        :param observer: the observer assigned to this controller
        :return:
        """
        self.observer = observer
