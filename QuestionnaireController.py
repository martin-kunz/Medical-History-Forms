import logging
from pathlib import Path

from DatabaseController import DatabaseController
from Question import Question
from Questionnaire import Questionnaire
from QuestionnaireCategory import QuestionnaireCategory
from QuestionnaireObserver import QuestionnaireObserver
from fileHandler import writeToFile, readFromFile


class QuestionnaireController:
    """
    Class handling all actions regarding Questionnaires like saving, creating and editing.
    """

    def __init__(self, questionnaire: Questionnaire, database: DatabaseController, logger: logging.Logger):
        """
        Constructor
        :param questionnaire: The Questionnaire object that is handled by the controller
        :param database: The DatabaseController that is used to save to the database
        :param logger: The Logger for logging actions and errors
        """
        self.questionnaire = questionnaire
        self.database = database
        self.logger = logger
        self.observer: QuestionnaireObserver
        self.requirements: list = []

    def addQuestion(self, newQuestion: Question) -> bool:
        """
        Method to add a question to the current active questionnaire.
        :param newQuestion: the question to add to the current active questionnaire
        :return: true if successful, false if not
        """
        for question in self.questionnaire.questions:
            if question.id == newQuestion.id:
                return False
        self.questionnaire.questions.append(newQuestion)
        self.notify()
        return True

    def addQuestionnaireCategory(self, category: QuestionnaireCategory) -> QuestionnaireCategory:
        """
        Method to save a new questionnaire category to the database.
        :param category: category to save
        :return: the updated category
        """
        try:
            return self.database.addQuestionnaireCategory(category=category)
        except Exception as exception:
            self.logger.exception(exception)

    def categories(self):
        """
        Method to return all currently present categories for questionnaires from the database
        :return: list of questionnaireCategories
        """
        return self.database.getQuestionnaireCategories()

    def editCategory(self, category: QuestionnaireCategory) -> Questionnaire:
        """
        Method to change category of current questionnaire
        :param category: New category for current questionnaire
        :return: Updated questionnaire
        """
        self.questionnaire.category = category
        return self.questionnaire

    def editQuestion(self, target: int, editedQuestion: Question):
        self.questionnaire.questions[target] = editedQuestion

    def editQuestionnaireCategory(self, category: QuestionnaireCategory):
        """
        Method to edit an existing category in the database
        :param category: the edited category
        :return: a boolean regarding success (true) or failure (false) of the operation
        """
        try:
            return self.database.editQuestionnaireCategory(category=category)
        except Exception as exception:
            self.logger.exception(exception)

    def exportQuestionnaire(self, path: Path):
        """
        Method to send an edited copy of the current active questionnaire to the fileHandler for export.
        The edit consists of requirement adjustions specifically for the questionnaire.
        :return:
        """
        tempQuestionnaire = self.questionnaire
        for entry in self.requirements:
            for question in tempQuestionnaire.questions:
                if entry[0].abbr == question.abbreviation:
                    question.required = entry[1]
        return writeToFile(pathToFile=path, questionnaire=tempQuestionnaire)

    def getAllQuestionnaires(self):
        """
        Method to get all questionnaires as questionnaire objects from the database.
        :return:
        """
        return self.database.getQuestionnaires()

    def getCategoryByID(self, catID: int) -> QuestionnaireCategory:
        """
        Method to search for a questionnaireCategory by ID
        :param catID: the id of the searched questionnaireCategory
        :return: the questionnaireCategory with given ID
        """
        for category in self.categories():
            if category.id == catID:
                return category

    def getDefaultCategory(self) -> QuestionnaireCategory:
        """
        Method to get the default "Allgemein" category for questionnaires.
        :return: the default category object
        """
        for category in self.categories():
            if category.id == 1:
                return category

    def getDependencies(self, questionToRemove: Question) -> list:
        """
        Method to get all questions dependent on the given question from the current active questionnaire.
        :param questionToRemove: question object that is to be checked.
        :return: list of all questions that have a dependency on the given question from the current active questionnaire.
        """
        dependentQuestions: list = []
        for question in self.questionnaire.questions:
            if question.dependent_on == questionToRemove.abbreviation:
                dependentQuestions.append(question)
        return dependentQuestions

    def importQuestionnaire(self, path: Path) -> Questionnaire:
        """
        Sets the current questionnaire to the object returned by the file handler.
        :return:
        """
        try:
            self.questionnaire = readFromFile(pathToFile=path)
            self.notify()
        except Exception as e:
            self.logger.warning(e)
            raise e
        return self.questionnaire

    def notify(self):
        """
        Method to inform the Observer about changes to save the current state of the controller.
        :return:
        """
        self.observer.update()

    def remove(self, questionnaire: Questionnaire):
        """
        Method to remove the given questionnaire from the database.
        :param questionnaire: the questionnaire to remove
        :return:
        """
        if questionnaire.id == self.questionnaire.id:
            self.database.removeQuestionnaire(questionnaire=self.questionnaire)
            self.questionnaire = Questionnaire(category=self.getDefaultCategory())
        else:
            self.database.removeQuestionnaire(questionnaire=questionnaire)

    def removeQuestion(self, questionToDelete: Question):
        """
        Method to remove a question from the current active questionnaire
        :param questionToDelete: question to be deleted
        :return:
        """
        for question in self.questionnaire.questions:
            if question.abbreviation == questionToDelete.abbreviation:
                self.questionnaire.questions.remove(question)
        self.notify()
        return

    def removeQuestionnaireCategory(self, category: QuestionnaireCategory) -> bool:
        """
        Method to remove the given category from the database.
        :param category: the category to be removed
        :return: a boolean regarding success (true) or failure (false) of the operation
        """
        try:
            return self.database.removeQuestionnaireCategory(category=category)
        except Exception as exception:
            self.logger.exception(exception)

    def saveQuestionnaire(self, questionnaire: Questionnaire) -> [Questionnaire, list]:
        """
        Method to save the connected questionnaire to the database.
        If it is a new one it creates it and sets the id, otherwise it saves it with the current id.
        :return: The updated questionnaire and possibly a list of questions that could not been saved due to unique abbrevations
        """
        try:
            if questionnaire.id != -1:
                return self.database.editQuestionnaire(questionnaire=questionnaire)
            else:
                return self.database.addQuestionnaire(questionnaire=questionnaire)
        except Exception as e:
            self.logger.exception(e)
            return False

    def setObserver(self, observer: QuestionnaireObserver):
        """
        Method to set the observer of the current controller object.
        :param observer: The @Observer object that observes this object
        """
        self.observer = observer

    def setQuestionnaire(self, questionnaire: Questionnaire):
        """
        Method to change the current active questionnaire and inform the observer about the change.
        :param questionnaire: the new active questionnaire
        :return:
        """
        self.questionnaire = questionnaire
        self.notify()

    def swapQuestionPosition(self, abbreviation: str, index: int):
        """
        Method to swap places of 2 questions inside the current active questionnaires question list
        :param abbreviation: the abbreviation of the question that gets repositioned
        :param index: the new position of the question to swap
        :return:
        """
        for question in self.questionnaire.questions:
            if question.abbreviation == abbreviation:
                oldPos = self.questionnaire.questions.index(question)
                buf = self.questionnaire.questions[index]
                self.questionnaire.questions[index] = question
                self.questionnaire.questions[oldPos] = buf
        self.notify()

    def toggleRequired(self, question: Question):
        """
        Method to record requirement changes specifically for the current active questionnaire.
        :param question: question with changed requirements
        :return:
        """
        found = False
        for entry in self.requirements:
            if entry[0].abbr == question.abbreviation:
                entry[1] = not entry[1]
                found = True
        if not found:
            self.requirements.append([question, not question.required])

    def updateQuestion(self, questionToUpdate: Question):
        """
        Method called on changes on questions that are part of the current active questionnaire. Calls an update on the given question from the database.
        :param questionToUpdate: the question that has been updated
        :return:
        """
        for question in self.questionnaire.questions:
            if question.id == questionToUpdate.id:
                self.questionnaire.questions[self.questionnaire.questions.index(question)] = self.database.getQuestionById(question.id)
