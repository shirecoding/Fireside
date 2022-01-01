FROM python:slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc wget zip procps

RUN pip install --upgrade pip

# Watchman

ARG WM_VERSION=v2021.03.01.00

RUN wget https://github.com/facebook/watchman/releases/download/$WM_VERSION/watchman-$WM_VERSION-linux.zip && \
    unzip watchman-$WM_VERSION-linux.zip && \
    cd watchman-$WM_VERSION-linux && \
    mkdir -p /usr/local/{bin,lib} /usr/local/var/run/watchman && \
    cp bin/* /usr/local/bin && \
    cp lib/* /usr/local/lib && \
    chmod 755 /usr/local/bin/watchman && \
    chmod 2777 /usr/local/var/run/watchman && \
    cd .. && \
    rm -fr watchman-$WM_VERSION-linux.zip watchman-$WM_VERSION-linux

# FSGAgent

COPY ./deps/RxPipes             /deps/RxPipes
COPY ./deps/VeryPowerfulAgents  /deps/VeryPowerfulAgents
COPY ./deps/FSGAgent            /deps/FSGAgent

RUN pip install -U /deps/RxPipes
RUN pip install -U /deps/VeryPowerfulAgents
RUN pip install -U /deps/FSGAgent

ENV PYTHONPATH "/deps/RxPipes:/deps/VeryPowerfulAgents:/deps/FSGAgent:${PYTHONPATH}"
ENV PATH "/deps/FSGAgent/bin:${PATH}"

WORKDIR /deps
