# Data Observatory - Voice Assistant

The goal of this project is to provide a voice assistant to the [Data Observatory](https://www.imperial.ac.uk/data-science/data-observatory/) able to execute various commands and to support users during their presentation. 

## Description

<p align="center"><img src="https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/architecture-v3.png" width="500"/></p>

This project offers a modular framework for a voice-enabled chat service. The [voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/voicebot) folder contains the components of the voice assistant. You will find there the following services:
* [Dialog manager service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/dialog_manager_service/README.md)
* [Speech-to-Text service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/stt_service/README.md)
* [Voice assistant service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/voice_assistant_service/README.md)
* [Text-to-Speech service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/tts_service/README.md)
* [Emotion recognition service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/emotion_recognition_service/README.md)
* [Hotword detection service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/hotword_service/Readme.md)
* [Grammar correction service](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/grammar_correction_service/README.md)
* [(Draft) Speech Filler service](https://github.com/dsi-icl/do-voice-interaction/blob/experimental/bigram_naturalisation/voicebot/speech_filler_service/README.md)

There's also a [web client](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/voice_assistant_client/README.md) to help you with the interaction.

## Versions

The evolution of the system will be best seen after looking at the system diagrams for different versions:
* [Version 1](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/architecture-v1.png)
    * **Author(s):** [Aurélie Beaugeard](https://github.com/abeaugeard)
    * **Project type:** [UROP - 10 weeks](https://www.imperial.ac.uk/urop)
    * **Objective:** Setup the whole infrastructure for the system, creation of the initial dialogue model and first interactive model. 
* [Version 2](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/architecture-v2.png)
    * **Author(s):** [Mifu Suzuki](https://github.com/mifusuzuki)
    * **Project type:** MSc Individual Project - 5 months
    * **Objective:** Recognition of emotion from speech, translation of continuous emotions into a discrete space and adaptation of the dialogue model based on the recognized emotion. 
* [Version 3, Galileo Team](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/architecture-v3.png)
    * **Author(s):** [Bianca Ganescu](https://github.com/biancaganescu), [Izabella Kacprzak](https://github.com/izabellakacprzak), [Una Miralles](https://github.com/umiralles), [Vlad Nicolaescu](https://github.com/vladioannicolaescu), [Nicole Obretincheva](https://github.com/nobretincheva), [Alex Stocks](https://github.com/AlexanderJStocks)
    * **Project type:** Undergraduate Group Project - 8 weeks
    * **Objective:** Hotword detection. Grammar correction to improve transcription quality. A draft speech filler model. 

## Further reading

These models will help you to better understand how the project works:
* [Front-end perpective](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/front_end.png)
* [Back-end perspective](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/back_end.png)
* [Dialogue Use Case](https://github.com/dsi-icl/do-voice-interaction/blob/master/diagrams/use_case.png)

## Getting started

The various components of the project can be configured using the [docker compose file](https://github.com/dsi-icl/do-voice-interaction/blob/master/voicebot/docker-compose.yml). Several components require a bit of tweaking and configuration. All details should be available in the component readme file.

## Development

All the components can be run independently and the instruction should be found in the readme file of each service. 