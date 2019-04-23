FROM ubuntu:18.04

LABEL maintainer="Rafael Campos Nunes <rafaelnunes@engineer.com>"

RUN apt update && apt install sqlite3 python3 python3-pip -y

WORKDIR $HOME/jn-scraper

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000
#ENTRYPOINT ["make"]
