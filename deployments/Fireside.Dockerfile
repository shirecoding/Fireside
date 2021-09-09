FROM python:slim-buster

# copy context dir to code
COPY ./ /code

WORKDIR /code

RUN bash /code/deployments/scripts/install_dependencies.sh