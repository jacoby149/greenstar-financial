FROM python:3.5-buster

WORKDIR /app

RUN apt-get update

RUN apt-get -y install sudo

RUN pip install --upgrade pip

#stats packs
RUN pip install numpy scipy pandas statsmodels matplotlib

#zipline related stuff
RUN pip install yfinance

RUN pip install cvxopt matplotlib

RUN pip install flask 
RUN pip install flask_cors

RUN sudo apt-get -y install texlive texlive-latex-extra texlive-fonts-recommended dvipng
RUN pip install latex
RUN sudo apt-get install -y texlive-science
RUN pip install html5lib
RUN pip install BeautifulSoup4

RUN pip install latex
RUN pip install opencv-python
RUN pip install pandas_datareader
RUN pip install sympy
RUN pip install mpld3
RUN pip install SQLAlchemy

COPY . /app
CMD pip freeze > requirements.txt
EXPOSE 80
CMD flask run --host=0.0.0.0 --port=80
