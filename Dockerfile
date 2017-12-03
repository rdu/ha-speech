FROM node:9.2

WORKDIR /home
COPY credentials.json /home/credentials.json 
COPY node/* /home/
RUN npm install

ENV GOOGLE_APPLICATION_CREDENTIALS="/home/credentials.json"

EXPOSE 9000

ENTRYPOINT node /home/recognize.js
