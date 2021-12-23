FROM python:slim-buster

COPY ./deps/RxPipes             /deps/RxPipes
COPY ./deps/VeryPowerfulAgents  /deps/VeryPowerfulAgents
COPY ./deps/FSGAgent            /deps/FSGAgent
COPY ./deployments/scripts      /deployments/scripts

RUN pip install --upgrade pip
RUN bash /deployments/scripts/install_dependencies.sh

WORKDIR /deps