FROM python:slim-buster

COPY ./deps/RxPipes             /deps/RxPipes
COPY ./deps/VeryPowerfulAgents  /deps/VeryPowerfulAgents
COPY ./deps/FSGAgent            /deps/FSGAgent

RUN apt-get update \
    && apt-get -y install entr

RUN pip install --upgrade pip
RUN pip install -U /deps/RxPipes
RUN pip install -U /deps/VeryPowerfulAgents
RUN pip install -U /deps/FSGAgent

ENV PYTHONPATH "/deps/RxPipes:/deps/VeryPowerfulAgents:/deps/FSGAgent:${PYTHONPATH}"
ENV PATH "/deps/FSGAgent/bin:${PATH}"

WORKDIR /deps
