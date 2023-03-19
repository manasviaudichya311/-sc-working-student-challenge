FROM python:3.8-alpine

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

RUN chmod +x /wait

WORKDIR /usr/src/app

COPY client.py requirements.txt ./

RUN pip install -r requirements.txt

CMD /wait && python3 client.py
