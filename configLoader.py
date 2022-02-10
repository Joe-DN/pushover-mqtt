import json

class ConfigLoader():

    def __init__(self):
        self.__pushoverConfig = {}
        self.__loadConfig()

    def __loadConfig(self):
        config = {}
        try:
            with open('config.json', 'r') as configFile:
                self.__pushoverConfig = json.loads(configFile.read())
        except Exception as e:
            print(e)

    def apiKey(self):
        key = ""

        try:
            key = self.__pushoverConfig["user-api-key"]
        except:
            pass

        return key

    def mqttHost(self):
        host = ""

        try:
            host = self.__pushoverConfig["mqtt-host"]
        except:
            pass

        return host

    def mqttPort(self):
        port = 1883

        try:
            port = self.__pushoverConfig["mqtt-port"]
        except:
            pass

        return port

    def getAppKey(self, appName):
        key = ""
        try:
            for application in self.__pushoverConfig["applications"]:
                if application["name"] == appName:
                    key = application["api-key"]
                    break
        except:
            pass

        return key
            