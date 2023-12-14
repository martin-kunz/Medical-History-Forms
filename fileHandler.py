import json
import os
import configparser
from pathlib import Path
import logging
import time

from Config import Config
from Question import Question
from QuestionCategory import QuestionCategory
from QuestionType import QuestionType
from Questionnaire import Questionnaire
from QuestionnaireCategory import QuestionnaireCategory


class FileHandlerStash:
    SESSION_FILE_PATH: Path = Path(os.getcwd()) / Path("session.lock")
    CONFIG_FILE_PATH: Path = Path(os.getcwd()) / Path("config/config.ini")
    TYPES: list = []
    QUESTION_CATEGORIES: list = []
    QUESTIONNAIRE_CATEGORIES: list = []
    LOGGER: logging.Logger = None


def readFromFile(pathToFile: Path) -> Questionnaire:
    """Function to read the questionnaire from the given JSON file

    Args:
        pathToFile (Path): Path to the file, which should be read from

    Returns:
        Questionnaire: The read questionnaire
    """
    FileHandlerStash.LOGGER.debug("Reading from file: " + str(pathToFile))
    jsonObj = readJSONObjFromFile(pathToFile)
    jsonQuestions = jsonObj["question"]
    questions: list = []
    FileHandlerStash.LOGGER.debug("Creating question list")
    for q in jsonQuestions:
        question: Question
        if q["required"] == "true":
            required = True
        else:
            required = False
        if q["score"] == "true":
            score = True
        else:
            score = False
        if q["comment"] == "true":
            comment = True
        else:
            comment = False
        if q["options"] == "none":
            question: Question = Question(
                text=q["text"],
                type=getTypeByTypeName(q["type"]),
                options=[],
                required=required,
                dependent_on=q["dependent_on"],
                expected_answer=q["expected_answer"],
                abbreviation=q["abbrv"],
                score=score,
                comment=comment,
                category=getQuestionCategoryByID(),
            )
            questions.insert(int(q["number"]), question)
        else:
            optionKeys: list = []
            options: list = []
            for o in q["options"]:
                optionKeys.append(o)
            for o in optionKeys:
                options.append(q["options"][o])
            question: Question = Question(
                text=q["text"],
                type=getTypeByTypeName(q["type"]),
                options=options,
                required=required,
                dependent_on=q["dependent_on"],
                expected_answer=q["expected_answer"],
                abbreviation=q["abbrv"],
                score=score,
                comment=comment,
                category=getQuestionCategoryByID(),
            )
            questions.insert(int(q["number"]), question)
    FileHandlerStash.LOGGER.debug("Creating questionnaire")
    questionnaire: Questionnaire = Questionnaire(name=pathToFile.stem, questions=questions, category=getQuestionnaireCategoryByID())
    return questionnaire


def writeToFile(pathToFile: Path, questionnaire: Questionnaire):
    """Function to write the questionnaire in the given JSON format to the given file

    Args:
        pathToFile (Path): Path to the file, which should be written to
        questionnaire (Questionnaire): The questionnaire, that should be written to the file
    """
    FileHandlerStash.LOGGER.debug("Writing to file: " + str(pathToFile))
    if len(questionnaire.questions) == 0:
        raise Exception("No questions in questionnaire.")
    questions: list = questionnaire.questions
    FileHandlerStash.LOGGER.debug("Building JSON string")
    jsonStr = '{"question":['
    q1Q = questions[0]
    q1Str = '{"number": "' + str(1) + '","text": "' + str(q1Q.text) + '","type": "' + str(q1Q.type.typeName)
    if len(q1Q.options) == 0:
        q1Str += '","options": "' + "none" + '"'
    else:
        optionsStr = '","options": {'
        o1Str = '"' + str(q1Q.options[0]) + '": "' + str(q1Q.options[0]) + '"'
        optionsStr += o1Str
        for n in range(1, len(q1Q.options)):
            o = q1Q.options[n]
            optionsStr += ',"' + str(o) + '": "' + str(o) + '"'
        optionsStr += "}"
        q1Str += optionsStr
    q1Str += (
        ',"required": "'
        + str(q1Q.required).lower()
        + '","dependent_on": "'
        + str(q1Q.dependent_on)
        + '","expected_answer": "'
        + str(q1Q.expected_answer)
        + '","abbrv": "'
        + str(q1Q.abbreviation)
        + '","score": "'
        + str(q1Q.score).lower()
        + '","comment": "'
        + str(q1Q.comment).lower()
        + '"}'
    )
    jsonStr += q1Str
    for n in range(1, len(questions)):
        q: Question = questions[n]
        questionStr = ',{"number": "' + str(n + 1) + '","text": "' + str(q.text) + '","type": "' + str(q.type.typeName)
        if len(q.options) == 0:
            questionStr += '","options": "' + "none" + '"'
        else:
            optionsStr = '","options": {'
            o1Str = '"' + str(q.options[0]) + '": "' + str(q.options[0]) + '"'
            optionsStr += o1Str
            for n in range(1, len(q.options)):
                o = q.options[n]
                optionsStr += ',"' + str(o) + '": "' + str(o) + '"'
            optionsStr += "}"
            questionStr += optionsStr
        questionStr += (
            ',"required": "'
            + str(q.required).lower()
            + '","dependent_on": "'
            + str(q.dependent_on)
            + '","expected_answer": "'
            + str(q.expected_answer)
            + '","abbrv": "'
            + str(q.abbreviation)
            + '","score": "'
            + str(q.score).lower()
            + '","comment": "'
            + str(q.comment).lower()
            + '"}'
        )
        jsonStr += questionStr
    jsonStr += "]}"
    writeJSONObjToFile(pathToFile, json.loads(jsonStr))


def readJSONObjFromFile(pathToFile: Path) -> object:
    """Function to read the content from a JSON file

    Args:
        pathToFile (Path): Path to the file, which should be read from

    Raises:
        FileNotFoundError: If the file doesn't exist

    Returns:
        object: The read JSON object
    """
    FileHandlerStash.LOGGER.debug("Checking if given file exists")
    if not pathToFile.exists():
        raise FileNotFoundError

    FileHandlerStash.LOGGER.debug("File existed. Reading JSON object from: " + str(pathToFile))
    with open(pathToFile, "r", encoding="utf-8") as file:
        jsonObj = json.load(file)
    return jsonObj


def writeJSONObjToFile(pathToFile: Path, jsonObj: object):
    """Function to write a JSON object to a file

    Args:
        pathToFile (Path): Path to the file, wich sould be written to
        jsonObj (object): The JSON object, that should be written to the file
    """
    FileHandlerStash.LOGGER.debug("Writing given JSON object to file: " + str(pathToFile))
    with open(pathToFile, "w", encoding="utf-8") as file:
        json.dump(obj=jsonObj, fp=file, indent=2, ensure_ascii=False)


def createSessionFile():
    """Creates a SessionFile if there is none

    Raises:
        FileExistsError: If there is already a SessionFIle
    """
    FileHandlerStash.LOGGER.debug("Checking if session file already exists")
    if FileHandlerStash.SESSION_FILE_PATH.exists():
        raise FileExistsError

    FileHandlerStash.LOGGER.debug("No session file. Creating a new one")
    open(FileHandlerStash.SESSION_FILE_PATH, "w").close()


def removeSessionFile():
    """Removes the SessionFile

    Raises:
        FileNotFoundError: If there is no SessionFile
    """
    FileHandlerStash.LOGGER.debug("Checking if session file exists")
    if not FileHandlerStash.SESSION_FILE_PATH.exists():
        raise FileNotFoundError

    FileHandlerStash.LOGGER.debug("Session file existed. Removing it")
    os.remove(FileHandlerStash.SESSION_FILE_PATH)


def readSessionFile() -> Questionnaire:
    """Reads the content of the SessionFile

    Raises:
        FileNotFoundError: If there is no SessionFile

    Returns:
        Questionnaire: The questionnaire read from the SessionFile
    """
    FileHandlerStash.LOGGER.debug("Checking if session file exists")
    if not FileHandlerStash.SESSION_FILE_PATH.exists():
        raise FileNotFoundError

    FileHandlerStash.LOGGER.debug("Session file exitsed. Reading from session file")
    with open(FileHandlerStash.SESSION_FILE_PATH, "r", encoding="utf-8") as file:
        jO = json.load(file)
        questions: list = []
        FileHandlerStash.LOGGER.debug("Building questions list")
        for q in jO["questions"]:
            options: list = []
            for o in q["options"]:
                options.append(o)
            question: Question = Question(
                text=q["text"],
                type=getTypeByTypeName(q["type"]["typeName"]),
                options=options,
                required=q["required"],
                dependent_on=q["dependent_on"],
                expected_answer=q["expected_answer"],
                abbreviation=q["abbreviation"],
                score=q["score"],
                comment=q["comment"],
                category=getQuestionCategoryByID(q["category"]["id"]),
                id=q["id"],
            )
            questions.append(question)
        FileHandlerStash.LOGGER.debug("Building and returning questionnaire")
        return Questionnaire(
            name=jO["name"],
            id=jO["id"],
            description=jO["description"],
            creationDate=jO["creationDate"],
            lastEdited=jO["lastEdited"],
            questions=questions,
            category=getQuestionnaireCategoryByID(jO["category"]["id"]),
        )


def writeToSessionFile(questionnaire: Questionnaire) -> bool:
    """Writes the given object to the SessionFile

    Args:
        questionnaire (Questionnaire): The object, that should be written to the SessionFile

    Returns:
        bool: True, if the writing was successfull
    """
    FileHandlerStash.LOGGER.debug("Writing questionnaire to session file")
    with open(FileHandlerStash.SESSION_FILE_PATH, "w", encoding="utf-8") as file:
        file.write(questionnaire.toJSON())
    return True


def createLogger(maxFileCount: int) -> logging.Logger:
    """Creates a logger and a logging.FileHandler and removes the oldest logfile to keep max 5 logfiles

    Returns:
        logging.Logger: The created logger with the FileHandler
    """
    logsDir: Path = Path(Path(os.getcwd()) / Path("log/"))
    logsDir.mkdir(exist_ok=True)
    loggerFormat = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s:%(funcName)s | %(message)s")
    logger: logging.Logger = logging.getLogger("MainLogger")
    logFile = logsDir / Path(time.strftime("%Y_%m_%d.log", time.localtime()))

    logFiles: list = list(logsDir.glob("*.log"))
    logFiles.sort()
    if len(logFiles) > 0 and len(logFiles) > maxFileCount and (Path(logFiles[-1]) != Path(logFile)):
        os.remove(logFiles[0])

    logFileHandler = logging.FileHandler(filename=logFile, mode="a")
    logFileHandler.setFormatter(loggerFormat)

    logger.addHandler(logFileHandler)
    FileHandlerStash.LOGGER = logger
    return logger


def setTypes(types: list):
    """Correlates the types list with the given types

    Args:
        types (list): The given types
    """
    FileHandlerStash.LOGGER.debug("Setting types")
    for typeName in types:
        FileHandlerStash.TYPES.append(typeName)


def setQuestionCategories(categories: list):
    """Correlates the categories list with the given categories

    Args:
        categories (list): The given categories
    """
    FileHandlerStash.LOGGER.debug("Setting question categories")
    for category in categories:
        FileHandlerStash.QUESTION_CATEGORIES.append(category)


def setQuestionnaireCategories(categories: list):
    """Correlates the categories list with the given categories

    Args:
        categories (list): The given categories
    """
    FileHandlerStash.LOGGER.debug("Setting questionnaire categories")
    for category in categories:
        FileHandlerStash.QUESTIONNAIRE_CATEGORIES.append(category)


def getTypeByTypeName(typeName: str) -> QuestionType:
    """Get a type object by it's name

    Args:
        typeName (str): The name of the type object

    Returns:
        QuestionType: The found type object
    """
    FileHandlerStash.LOGGER.debug("Getting QuestionType for typeName: " + typeName)
    for type in FileHandlerStash.TYPES:
        if typeName == type.typeName:
            return type


def getQuestionCategoryByID(catID: int = 1) -> QuestionCategory:
    """Gets a QuestionCategory by its ID

    Args:
        catID (int, optional): The ID to search for. Defaults to 1.

    Returns:
        QuestionCategory: The found category
    """
    FileHandlerStash.LOGGER.debug("Getting question category for ID: " + str(catID))
    default = None
    for category in FileHandlerStash.QUESTION_CATEGORIES:
        if category.id == catID:
            return category
        if category.id == 1:
            default = category
    return default


def getQuestionnaireCategoryByID(catID: int = 1) -> QuestionnaireCategory:
    """Gets a QuestionnaireCategory by its ID

    Args:
        catID (int, optional): The ID to search for. Defaults to 1.

    Returns:
        QuestionnaireCategory: The found category
    """
    FileHandlerStash.LOGGER.debug("Getting questionnaire category for ID: " + str(catID))
    default = None
    for category in FileHandlerStash.QUESTIONNAIRE_CATEGORIES:
        if category.id == catID:
            return category
        if category.id == 1:
            default = category
    return default


def createConfigFile():
    """
    Method to create a config file - if none is found - with given default parameters.
    :return:
    """
    Path(Path(os.getcwd()) / Path("config/")).mkdir(exist_ok=True)
    if not FileHandlerStash.CONFIG_FILE_PATH.exists():
        parser: configparser.ConfigParser = configparser.ConfigParser()
        parser["DEFAULT"] = {"UseQuestionAnswerLimit": "no", "QuestionAnswerLimit": "-1", "UseRecoveryPoints": "yes", "ShowTutorialDialog": "yes"}
        parser["DATABASE"] = {
            "UseNetworkDatabase": "no",
            "LocalDatabase": "data/mhf.db",
            "NetworkDatabaseAddress": "0.0.0.0",
            "NetworkDatabasePort": "0",
            "NetworkDatabaseUser": "",
            "NetworkDatabasePassword": "",
            "NetworkDatabase": "",
        }
        parser["USER INTERFACE"] = {"UseCustomColorCodes": "no", "CustomColorCodes": "FF, FF, FF", "UserIcon": Path(os.getcwd()) / Path("data/logo.png")}
        parser["DEBUGGING"] = {"LogFileMaxCount": "5"}
        with open(FileHandlerStash.CONFIG_FILE_PATH, "w") as configFile:
            parser.write(configFile)


def readConfigFile() -> Config:
    """
    Method to read from existing config file
    :return: config object with read attributes
    """
    if not FileHandlerStash.CONFIG_FILE_PATH.exists():
        raise FileNotFoundError

    parser: configparser.ConfigParser = configparser.ConfigParser()
    parser.read(FileHandlerStash.CONFIG_FILE_PATH)
    config: Config = Config()
    config.useQuestionAnswerLimit = parser.get("DEFAULT", "UseQuestionAnswerLimit") == "yes"
    config.useRecoveryPoints = parser.get("DEFAULT", "UseRecoveryPoints") == "yes"
    config.useNetworkDatabase = parser.get("DATABASE", "UseNetworkDatabase") == "yes"
    config.useCustomColorCodes = parser.get("USER INTERFACE", "UseCustomColorCodes") == "yes"
    config.showTutorialDialog = parser.get("DEFAULT", "ShowTutorialDialog") == "yes"

    config.logFileMaxCount = int(parser.get("DEBUGGING", "LogFileMaxCount"))
    config.localDatabase = Path(parser.get("DATABASE", "LocalDatabase"))

    config.networkDatabaseAddress = parser.get("DATABASE", "NetworkDatabaseAddress")
    config.networkDatabasePort = int(parser.get("DATABASE", "NetworkDatabasePort"))
    config.networkDatabaseUser = parser.get("DATABASE", "NetworkDatabaseUser")
    config.networkDatabasePassword = parser.get("DATABASE", "NetworkDatabasePassword")
    config.networkDatabase = parser.get("DATABASE", "NetworkDatabase")

    config.customColorCodes = parser.get("USER INTERFACE", "CustomColorCodes")

    config.userIcon = Path(parser.get("USER INTERFACE", "UserIcon"))

    config.questionAnswerLimit = int(parser.get("DEFAULT", "QuestionAnswerLimit"))

    return config


def updateConfig(key, value, category) -> Config:
    """
    Method to update values in the config file.
    :param key: config key to be updated
    :param value: value connected to the key to be updated
    :param category: category in which the key is put
    :return: updated config object
    """
    if not FileHandlerStash.CONFIG_FILE_PATH.exists():
        raise FileNotFoundError

    parser: configparser.ConfigParser = configparser.ConfigParser()
    parser.read(FileHandlerStash.CONFIG_FILE_PATH)
    parser.set(category, key, value)
    with open(FileHandlerStash.CONFIG_FILE_PATH, "w") as configFile:
        parser.write(configFile)
    return readConfigFile()
