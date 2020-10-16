FROM python:2.7-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip install numpy

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get -y install sudo

#RUN sudo apt-get -y install tesseract-ocr

COPY . /app

#RUN git clone --depth=1 https://majinghoozie:ghooziemajin1@github.com/jacoby149/tlibs

#RUN git clone --depth=1 https://majinghoozie:ghooziemajin1@github.com/jacoby149/initiald

EXPOSE 8000

CMD flask run --host=0.0.0.0 --port=80
