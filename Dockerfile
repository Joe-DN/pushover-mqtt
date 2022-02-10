FROM alpine

RUN sed -i.bak 's+https://+http://+' /etc/apk/repositories
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /pushover-mqtt

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD pushoverClient.py .
ADD configLoader.py .
ADD config.json .

CMD ["python3", "pushoverClient.py"]