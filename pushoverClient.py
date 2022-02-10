import json
import time
import logging
import requests
import paho.mqtt.client as mqtt
from configLoader import ConfigLoader

logging.basicConfig(format='[%(levelname)s]\t%(asctime)s - %(message)s', level=logging.INFO)

class PushoverClient(mqtt.Client):

    def __init__(self):
        super().__init__()
        self.__config = ConfigLoader()
        self.will_set("pushover/status","offline", retain=True)

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Broker connection successful")
        self.publish("pushover/status","online", retain=True)  

    def on_connect_fail(self, mqttc, obj):
        logging.info("Broker connection failed")

    def on_message(self, mqttc, obj, msg):
        try:
            self.sendPushoverMessage(str(msg.topic).split("/")[2],msg.payload.decode('UTF-8'))
        except:
            pass

    def sendPushoverMessage(self, appName, message):
        apiKey = self.__config.getAppKey(appName)

        if not apiKey:
            logging.error("Unknown application - " + appName)
            return      

        payload = {"message": message, "user": self.__config.apiKey(), "token": apiKey}

        try:
            r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
        
            if not r.status_code == 200:
                logging.error("Failed to send message to " + appName + ", got error from pushover - "+r.text)
            else:
                logging.info("Successfully sent message to " + appName)
        except Exception as e:
            logging.error("Failed to send message to " + appName + ", got internal error - "+e)


    def on_log(self, mqttc, obj, level, string):
        pass
        #logging.info(string)

    def run(self):
        self.connect(self.__config.mqttHost(), self.__config.mqttPort(), 60)
        self.subscribe("pushover/notification/+", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc

if __name__ == '__main__':
    
    mqttc = PushoverClient()
    
    try:
        rc = mqttc.run()
        logging.error("Pushover Client exited with response code " + str(rc))
    except KeyboardInterrupt:
        print("")