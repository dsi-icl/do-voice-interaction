
# Voice-assistant service

## Description

This service is the heart of our architecture since it will allow communication between the different departments and the client. Here's how he does it :

1. It receives the user's voice message from the [client](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/voice_assistant_client) via a socket.
2. It posts it to the stt service and gets the text message.
3. Then, it transfers this message to the the dialog manager service and gets the bot response.
4. It posts the bot text response to the tts service and gets the bot voice answer.
5. This voice answer is sent to the client through the socket with the text exchange to be displayed.

You can see in details how it's done in the [voice_assistant.js](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/voice_assistant_service/src/routes/voice_assistant.js) file.

## How to install it

`npm install` to install all dependencies.

## How to build it

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot) you'll find a [build bash](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/build.sh) that will build tts and voice-assistant services. To use this bash, run `./build.sh`.

Locally you can execute `npm run build`

## How to check and correct the syntax

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot) you'll find a [lint bash](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/lint.sh) that will check the integrality of the syntax in each microservice. Execute `./lint.sh` to symply check the syntax and `./lint.sh --fix` to correct syntax errors automaticaly.

Locally you can execute `npm run lint`or`npm run lint:fix`.

## How to run it

Use `npm run start:dev` if you want the server to be refreshed automatically at any modification in the code. Else you can directly use `npm run start`

## How to use it with docker

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot), you'll find a [docker-compose](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/docker-compose.yml) file. Here you can run `docker-compose up do-voice-assistant-service` and that's it.

## Where to find the documentation 

In the [docs](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/voice_assistant_service/docs) folder, you'll find javascript documentation about the Text-To-Speech service. 

To generate your own [documentation](https://jsdoc.app/), please use `jsdoc <file_1.js> <file_2.js>` indicating all documented javascripts files.
