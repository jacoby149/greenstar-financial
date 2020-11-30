FROM python:3.5-buster

WORKDIR /app

RUN apt-get update

RUN apt-get -y install sudo

RUN pip install --upgrade pip

#stats packs
RUN pip install numpy scipy pandas statsmodels matplotlib

#zipline dependencies
RUN sudo apt-get -y install libatlas-base-dev python-dev gfortran pkg-config libfreetype6-dev hdf5-tools libhdf5-serial-dev

#zipline related stuff
RUN pip install yfinance

RUN pip install zipline
RUN pip install empyrical 
RUN pip install pyfolio 
RUN pip install alphalens

#talibs stuff
RUN sudo apt-get install build-essential
RUN apt-get install python-dev
RUN sudo pip install -U setuptools
COPY /ta-lib /app
RUN ./configure --prefix=/usr
RUN make
RUN sudo make install
RUN pip install ta-lib 

RUN pip install pyalgotrade

#fancy black scholes stuff
RUN apt-get -y install swig
RUN pip install vollib

RUN pip install cvxopt matplotlib

RUN pip install flask 
RUN pip install flask_cors

RUN sudo apt-get -y install texlive texlive-latex-extra texlive-fonts-recommended dvipng
RUN pip install latex
RUN pip install html5lib
RUN pip install BeautifulSoup4
RUN pip install pandas==0.23
RUN pip install fpdf
RUN pip install latex
RUN pip install opencv-python
RUN zipline --help
RUN find / -type d -name ".zipline" 

COPY . /app

#RUN python libs.py
CMD pip freeze > requirements.txt | python app.py
#CMD python multipdf.py
#CMD python yf.py

#EXPOSE 8000

#CMD flask run --host=0.0.0.0 --port=80
