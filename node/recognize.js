var net = require('net');
var mqtt = require('mqtt')

var PORT=process.env.PORT || 9000;
var MQTT_URL=process.env.MQTT_URL || "mqtt://10.10.0.137";
var MQTT_PUBLISH_TOPIC = process.env.MQTT_PUBLISH_TOPIC || "test_speak/speak";

var mqttClient  = mqtt.connect(MQTT_URL);

var canPost = false;

mqttClient.on('connect', function () {
    canPost = true;
});


mqttClient.on('close', function () {
    canPost = false;
});

mqttClient.on('offline', function () {

    canPost = false;
});

var server = net.createServer();  
server.on('connection', handleConnection);

server.listen(9000, function() {  
  console.log('server listening to %j', server.address());
});

function handleConnection(conn) {  
  var remoteAddress = conn.remoteAddress + ':' + conn.remotePort;
  console.log('new client connection from %s', remoteAddress);

  conn.once('close', onConnClose);
  conn.on('error', onConnError);

  streamingRecognize(conn);

  function onConnData(d) {
    console.log('connection data from %s: %j', remoteAddress, d);
    conn.write(d);
  }

  function onConnClose() {
    console.log('connection from %s closed', remoteAddress);
  }

  function onConnError(err) {
    console.log('Connection %s error: %s', remoteAddress, err.message);
  }
}


function streamingRecognize(sh) 
{
  const fs = require('fs');
  const speech = require('@google-cloud/speech');
  const client = new speech.SpeechClient();

  const request = {
    config: {
      encoding: 'LINEAR16',
      sampleRateHertz: 16000,
      languageCode: 'de-DE',
    },
    interimResults: false,
  };

  const recognizeStream = client
    .streamingRecognize(request)
    .on('error', console.error)
    .on('data', data => {
      console.log(
        `Transcription: ${data.results[0].alternatives[0].transcript}`
      );
      if (canPost)
      {
        mqttClient.publish(MQTT_PUBLISH_TOPIC, data.results[0].alternatives[0].transcript);
      }
      else
      {
	console.log("mqqt offline, not posting");
      }
    });

  sh.pipe(recognizeStream)
}

