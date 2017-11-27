import socket
import multiprocessing
import speech_recognition as sr
import io
import os
import wave
import paho.mqtt.client as mqtt
import re

SERVICE_PORT = os.environ.get('SERVICE_PORT', 1998)
MQTT_HOST = os.environ.get('MQTT_HOST', "10.10.0.137")
MQTT_PORT = os.environ.get('MQTT_PORT', 1883)
MQTT_PUBLISH_TOPIC = os.environ.get('MQTT_PUBLISH_TOPIC', "commandprocessor/process")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()


r = sr.Recognizer()

HOST = '0.0.0.0'
PORT = SERVICE_PORT
ADDR = (HOST,PORT)
BUFSIZE = 4096

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(ADDR)
serv.listen(5)

print('listening on port: ', SERVICE_PORT)

total = 0
while True:
  conn, addr = serv.accept()
  print('client connected ... ', addr)

  with io.BytesIO() as wav_file:
      wav_writer = wave.open(wav_file, "wb")
      try:
          wav_writer.setframerate(16000)
          wav_writer.setsampwidth(2)
          wav_writer.setnchannels(1)
          while True:
              data = conn.recv(BUFSIZE)
              if not data: break
              wav_writer.writeframes(data)
      finally:
          wav_file.seek(0)
          wav_writer.close()

      try:
        with sr.AudioFile(wav_file) as source:
           try:
             audio = r.record(source)
           except Exception as e:
             print(e)
        try:
          transcript = r.recognize_google_cloud(audio, language="de-DE")
        except sr.UnknownValueError:
          transcript = "Fehler bei der Spracherkennung"	
        except sr.RequestError as e:
          transcript = "Die Spracherkennung funktioniert im Moment nicht"
	
        print("say:", transcript)
	client.publish(MQTT_PUBLISH_TOPIC, transcript)

#        try:
#            command = r.recognize_google(audio, language="de-DE", key="")
#            print("command:", command)
#            client.publish("commandprocessor/process", command)
#        except sr.UnknownValueError:
#            print("Speech Recognition could not understand audio")
#        except sr.RequestError as e:
#            print("Speech Recognition service; {0}".format(e))


      except Exception as sl:
        print(sl)

      wav_writer.close()
      conn.close()
      print('client disconnected')
