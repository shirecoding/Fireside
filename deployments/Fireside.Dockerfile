FROM python:slim-buster

COPY ./firesidegames                    /firesidegames
COPY ./deps/RxPipes                     /deps/RxPipes
COPY ./deps/VeryPowerfulAgents          /deps/VeryPowerfulAgents
COPY ./deps/FSGAgent                    /deps/FSGAgent
COPY ./deployments/scripts              /deployments/scripts

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip
RUN pip install -r /firesidegames/requirements.txt
RUN bash /deployments/scripts/install_dependencies.sh

WORKDIR /firesidegames
