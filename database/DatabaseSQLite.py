#!/usr/bin/env python3

import sqlite3
from pathlib import Path

from database.DatabaseExceptions import DatabaseNotConnectedError


class DatabaseSQLite:
    """
    DatabaseController class will handle connections between MHF and a SQLite database
    """

    def __init__(self, logger, pathSQLiteDatabase: Path, questionTypes: list = []):
        """
        Constructor
        :keyword logger logger Object
        :param pathSQLiteDatabase: path of databasefile e.g. data/mhf.db
        :param questionTypes: List of Questiontypes ("typeName", "displayName", options)
        """
        self.logger: logger = logger
        self.connected: bool = False
        self.lstQuestionTypes: list = questionTypes

        if not pathSQLiteDatabase.parent.is_dir():
            self.logger.warning("Data directory not exist, will be created.")
            try:
                pathSQLiteDatabase.parent.mkdir()
            except Exception as e:
                self.logger.error("Error while create data directory: " + str(e))
                raise

        try:
            self.conn = sqlite3.connect(str(pathSQLiteDatabase))
            self.c = self.conn.cursor()

        except Exception as e:
            self.logger.error("Error while connection to SQLITE database: " + str(e))
            raise

        self.__createTables()

        self.connected = True

        self.__createTypes()
        self.__createCategories()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except Exception as e:
            self.logger.error("Error while disconnect SQLITE database: " + str(e))
            raise

    def __createTables(self):
        """
        Method which create all needed Tables if they not exist
        :return: True or raise Exception
        """
        try:
            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_question_types(" "id_type INTEGER PRIMARY KEY AUTOINCREMENT," "typeName TEXT NOT NULL," "displayName TEXT NOT NULL," "options INTEGER NOT NULL" ")"
            )

            self.c.execute("CREATE TABLE IF NOT EXISTS tb_question_categories(" "id_categoryQ INTEGER PRIMARY KEY AUTOINCREMENT," "name TEXT UNIQUE NOT NULL," "description TEXT" ")")

            self.c.execute("CREATE TABLE IF NOT EXISTS tb_questionnaire_categories(" "id_categoryQA INTEGER PRIMARY KEY AUTOINCREMENT," "name TEXT UNIQUE NOT NULL," "description TEXT" ")")

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_questions("
                "id_question INTEGER PRIMARY KEY AUTOINCREMENT,"
                "text TEXT NOT NULL,"
                "type INTEGER NOT NULL,"
                "options TEXT NOT NULL,"
                "required INTEGER NOT NULL,"
                "dependentOn INTEGER NOT NULL,"
                "expectedAnswer TEXT NOT NULL,"
                "abbrv TEXT UNIQUE NOT NULL,"
                "score INTEGER NOT NULL,"
                "comment INTEGER NOT NULL,"
                "category INTEGER NOT NULL,"
                "FOREIGN KEY(type) REFERENCES tb_question_types(id_type),"
                "FOREIGN KEY(dependentOn) REFERENCES tb_questions(id_question),"
                "FOREIGN KEY(category) REFERENCES tb_question_Categories(id_categoryQ)"
                ")"
            )

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_questionnaires("
                "id_questionnaire INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT NOT NULL,"
                "description TEXT,"
                "category INTEGER NOT NULL,"
                "created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                "lastChanged TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                "FOREIGN KEY(category) REFERENCES tb_questionnaire_Categories(id_categoryQA)"
                ")"
            )

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_collections("
                "id_Q INTEGER NOT NULL,"
                "id_QA INTEGER NOT NULL,"
                "position INTEGER NOT NULL,"
                "required INTEGER NOT NULL,"
                "PRIMARY KEY (id_Q, id_QA),"
                "FOREIGN KEY(id_Q) REFERENCES tb_questions(id_question),"
                "FOREIGN KEY(id_QA) REFERENCES tb_questionnaires(id_questionnaire)"
                ")"
            )

        except Exception as e:
            self.logger.error("Error while create tables in SQLITE database: " + str(e))
            raise

        return True

    def __createTypes(self):
        """
        Method which create all possible question types
        """

        for value in self.lstQuestionTypes:
            if self.connected:
                try:
                    # Check if the type already exist
                    self.c.execute("SELECT COUNT(typeName) FROM tb_question_types WHERE typeName=?", (value[0],))
                    if self.c.fetchone()[0] == 0:
                        self.addType(value[0], value[1], value[2])

                except Exception as e:
                    self.logger.error("Error while SELECT database rows from tb_question_types: " + str(e))
                    raise

            else:
                self.logger.error("SQLite database not connect")
                raise DatabaseNotConnectedError("SQLite database not connect")

        return True

    def __createCategories(self):
        """
        Method which create the standard categories
        """

        try:
            self.c.execute("SELECT COUNT(id_categoryQ) FROM tb_question_Categories WHERE id_categoryQ=1 AND name=?", ("Allgemein",))
            if self.c.fetchone()[0] == 0:
                self.addQuestionCategory("Allgemein", "")

        except Exception as e:
            self.logger.error("Error while SELECT database rows from tb_question_Categories: " + str(e))
            raise

        try:
            self.c.execute("SELECT COUNT(id_categoryQA) FROM tb_questionnaire_Categories WHERE id_categoryQA=1 AND name=?", ("Allgemein",))
            if self.c.fetchone()[0] == 0:
                self.addQuestionnaireCategory("Allgemein", "")

        except Exception as e:
            self.logger.error("Error while SELECT database rows from tb_questionnaire_Categories: " + str(e))
            raise

    def addQuestion(self, text: str, questionType: int, options: str, required: int, dependent_on: int, expectedAnswer: str, abbrv: str, score: int, comment: int, category: int) -> int:
        """
        Method to add a new question into the tb_questions table
        :param text: text of question
        :param questionType: type id ov question
        :param options: options of question (JSON)
        :param required: if question required or not
        :param dependent_on: dependent on question id
        :param expectedAnswer: option of dependent on question
        :param abbrv: unique abbreviation of question
        :param score: if question score or not
        :param comment: if question comment or not
        :param category: category id of question
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute(
                    "INSERT INTO tb_questions(text, type, options, required, dependentON, expectedAnswer, abbrv, score, comment, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        text,
                        questionType,
                        options,
                        required,
                        dependent_on,
                        expectedAnswer,
                        abbrv,
                        score,
                        comment,
                        category,
                    ),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_questions: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def changeQuestion(
        self, id_question: int, text: str, questionType: int, options: str, required: int, dependent_on: int, expectedAnswer: str, abbrv: str, score: int, comment: int, category: int
    ) -> bool:
        """
        Method to change a question from the tb_questions table
        :param id_question: id of question
        :param text: text of question
        :param questionType: type id ov question
        :param options: options of question (JSON)
        :param required: if question required or not
        :param dependent_on: dependent on question id
        :param expectedAnswer: option of dependent on question
        :param abbrv: unique abbreviation of question
        :param score: if question score or not
        :param comment: if question comment or not
        :param category: category id of question
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute(
                    "UPDATE tb_questions SET text=?, type=?, options=?, required=?, dependentOn=?, expectedAnswer=?, abbrv=?, score=?, comment=?, category=? WHERE id_question=?",
                    (
                        text,
                        questionType,
                        options,
                        required,
                        dependent_on,
                        expectedAnswer,
                        abbrv,
                        score,
                        comment,
                        category,
                        id_question,
                    ),
                )
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while update database row from tb_questions: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def removeQuestion(self, questionId) -> bool:
        """
        Method to remove a question from the tb_questions table
        :param questionId: question row id
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questions WHERE id_question=?", (questionId,))
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_questions: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getQuestions(self) -> list:
        """
        Method to return all rows from the tb_questions table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_questions"):
            lstRows.append(row)

        return lstRows

    def addQuestionCategory(self, name: str, description: str) -> int:
        """
        Method to add a new category into the tb_question_Categories table
        :param name: name of QuestionCategory
        :param description: description of QuestionCategory
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_question_Categories(name, description) VALUES (?, ?)", (name, description))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_question_Categories: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def changeQuestionCategory(self, id_categoryQ: int, name: str, description: str) -> bool:
        """
        Method to change a category from the tb_question_Categories table
        :param id_categoryQ: id of row to alter
        :param name: name of QuestionCategory
        :param description: description of QuestionCategory
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute(
                    "UPDATE tb_question_Categories SET name=?, description=? WHERE id_categoryQ=?",
                    (
                        name,
                        description,
                        id_categoryQ,
                    ),
                )
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while update database row from tb_question_Categories: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def removeQuestionCategory(self, categoryId) -> bool:
        """
        Method to remove a category from the tb_question_Categories table
        :param categoryId: category row id
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_question_Categories WHERE id_categoryQ=?", (categoryId,))
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_question_Categories: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getQuestionCategories(self) -> list:
        """
        Method to return all rows from the tb_question_Categories table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_question_Categories"):
            lstRows.append(row)

        return lstRows

    def addQuestionnaireCategory(self, name: str, description: str) -> int:
        """
        Method to add a new category into the tb_questionnaire_Categories table
        :param name: name of QuestionnaireCategory
        :param description: description of QuestionnaireCategory
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute(
                    "INSERT INTO tb_questionnaire_Categories(name, description) VALUES (?, ?)",
                    (
                        name,
                        description,
                    ),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_Categories: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def changeQuestionnaireCategory(self, id_categoryQA: int, name: str, description: str) -> bool:
        """
        Method to change a category from the tb_questionnaire_Categories table
        :param id_categoryQA: id of row to alter
        :param name: name of QuestionnaireCategory
        :param description: description of QuestionnaireCategory
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute(
                    "UPDATE tb_questionnaire_Categories SET name=?, description=? WHERE id_categoryQA=?",
                    (
                        name,
                        description,
                        id_categoryQA,
                    ),
                )
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while update database row from tb_Categories: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def removeQuestionnaireCategory(self, categoryId) -> bool:
        """
        Method to remove a category from the tb_questionnaire_Categories table
        :param categoryId: category row id
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questionnaire_Categories WHERE id_categoryQA=?", (categoryId,))
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_Categories: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getQuestionnaireCategories(self) -> list:
        """
        Method to return all rows from the tb_questionnaire_Categories table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_questionnaire_Categories"):
            lstRows.append(row)

        return lstRows

    def addCollection(self, id_Q: int, id_QA: int, position: int, required: int) -> int:
        """
        Method to add a new collection into the tb_collections table
        :param id_Q: id of question
        :param id_QA: id of questionnaire
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute(
                    "INSERT INTO tb_collections(id_Q, id_QA, position, required) VALUES (?, ?, ?, ?)",
                    (
                        id_Q,
                        id_QA,
                        position,
                        required,
                    ),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_collections: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def removeCollection(self, id_Q: int, id_QA: int) -> bool:
        """
        Method to remove a collection from the tb_collections table
        :param id_Q: id of question
        :param id_QA: id of questionnaire
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute(
                    "DELETE FROM tb_collections WHERE id_Q=? AND id_QA=?",
                    (
                        id_Q,
                        id_QA,
                    ),
                )
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_collections: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def clearCollections(self, id_QA: int) -> bool:
        """
        Method to remove all collection by questionaireId from the tb_collections table
        :param id_QA: id of questionnaire
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_collections WHERE id_QA=?", (id_QA,))
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_collections: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getCollections(self) -> list:
        """
        Method to return all rows from the tb_collections table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_collections"):
            lstRows.append(row)

        return lstRows

    def addType(self, name: str, displayName: str, options: int) -> int:
        """
        Method to add a new type into the tb_question_types table
        :param name: name of type
        :param displayName: displayName of type
        :param options: 1=true, 0=false
        :return: new row id
        """

        if self.connected:
            try:
                self.c.execute(
                    "INSERT INTO tb_question_types(typeName, displayName, options) VALUES (?, ?, ?)",
                    (
                        name,
                        displayName,
                        options,
                    ),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_question_types: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getTypes(self) -> list:
        """
        Method to return all rows from the tb_question_types table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_question_types"):
            lstRows.append(row)

        return lstRows

    def addQuestionnaire(self, name: str, description: str, category: int) -> int:
        """
        Method to add a new questionnaire into the tb_questionnaires table
        :param name: name of questionnaire
        :param description: description of questionnaire
        :param category: category id of questionnaire
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute(
                    "INSERT INTO tb_questionnaires(name, description, category) VALUES (?, ?, ?)",
                    (
                        name,
                        description,
                        category,
                    ),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_questionnaires: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def changeQuestionnaire(self, id_questionnaire: int, name: str, description: str, category: int) -> bool:
        """
        Method to change a questionnaire from the tb_questionnaires table
        :param id_questionnaire: id of questionnaire
        :param name: name of questionnaire
        :param description: description of questionnaire
        :param category: category id of questionnaire
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute(
                    "UPDATE tb_questionnaires SET name=?, description=?, category=?, lastChanged=CURRENT_TIMESTAMP WHERE id_questionnaire=?", (name, description, category, id_questionnaire)
                )
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while update database row from tb_questionnaires: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def removeQuestionnaire(self, questionnaireId) -> bool:
        """
        Method to remove a questionnaire from the tb_questionnaires table
        :param questionnaireId: questionnaire row id
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questionnaires WHERE id_questionnaire=?", (questionnaireId,))
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while delete database row from tb_questionnaires: " + str(e))
                raise
        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("SQLite database not connect")

    def getQuestionnaire(self) -> list:
        """
        Method to return all rows from the tb_questionnaires table
        return: List of rows
        """

        lstRows = []

        for row in self.c.execute("SELECT * FROM tb_questionnaires"):
            lstRows.append(row)

        return lstRows
