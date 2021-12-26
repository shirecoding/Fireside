FROM python:slim-buster

COPY ./firesidegames                    /firesidegames
COPY ./deps/RxPipes                     /deps/RxPipes
COPY ./deps/VeryPowerfulAgents          /deps/VeryPowerfulAgents
COPY ./deps/FSGAgent                    /deps/FSGAgent

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip
RUN pip install -r /firesidegames/requirements.txt
RUN pip install -U /deps/RxPipes
RUN pip install -U /deps/VeryPowerfulAgents
RUN pip install -U /deps/FSGAgent

ENV PYTHONPATH "/deps/RxPipes:/deps/VeryPowerfulAgents:/deps/FSGAgent:${PYTHONPATH}"

WORKDIR /firesidegames
