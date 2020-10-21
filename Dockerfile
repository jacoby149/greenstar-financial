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


#download data
RUN export QUANDL_API_KEY="GL6R8mpKFfHJWvpmkNxV" && zipline ingest -b quandl

RUN pip install flask 
RUN pip install flask_cors

COPY . /app

#RUN python libs.py
CMD python app.py

#EXPOSE 8000

#CMD flask run --host=0.0.0.0 --port=80
