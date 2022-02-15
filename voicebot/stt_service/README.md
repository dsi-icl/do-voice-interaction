# Speech-To-Text service

## Description

This service will take care of receiving the voice message and transcribing it using the [Mozilla's DeepSpeech](https://github.com/mozilla/STT) model. To learn more about DeepSpeech, you can access to the documentation [here](https://mozilla-voice-stt.readthedocs.io/en/latest/index.html). In the [stt.js](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/stt_service/src/routes/stt.js) file you'll find how the received audioBuffer is processed.

## How to install it

`npm install` to install all dependencies.

If you don't want to use docker, please make sure, that you installed deepspeech models by executing the following command `./download_models.sh`

## How to check and correct the syntax

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot) you'll find a [lint bash](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/lint.sh) that will check the integrality of the syntax in each microservice. Execute `./lint.sh` to symply check the syntax and `./lint.sh --fix` to correct syntax errors automaticaly.

Locally you can execute `npm run lint`or`npm run lint:fix`.

## How to run it

 Use `npm run start:dev` if you want the server to be refreshed automatically at any modification in the code. Else you can directly use `npm run start`

## How to use it with docker

In the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot), you'll find a [docker-compose](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/docker-compose.yml) file. Here you can run `docker-compose up do-voice-stt-service` and that's it.

## Where to find the documentation

In the [docs](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/stt_service/docs) folder, you'll find javascript documentation about the Speech-to-Text service. 

To generate your own [documentation](https://jsdoc.app/), please use `jsdoc <file_1.js> <file_2.js>` indicating all documented javascripts files.
