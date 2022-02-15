# Hotword Detection service

## Description
This service detects if the DO-Hotword "Hey Galileo" (or any other configured hotword in the config.json file) is present in the audio data that it has received. In the GDO voicebot, the voice assistent client listens in the background and every time it hears a voice, it sends the audio data (via the voice assistent service) to this Hotword Detection service. Here is what happens:

1. The service receives the audio data from the Voice Assistent [service](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/voice_assistant_service) via a POST request (the audio data is the body of the request).
2. If the body is not as expected it returns 400, otherwise it starts analysing the data.
3. It uses an open-source third party library [hotword-library](https://github.com/mathquis/node-personal-wakeword/) for the actual hotword detection. The function "getHotword" from [hotword.js](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/hotword_service/src/routes/hotword.js) creates a KeywordClient object of the [hotword-library] and configures it with the corresponding keyword samples, sample rate, and thresholds.
4. The audio data is transformed into a buffer and then saved to a file. The service has a maximum number of files that is allowed to save (which should be mentioned in the config file), each having a unique identifier. This is beacuse of the [hotword-library] configurations, direct streams not being interpreted as expected.
5. Eventually, the audio file gets transformed into a read stream, which is piped to the keywordClient object that listens for the hotword.
6. After the hotword is detected or th maximum wait time configured passes, the service responds with a 200 status code (it was successful if it reached this place), and a text message in saying 'detected' or 'not-detected' as necessary.

The response is then interpreted in the [service](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/voice_assistant_service), which in a 'detected' will make the [client](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/voice_assistant_client) start listening for the command.

## How to install it

`npm install` to install all dependencies.

## How to run it

Use `npm run start` for the whole service. If you just want the [hotword.js](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/hotword_service/src/routes/hotword.js) file, use `node hotword.js`.

## How to test it

Use `npm run test`. With a correct configuration, all tests should pass.

## How to use it with docker

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot), you'll find a [docker-compose](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/docker-compose.yml) file. Here you can run `docker-compose up do-voice-hotword-service` and that's it.

## Where to find the documentation

In the [docs](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/hotword_service/docs) folder, you'll find javascript documentation about the Hotword Detection service. 

To generate your own [documentation](https://jsdoc.app/), please use `jsdoc <file_1.js> <file_2.js>` indicating all documented javascripts files.
