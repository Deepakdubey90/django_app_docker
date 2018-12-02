# base image
FROM python:3

ENV PYTHONUNBUFFERED 1

# code directoy
RUN mkdir /code

WORKDIR /code

# install virtualenv
RUN pip install virtualenv

# create virtual env
RUN virtualenv -p python3 venv

# activate
RUN . venv/bin/activate

#add requirements file
ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/
