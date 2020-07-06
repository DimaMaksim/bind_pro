FROM registry.fozzy.lan/calcengine/flaskbasic
#FROM python:3.7.6
COPY . /app/

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN ["apt-get", "update"]


RUN apt -y install curl
RUN apt -y install build-essential
RUN apt -y install unixodbc-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt -y update



RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17
RUN DEBIAN_FRONTEND=noninteractive apt -y install krb5-user



#RUN ["apt-get", "-y", "install", "vim"]


CMD ["/bin/bash","-c","python3 starter.py & tail -f /dev/null"]
