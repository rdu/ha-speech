FROM debian:stretch

RUN apt-get update
RUN apt-get install -y python3 python3-pip wget htop vim mc
#RUN apt-get install -y swig3.0 python-pyaudio python3-pyaudio sox
RUN pip3 install --upgrade pip
#RUN pip3 install pyaudio
RUN apt-get install -y python3-all-dev python3-pip build-essential swig git libpulse-dev 
ENV LANG C.UTF-8
#RUN pip3 install pocketsphinx
RUN pip3 install SpeechRecognition
RUN pip3 install google-api-python-client
RUN pip3 install --upgrade google-api-python-client
RUN pip3 install paho-mqtt
#RUN apt-get install -y libatlas-base-dev
#RUN apt-get install -y alsa-utils unzip openssh-server libpython2.7 bzip2
#ENV AUDIODEV=hw:1,0
#ENV AUDIODRIVER=alsa
WORKDIR /home
COPY credentials.json /home/credentials.json 
COPY server.py /home/server.py

ENV GOOGLE_APPLICATION_CREDENTIALS="/home/credentials.json"

#ADD https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.1.tar.bz2  /home

#RUN tar xfj rpi*.bz2

#COPY asoundrc /root/.asoundrc
#COPY idle.sh /home/idle.sh

ENTRYPOINT python3 /home/server.py
