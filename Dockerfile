FROM python:3.8 

ENV TZ=America/Sao_Paulo

RUN apt-get update 

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY ./central/ ./central/
COPY ./start.sh ./start.sh

EXPOSE 10048

RUN chmod 777 ./start.sh

CMD ./start.sh
