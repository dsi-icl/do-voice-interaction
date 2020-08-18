# do-voice-interaction

The goal of this project is to provide a voice assistant to the Global Data Observatory able to execute various display commands and to support users during their presentation. 

## Specifications

<p align="center"><img src="https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/use_case.png" width="500"/></p>

We'll have two actors : the presenter and the GDO. They'll interact through the voicebot system. These actions will be executed using the [GDO Project Launcher](https://github.com/dsi-icl/gdo-project-launcher). Greet, Help and Goodbye actions will be directly managed by the voicebot without interaction with the GDO.

## Description

<p align="center"><img src="https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/voice_assistant%20_architecture.png" width="500"/></p>

This project offers a modular framework for a voice-enabled chat service. The [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot) directory contains the microservices architecture. You will find there the following services:
* [Dialog manager service](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/dialog_manager_service/README.md)
* [Speech-to-Text service](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/stt_service/README.md)
* [Voice assistant service](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/voice_assistant_service/README.md)
* [Text-to-Speech service](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/tts_service/README.md)

You'll also find a [react client](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/voice_assistant_client/README.md)

## Documentation

These two models will help you to better understand how the project works:
* [Front-end perpective](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/front_end.png)
* [Back-end perspective](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/back_end.png)

