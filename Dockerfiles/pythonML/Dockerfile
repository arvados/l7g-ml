FROM arvados/jobs:latest

USER root

RUN echo "deb http://deb.debian.org/debian stretch main" > /etc/apt/sources.list.d/stretch.list

RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install python-pip -y
RUN apt-get install python-numpy -y
RUN apt-get install python-scipy -y
RUN apt-get install python-matplotlib -y
RUN apt-get install python-pandas -y
RUN apt-get clean

RUN pip install sklearn
RUN pip install --upgrade scipy
