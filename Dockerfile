FROM python:3.5-buster
WORKDIR /app
RUN apt-get update
RUN apt-get -y install sudo
RUN sudo apt-get -y install texlive texlive-latex-extra texlive-fonts-recommended dvipng
RUN sudo apt-get install -y texlive-science

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 80
CMD flask run --host=0.0.0.0 --port=80
