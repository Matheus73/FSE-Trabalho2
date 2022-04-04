FROM python:3.8 

ENV TZ=America/Sao_Paulo

RUN apt-get update 

WORKDIR /home

COPY docker/requirements.txt .

RUN pip install -r requirements.txt 

COPY ./src/ ./src/
COPY ./start.sh ./start.sh

EXPOSE 5000

CMD ./start.sh
