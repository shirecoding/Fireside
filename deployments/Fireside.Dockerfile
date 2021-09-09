FROM python:slim-buster

# copy context dir to code
COPY ./ /code

RUN pip install --upgrade pip
RUN pip install -r /code/deployments/requirements.txt

WORKDIR /code
