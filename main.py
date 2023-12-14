from ConfigInit import ConfigInit
from fileHandler import removeSessionFile

if __name__ == "__main__":
    ConfigInit.init()
    removeSessionFile()
