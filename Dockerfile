FROM python:3.7-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install sudo
RUN sudo apt-get -y install tesseract-ocr
COPY . /app
EXPOSE 80
CMD flask run --host=0.0.0.0 --port=80