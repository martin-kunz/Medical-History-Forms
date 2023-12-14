import json
import threading
import time
from pathlib import Path

from Question import Question
from QuestionCategory import QuestionCategory
from QuestionType import QuestionType
from Questionnaire import Questionnaire
from QuestionnaireCategory import QuestionnaireCategory
from database.DatabaseMySQL import DatabaseMySQL
from database.DatabaseSQLite import DatabaseSQLite


class DatabaseController:
    """
    DatabaseController class will handle connections between MHF and any SQL databases
    """

    def __init__(self, logger, pathSQLiteDatabase: Path):
        """
        Constructor
        :keyword logger: logger Object
        :keyword pathSQLiteDatabase: path of databasefile e.g. data/mhf.db
        """
        self.logger = logger
        self.pathSQLiteDatabase = pathSQLiteDatabase
        self.mysqlDisconnect = False

        lstQuestionTypes = [
            ("radio", "Auswahl", 1),
            ("select", "Dropdown", 1),
            ("text", "Freitext", 0),
            ("textarea", "Mehrzeiliger Freitext", 0),
            ("number", "Zahl", 0),
            ("date", "Datum", 0),
            ("heading", "Überschrift", 0),
        ]

        try:
            self.databaseSQLite = DatabaseSQLite(self.logger, self.pathSQLiteDatabase, lstQuestionTypes)
            self.databaseMySQL = None

            self.syncDatabasesThreadEvent = threading.Event()
            self.syncDatabasesRequired = []

        except Exception as e:
            self.logger.error("Error while init DatabaseController:" + str(e))
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def connectToExtern(self, host: str, port: int, user: str, password: str, database: str) -> bool:
        """
        Constructor
        :keyword host: IPAddress MySQL Server
        :keyword port: Port MySQL Server
        :keyword user: Username MySQL Server
        :keyword password: Password MySQL Server
        :keyword database: name of database
        """
        try:
            self.databaseMySQL = DatabaseMySQL(self.logger, host, port, user, password, database)

            self.syncDatabasesThread = threading.Thread(target=self.syncDatabases, daemon=True, args=(self.syncDatabasesThreadEvent, self.databaseMySQL)).start()

            self.syncDatabasesRequired.append("tb_question_types")
            self.syncDatabasesRequired.append("tb_question_categories")
            self.syncDatabasesRequired.append("tb_questionnaire_categories")
            self.syncDatabasesRequired.append("tb_questions")
            self.syncDatabasesRequired.append("tb_questionnaires")
            self.syncDatabasesRequired.append("tb_collections")
            self.syncDatabasesThreadEvent.set()

        except Exception as e:
            self.logger.error("Error while connectToExtern:" + str(e))
            raise

        return True

    def disconnectFromExtern(self):
        """
        Method to disconnect from extern database
        """
        self.mysqlDisconnect = True
        self.syncDatabasesRequired.clear()
        self.syncDatabasesThreadEvent.set()
        self.databaseMySQL = None

    def addQuestion(self, question: Question) -> Question:
        """
        Methode to add a new question to the database
        :param question: object of question
        :return: question object include id
        """
        try:
            dependentOnID = -1
            for currentQuestion in self.getQuestions():
                if currentQuestion.abbreviation == question.dependent_on:
                    dependentOnID = currentQuestion.id

            question.id = self.databaseSQLite.addQuestion(
                text=question.text,
                questionType=question.type.id,
                options=json.dumps(question.options),
                required=question.required,
                dependent_on=dependentOnID,
                expectedAnswer=question.expected_answer,
                abbrv=question.abbreviation,
                score=question.score,
                comment=question.comment,
                category=question.category.id,
            )

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questions")
                self.syncDatabasesThreadEvent.set()

            return question

        except Exception as e:
            self.logger.error("Error while addQuestion:" + str(e))
            raise

    def editQuestion(self, question: Question) -> Question:
        """
        Methode to alter a exist question in database
        :param question:  altered object of question
        :return: True if done / raise exception
        """
        try:
            dependentOnID = -1
            for row in self.getQuestions():
                if row.abbreviation == question.dependent_on:
                    dependentOnID = row.id

            self.databaseSQLite.changeQuestion(
                id_question=question.id,
                text=question.text,
                questionType=question.type.id,
                options=json.dumps(question.options),
                required=question.required,
                dependent_on=dependentOnID,
                expectedAnswer=question.expected_answer,
                abbrv=question.abbreviation,
                score=question.score,
                comment=question.comment,
                category=question.category.id,
            )

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questions")
                self.syncDatabasesThreadEvent.set()

            return question

        except Exception as e:
            self.logger.error("Error while editQuestion:" + str(e))
            raise

    def removeQuestion(self, question: Question) -> bool:
        """
        Methode to remove a exist question in database
        :param question:  current object of question
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.removeQuestion(questionId=question.id)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questions")
                self.syncDatabasesThreadEvent.set()

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestion:" + str(e))
            raise

    def getQuestions(self) -> list:
        """
        Methode to get all questions from database
        :return: list of question objects
        """
        lstQuestions = []
        lstTypes = self.getTypes()
        lstQuestionCategorys = self.getQuestionCategories()
        lstQuestionRows = self.databaseSQLite.getQuestions()

        for row in lstQuestionRows:
            currentType = None
            for questionType in lstTypes:
                if questionType.id == row[2]:
                    currentType = questionType
                    break

            currentCategory = None
            for category in lstQuestionCategorys:
                if category.id == row[10]:
                    currentCategory = category
                    break

            currentDependentOn = "none"
            if row[5] != -1:
                for questionRow in lstQuestionRows:
                    if questionRow[0] == row[5]:
                        currentDependentOn = questionRow[7]
                        break

            question = Question(
                id=row[0],
                text=row[1],
                type=currentType,
                options=json.loads(row[3]),
                required=bool(row[4]),
                dependent_on=currentDependentOn,
                expected_answer=row[6],
                abbreviation=row[7],
                score=bool(row[8]),
                comment=bool(row[9]),
                category=currentCategory,
            )
            lstQuestions.append(question)

        return lstQuestions

    def getQuestionById(self, questionId: int):
        """
        Method to get one question by id
        :param questionId: id of question
        :return: question object
        """
        for question in self.getQuestions():
            if question.id == questionId:
                return question
        return None

    def addQuestionnaire(self, questionnaire: Questionnaire) -> [Questionnaire, list]:
        """
        Methode to add a new questionnaire to the database
        :param questionnaire: object of questionnaire
        :return: questionnaire object include id´s, errorlist = list of questions which already in table
        """
        position = 0
        errorList = []

        try:
            questionnaire.id = self.databaseSQLite.addQuestionnaire(name=questionnaire.name, description=questionnaire.description, category=questionnaire.category.id)

            for question in questionnaire.questions:
                position += 1

                try:
                    if question.id == -1:
                        question = self.addQuestion(question)

                    self.__addCollection(id_Q=question.id, id_QA=questionnaire.id, position=position, required=question.required)

                except Exception as e:
                    self.logger.info("Question already exist in tb_questions:" + str(e))
                    errorList.append(question)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaires")
                self.syncDatabasesRequired.append("tb_collections")
                self.syncDatabasesThreadEvent.set()

            return questionnaire, errorList

        except Exception as e:
            self.logger.error("Error while addQuestionnaire:" + str(e))
            raise

    def editQuestionnaire(self, questionnaire: Questionnaire, purge: bool = False) -> [Questionnaire, list]:
        """
        Methode to alter a exist questionnaire in database
        :param questionnaire:  altered object of questionnaire
        :param purge: true= remove question; false= remove only collection
        :return: questionnaire object include id´s, errorlist = list of questions which already in table
        """
        position = 0
        errorList = []

        try:
            for question in questionnaire.questions:
                self.databaseSQLite.c.execute("SELECT COUNT(*) FROM tb_collections WHERE id_Q=?", (question.id,))
                count = self.databaseSQLite.c.fetchone()[0]

                self.__removeCollection(id_Q=question.id, id_QA=questionnaire.id)

                if count == 1 and purge:
                    self.removeQuestion(question=question)

            self.__clearCollections(id_QA=questionnaire.id)

            self.databaseSQLite.changeQuestionnaire(id_questionnaire=questionnaire.id, name=questionnaire.name, description=questionnaire.description, category=questionnaire.category.id)

            for question in questionnaire.questions:
                position += 1

                try:
                    if question.id == -1:
                        question = self.addQuestion(question)

                    self.__addCollection(id_Q=question.id, id_QA=questionnaire.id, position=position, required=question.required)

                except Exception as e:
                    self.logger.info("Question already exist in tb_questions:" + str(e))
                    errorList.append(question)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaires")
                self.syncDatabasesRequired.append("tb_collections")
                self.syncDatabasesThreadEvent.set()

            return questionnaire, errorList

        except Exception as e:
            self.logger.error("Error while editQuestionnaire:" + str(e))
            raise

    def removeQuestionnaire(self, questionnaire: Questionnaire, purge: bool = False) -> bool:
        """
        Methode to remove a exist questionnaire in database
        :param questionnaire:  current object of questionnaire
        :param purge: true= remove all; false= remove only collections and questionnaire
        :return: True if done / raise exception
        """
        try:
            for question in questionnaire.questions:
                self.databaseSQLite.c.execute("SELECT COUNT(*) FROM tb_collections WHERE id_Q=?", (question.id,))
                count = self.databaseSQLite.c.fetchone()[0]

                self.__removeCollection(id_Q=question.id, id_QA=questionnaire.id)

                if count == 1 and purge:
                    self.removeQuestion(question=question)

            self.databaseSQLite.removeQuestionnaire(questionnaireId=questionnaire.id)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaires")
                self.syncDatabasesRequired.append("tb_collections")
                self.syncDatabasesThreadEvent.set()

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestionnaire:" + str(e))
            raise

    def getQuestionnaires(self) -> list:
        """
        Methode to get all questionnaires from database
        :return: list of questionnaire objects
        """
        lstQuestionnaireCategory = self.getQuestionnaireCategories()
        lstQuestions = self.getQuestions()
        lstColletionRows = self.databaseSQLite.getCollections()

        lstQuestionnaires = []

        for questionnaireRow in self.databaseSQLite.getQuestionnaire():
            currentCategory = None
            for category in lstQuestionnaireCategory:
                if category.id == questionnaireRow[3]:
                    currentCategory = category
                    break

            currentQuestions = []
            for collectionRow in lstColletionRows:
                if collectionRow[1] == questionnaireRow[0]:
                    for question in lstQuestions:
                        if question.id == collectionRow[0]:
                            currentQuestions.insert(collectionRow[2], question)

            lstQuestionnaires.append(
                Questionnaire(
                    id=questionnaireRow[0],
                    name=questionnaireRow[1],
                    description=questionnaireRow[2],
                    questions=currentQuestions,
                    category=currentCategory,
                    creationDate=questionnaireRow[4],
                    lastEdited=questionnaireRow[5],
                )
            )

        return lstQuestionnaires

    def getQuestionnaire(self, questionnaire: Questionnaire) -> Questionnaire:
        """
        Methode to get one special questionnaires from database
        :return: questionnaire object; if not exist = new Questionnare
        """
        for questionnaireObject in self.getQuestionnaires():
            if questionnaire.id == questionnaireObject.id:
                return questionnaireObject

        return questionnaire

    def __addCollection(self, id_Q: int, id_QA: int, position: int, required: int) -> bool:
        """
        Methode to add a new collection to the database
        TODO: Parameter anpassen
        :return: new category id
        """
        try:
            self.databaseSQLite.addCollection(id_Q=id_Q, id_QA=id_QA, position=position, required=required)

            return True

        except Exception as e:
            self.logger.error("Error while __addCollection:" + str(e))
            raise

    def __removeCollection(self, id_Q: int, id_QA: int) -> bool:
        """
        Methode to remove a exist collection in database
        TODO: Parameter anpassen
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.removeCollection(id_Q=id_Q, id_QA=id_QA)

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestionCategory:" + str(e))
            raise

    def __clearCollections(self, id_QA: int) -> bool:
        """
        Methode to remove a exist collection in database
        :param id_QA: id of questionnaire
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.clearCollections(id_QA=id_QA)

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestionCategory:" + str(e))
            raise

    def addQuestionCategory(self, category: QuestionCategory) -> QuestionCategory:
        """
        Methode to add a new category to the database
        :param category: object of category
        :return: QuestionCategory object include id
        """
        try:
            category.id = self.databaseSQLite.addQuestionCategory(name=category.category, description=category.description)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_question_categories")
                self.syncDatabasesThreadEvent.set()

            return category

        except Exception as e:
            self.logger.error("Error while addQuestionCategory:" + str(e))
            raise

    def editQuestionCategory(self, category: QuestionCategory) -> QuestionCategory:
        """
        Methode to alter a exist category in database
        :param category:  altered object of category
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.changeQuestionCategory(id_categoryQ=category.id, name=category.category, description=category.description)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_question_categories")
                self.syncDatabasesThreadEvent.set()

            return category

        except Exception as e:
            self.logger.error("Error while editQuestionCategory:" + str(e))
            raise

    def removeQuestionCategory(self, category: QuestionCategory) -> bool:
        """
        Methode to remove a exist category in database
        :param category:  current object of category
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.removeQuestionCategory(categoryId=category.id)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_question_categories")
                self.syncDatabasesThreadEvent.set()

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestionCategory:" + str(e))
            raise

    def getQuestionCategories(self) -> list:
        """
        Methode to get all Categories from database
        :return: list of category objects
        """

        lstQuestionCategories = []

        for row in self.databaseSQLite.getQuestionCategories():
            category = QuestionCategory(id=row[0], category=row[1], description=row[2])
            lstQuestionCategories.append(category)

        return lstQuestionCategories

    def addQuestionnaireCategory(self, category: QuestionnaireCategory) -> QuestionnaireCategory:
        """
        Methode to add a new category to the database
        :param category: object of category
        :return: QuestionnaireCategory object include id
        """
        try:
            category.id = self.databaseSQLite.addQuestionnaireCategory(name=category.category, description=category.description)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaire_categories")
                self.syncDatabasesThreadEvent.set()

            return category

        except Exception as e:
            self.logger.error("Error while addQuestionnaireCategory:" + str(e))
            raise

    def editQuestionnaireCategory(self, category: QuestionnaireCategory) -> QuestionnaireCategory:
        """
        Methode to alter a exist category in database
        :param category:  altered object of category
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.changeQuestionnaireCategory(id_categoryQA=category.id, name=category.category, description=category.description)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaire_categories")
                self.syncDatabasesThreadEvent.set()

            return category

        except Exception as e:
            self.logger.error("Error while editQuestionnaireCategory:" + str(e))
            raise

    def removeQuestionnaireCategory(self, category: QuestionnaireCategory) -> bool:
        """
        Methode to remove a exist category in database
        :param category:  current object of category
        :return: True if done / raise exception
        """
        try:
            self.databaseSQLite.removeQuestionnaireCategory(categoryId=category.id)

            # invoke to sync database
            if self.databaseMySQL:
                self.syncDatabasesRequired.append("tb_questionnaire_categories")
                self.syncDatabasesThreadEvent.set()

            return True

        except Exception as e:
            self.logger.error("Error while removeQuestionnaireCategory:" + str(e))
            raise

    def getQuestionnaireCategories(self) -> list:
        """
        Methode to get all Categories from database
        :return: list of category objects
        """
        lstQuestionnaireCategories = []

        for row in self.databaseSQLite.getQuestionnaireCategories():
            category = QuestionCategory(id=row[0], category=row[1], description=row[2])
            lstQuestionnaireCategories.append(category)

        return lstQuestionnaireCategories

    def getTypes(self) -> list:
        """
        Methode to get all types from database
        :return: list of types objects
        """
        lstTypes = []

        for row in self.databaseSQLite.getTypes():
            questionType = QuestionType(id=row[0], typeName=row[1], displayName=row[2], options=bool(row[3]))
            lstTypes.append(questionType)

        return lstTypes

    def syncDatabases(self, event, destinationDatabase):
        """
        Method to sync two databases
        :param event: Threadevent
        :param destinationDatabase: destination database
        """
        time.sleep(5)

        databaseSQLite = DatabaseSQLite(self.logger, self.pathSQLiteDatabase)

        t = threading.currentThread()

        while not self.mysqlDisconnect:
            if event.wait():
                while len(self.syncDatabasesRequired) > 0:
                    try:
                        nextRequired = self.syncDatabasesRequired.pop()

                        if nextRequired == "tb_question_types":
                            destinationDatabase.clearTypes()

                            for row in databaseSQLite.getTypes():
                                destinationDatabase.addType(row[0], row[1], row[2], row[3])

                        elif nextRequired == "tb_question_categories":
                            destinationDatabase.clearQuestionCategories()

                            for row in databaseSQLite.getQuestionCategories():
                                destinationDatabase.addQuestionCategory(row[0], row[1], row[2])

                        elif nextRequired == "tb_questionnaire_categories":
                            destinationDatabase.clearQuestionnaireCategories()

                            for row in databaseSQLite.getQuestionnaireCategories():
                                destinationDatabase.addQuestionnaireCategory(row[0], row[1], row[2])

                        elif nextRequired == "tb_questions":
                            destinationDatabase.clearQuestions()

                            for row in databaseSQLite.getQuestions():
                                destinationDatabase.addQuestion(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])

                        elif nextRequired == "tb_questionnaires":
                            destinationDatabase.clearQuestionnaires()

                            for row in databaseSQLite.getQuestionnaire():
                                destinationDatabase.addQuestionnaire(row[0], row[1], row[2], row[3])

                        elif nextRequired == "tb_collections":
                            destinationDatabase.clearCollections()

                            for row in databaseSQLite.getCollections():
                                destinationDatabase.addCollection(row[0], row[1], row[2], row[3])

                    except Exception as e:
                        self.logger.warning("Warning while sync databases: " + str(e))

                event.clear()

        self.mysqlDisconnect = False
