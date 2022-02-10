# pushover-mqtt

pub on topic pushover/notification/app1 to send a message to app1

## Build 
docker build -t pushover-mqtt .

## Run

docker run -v ${PWD}/config.json:/pushover-mqtt/config.json pushover-mqtt:latest
