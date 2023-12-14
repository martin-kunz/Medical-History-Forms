#!/usr/bin/env python3

import threading
import time
import mysql.connector

from database.DatabaseExceptions import DatabaseNotConnectedError


class DatabaseMySQL:
    """
    DatabaseController class will handle connections between MHF and a MySQL database
    """

    def __init__(self, logger, host: str, port: int, user: str, password: str, database: str):
        """
        Constructor
        :keyword logger logger Object
        :keyword host IPAddress MySQL Server
        :keyword port Port MySQL Server
        :keyword user Username MySQL Server
        :keyword password Password MySQL Server
        :keyword database name of database
        """
        self.logger = logger
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password = password
        self.database: str = database

        self.mysqlRun: bool = True
        self.connected: bool = False

        self.__connect(True)

        self.checkThread = threading.Thread(target=self.__checkConnection, daemon=True).start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnet()

    def __connect(self, first: bool = False):
        """
        Method to connect to MySQL database, if not available try to reconnect all 5 seconds
        """
        while True:
            try:
                self.conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
                self.c = self.conn.cursor()

                self.__createTables()

                return

            except Exception as e:
                self.logger.error("Error while connection to MySQL database, try to reconnect in 5 seconds: " + str(e))

                if first:
                    raise

                time.sleep(5)

    def disconnet(self):
        """
        Method to disconnect from MySQL database
        """
        self.mysqlRun = False
        self.connected = True
        time.sleep(2)

        try:
            self.conn.close()
        except Exception as e:
            self.logger.error("Error while disconnect MySQL database: " + str(e))
            raise

    def __checkConnection(self):
        """
        Method to check if the MySQL database connected
        If not connected, the method try to connect
        """
        while self.mysqlRun:
            try:
                self.c.execute("SELECT * FROM tb_questions LIMIT 1")
                self.c.fetchone()
                self.connected = True

            except Exception as e:
                self.logger.error("Error: MySQL database are disconnected: " + str(e))
                self.connected = False
                self.__connect()

            time.sleep(1)

    def __createTables(self):
        """
        Methode to create all needed Tables if they are not exist
        """
        try:
            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_question_types(" "id_type INT PRIMARY KEY," "typeName VARCHAR(255) NOT NULL," "displayName VARCHAR(255) NOT NULL," "options BOOLEAN NOT NULL" ")"
            )

            self.c.execute("CREATE TABLE IF NOT EXISTS tb_question_categories(" "id_categoryQ INT PRIMARY KEY," "name VARCHAR(255) UNIQUE NOT NULL," "description VARCHAR(255)" ")")

            self.c.execute("CREATE TABLE IF NOT EXISTS tb_questionnaire_categories(" "id_categoryQA INT PRIMARY KEY," "name VARCHAR(255) UNIQUE NOT NULL," "description VARCHAR(255)" ")")

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_questions("
                "id_question INT PRIMARY KEY,"
                "text LONGTEXT NOT NULL,"
                "type INT NOT NULL,"
                "options VARCHAR(255) NOT NULL,"
                "required BOOLEAN NOT NULL,"
                "dependentOn INT NOT NULL,"
                "expectedAnswer VARCHAR(255) NOT NULL,"
                "abbrv VARCHAR(255) UNIQUE NOT NULL,"
                "score BOOLEAN NOT NULL,"
                "comment BOOLEAN NOT NULL,"
                "category INT NOT NULL"
                # 'FOREIGN KEY(type) REFERENCES tb_question_types(id_type),'
                # 'FOREIGN KEY(dependentOn) REFERENCES tb_questions(id_question),'
                # 'FOREIGN KEY(category) REFERENCES tb_question_Categories(id_categoryQ)'
                ")"
            )

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_questionnaires("
                "id_questionnaire INT PRIMARY KEY,"
                "name VARCHAR(255) NOT NULL,"
                "description VARCHAR(255),"
                "category INT NOT NULL,"
                "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                "lastChanged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
                # 'FOREIGN KEY(category) REFERENCES tb_questionnaire_Categories(id_categoryQA)'
                ")"
            )

            self.c.execute(
                "CREATE TABLE IF NOT EXISTS tb_collections("
                "id_Q INT NOT NULL,"
                "id_QA INT NOT NULL,"
                "position INT NOT NULL,"
                "required BOOLEAN NOT NULL,"
                "PRIMARY KEY (id_Q, id_QA)"
                # 'FOREIGN KEY(id_Q) REFERENCES tb_questions(id_question),'
                # 'FOREIGN KEY(id_QA) REFERENCES tb_questionnaires(id_questionnaire)'
                ")"
            )

        except Exception as e:
            self.logger.error("Error while create tables in MySQL database: " + str(e))
            raise

    def addQuestion(
        self, idQuestion: int, text: str, questionType: int, options: str, required: int, dependent_on: int, expectedAnswer: str, abbrv: str, score: int, comment: int, category: int
    ) -> int:
        """
        Method to add a new question into the tb_questions table
        :param idQuestion: id of question
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
                    "INSERT INTO tb_questions(id_question, text, type, options, required, dependentON, expectedAnswer, abbrv, score, comment, category) VALUES ( %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s, %s)",
                    (idQuestion, text, questionType, options, required, dependent_on, expectedAnswer, abbrv, score, comment, category),
                )
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_questions: " + str(e))
                raise

        else:
            self.logger.error("SQLite database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearQuestions(self) -> bool:
        """
        Method to clear the tb_questions table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questions")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_questions: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def addQuestionCategory(self, idCategoryQ: int, name: str, description: str) -> int:
        """
        Method to add a new category into the tb_question_Categories table
        :param idCategoryQ: id of QuestionCategory
        :param name: name of QuestionCategory
        :param description: description of QuestionCategory
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_question_Categories(id_categoryQ, name, description) VALUES ( %s,  %s, %s)", (idCategoryQ, name, description))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_question_Categories: " + str(e))
                raise

        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearQuestionCategories(self) -> bool:
        """
        Method to clear the tb_question_Categories table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_question_Categories")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_question_Categories: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def addQuestionnaireCategory(self, idCategoryQA: int, name: str, description: str) -> int:
        """
        Method to add a new category into the tb_questionnaire_Categories table
        :param idCategoryQA: id of QuestionnaireCategory
        :param name: name of QuestionnaireCategory
        :param description: description of QuestionnaireCategory
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_questionnaire_Categories(id_categoryQA, name, description) VALUES ( %s,  %s, %s)", (idCategoryQA, name, description))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_Categories: " + str(e))
                raise

        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearQuestionnaireCategories(self) -> bool:
        """
        Method to clear the tb_questionnaire_Categories table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questionnaire_Categories")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_Categories: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def addCollection(self, idQ: int, id_QA: int, position: int, required: int) -> int:
        """
        Method to add a new collection into the tb_collections table
        :param idQ: id of question
        :param id_QA: id of questionnaire
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_collections(id_Q, id_QA, position, required) VALUES ( %s,  %s,  %s,  %s)", (idQ, id_QA, position, required))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_collections: " + str(e))
                raise

        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearCollections(self) -> bool:
        """
        Method to clear the tb_collections table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_collections")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_collections: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def addType(self, idType: int, name: str, displayName: str, options: int) -> int:
        """
        Method to add a new type into the tb_question_types table
        :param idType: id of type
        :param name: name of type
        :param displayName: displayName of type
        :param options: 1=true, 0=false
        :return: new row id
        """

        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_question_types(id_type, typeName, displayName, options) VALUES ( %s,  %s,  %s, %s)", (idType, name, displayName, options))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_question_types: " + str(e))
                raise

        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearTypes(self) -> bool:
        """
        Method to clear the tb_question_types table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_question_types")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_question_types: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def addQuestionnaire(self, idQuestionnaire: int, name: str, description: str, category: int) -> int:
        """
        Method to add a new questionnaire into the tb_questionnaires table
        :param idQuestionnaire: id of questionnaire
        :param name: name of questionnaire
        :param description: description of questionnaire
        :param category: category id of questionnaire
        :return: new row id
        """
        if self.connected:
            try:
                self.c.execute("INSERT INTO tb_questionnaires(id_questionnaire, name, description, category) VALUES ( %s,  %s,  %s, %s)", (idQuestionnaire, name, description, category))
                self.conn.commit()

                return self.c.lastrowid

            except Exception as e:
                self.logger.error("Error while insert database row into tb_questionnaires: " + str(e))
                raise

        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")

    def clearQuestionnaires(self) -> bool:
        """
        Method to clear the tb_questionnaires table
        :return: True / exception
        """
        if self.connected:
            try:
                self.c.execute("DELETE FROM tb_questionnaires")
                self.conn.commit()

                return True

            except Exception as e:
                self.logger.error("Error while clear database rows from tb_questionnaires: " + str(e))
                raise
        else:
            self.logger.error("MySQL database not connect")
            raise DatabaseNotConnectedError("MySQL database not connect")
