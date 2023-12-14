import os
from pathlib import Path


class Config:
    """
    Class representing the programs configuration during runtime.
    """

    def __init__(self):
        """
        Constructor
        """
        self.useQuestionAnswerLimit: bool = False
        self.useRecoveryPoints: bool = True
        self.useNetworkDatabase: bool = False
        self.useCustomColorCodes: bool = False

        self.logFileMaxCount: int = 5
        self.localDatabase: Path = Path("")

        self.networkDatabaseAddress: str = ""
        self.networkDatabasePort: int = -1
        self.networkDatabaseUser: str = ""
        self.networkDatabasePassword: str = ""
        self.networkDatabase: str = ""

        self.customColorCodes: str = ""
        self.userIcon: Path = Path(os.getcwd()) / Path("data/logo.png")
