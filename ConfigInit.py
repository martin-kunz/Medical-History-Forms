import logging
import sys
from json import JSONDecodeError

from Config import Config
from DatabaseController import DatabaseController
from GUI.MainFrame import MainFrame, qss
from GUI.RestoreSession import RestoreSession
from QuestionController import QuestionController
from QuestionObserver import QuestionObserver
from QuestionnaireController import QuestionnaireController
from Questionnaire import Questionnaire
from QuestionnaireObserver import QuestionnaireObserver
from fileHandler import createSessionFile, removeSessionFile, createLogger, readSessionFile, setTypes, setQuestionCategories, setQuestionnaireCategories, createConfigFile, readConfigFile

from PyQt5 import QtWidgets


class ConfigInit:
    """
    The ConfigInit class handles the program start up and initializes certain objects
    that are accessed throughout most of the program, as well as objects needed by those.

    The class is handled static, so every component has access to the same objects, e.g. logger.
    """

    database: DatabaseController
    logger: logging.Logger
    questionnaireController: QuestionnaireController

    @staticmethod
    def init() -> int:
        """
        This method starts up the initialisation process of the program.
        It reads the configuration and sets up every object with the data needed.
        :return: On a successful execution the method returns 0 else an error code.
        """
        # 1. Load up or create config file
        createConfigFile()
        config: Config = readConfigFile()

        # 2. Create logger and log file
        ConfigInit.logger = createLogger(maxFileCount=config.logFileMaxCount)

        # 3. Connect to database
        ConfigInit.database = DatabaseController(logger=ConfigInit.logger, pathSQLiteDatabase=config.localDatabase)
        if config.useNetworkDatabase:
            ConfigInit.database.connectToExtern(
                host=config.networkDatabaseAddress, port=config.networkDatabasePort, user=config.networkDatabaseUser, password=config.networkDatabasePassword, database=config.networkDatabase
            )

        # 4. Create QuestionnaireController and check for Session file
        ConfigInit.questionController = QuestionController(database=ConfigInit.database, logger=ConfigInit.logger)

        categories = ConfigInit.database.getQuestionnaireCategories()
        defaultCategory = None
        for category in categories:
            if category.id == 1:
                defaultCategory = category

        ConfigInit.questionnaireController = QuestionnaireController(questionnaire=Questionnaire(category=defaultCategory), database=ConfigInit.database, logger=ConfigInit.logger)
        ConfigInit.questionnaireController.setObserver(observer=QuestionnaireObserver(observedController=ConfigInit.questionnaireController))

        setTypes(types=ConfigInit.database.getTypes())
        setQuestionCategories(categories=ConfigInit.database.getQuestionCategories())
        setQuestionnaireCategories(categories=ConfigInit.database.getQuestionnaireCategories())

        if config.useRecoveryPoints:
            try:
                createSessionFile()
            except FileExistsError:
                if ConfigInit.sendSessionPrompt():
                    try:
                        ConfigInit.questionnaireController = QuestionnaireController(questionnaire=readSessionFile(), database=ConfigInit.database, logger=ConfigInit.logger)
                        ConfigInit.questionnaireController.setObserver(observer=QuestionnaireObserver(observedController=ConfigInit.questionnaireController))
                    except JSONDecodeError as err:
                        ConfigInit.logger.warning("Found empty session file. Deleting and creating a new one...")
                        removeSessionFile()
                        createSessionFile()

        ConfigInit.questionController.setObserver(QuestionObserver(ConfigInit.questionController, ConfigInit.questionnaireController))

        # 5. Start GUI
        app = QtWidgets.QApplication(sys.argv)

        app.setStyleSheet(qss)

        widget = MainFrame(questionnaireController=ConfigInit.questionnaireController, questionController=ConfigInit.questionController)
        widget.show()

        return app.exec_()

    @staticmethod
    def sendSessionPrompt():
        """
        Method to create a dialog box for session recovery.
        :return: 0 (false) or 1 (true) dependent on user interaction
        """
        app = QtWidgets.QApplication(sys.argv)
        widget = RestoreSession()
        widget.show()
        app.exec_()
        return widget.result()
