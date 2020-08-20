# GDO Voicebot

From this folder there is a simple way to run each service with one command : `docker-compose up`.

Please, before, don't forget to indicate your local ip address in th [config.docker.yml](https://github.com/dsi-icl/do-voice-interaction/blob/2849c5f4cd586189bfdc64be7443c024179c3d74/gdo_voicebot/dialog_manager_service/config/config.docker.yml#L30) file, in the [credentials.docker.yml](https://github.com/dsi-icl/do-voice-interaction/blob/2849c5f4cd586189bfdc64be7443c024179c3d74/gdo_voicebot/dialog_manager_service/config/credentials.docker.yml#L12) and in the [config.docker.json](https://github.com/dsi-icl/do-voice-interaction/blob/2849c5f4cd586189bfdc64be7443c024179c3d74/gdo_voicebot/voice_assistant_service/config/config.docker.json#L5) file.

With the actual React client, you'll have also to modify the [config.js](https://github.com/dsi-icl/do-voice-interaction/blob/2849c5f4cd586189bfdc64be7443c024179c3d74/gdo_voicebot/voice_assistant_client/public/js/config.js#L1) file and replace localhost by the IP address of do-voice-assistant-service container. To get this IP, write `docker inspect do-voice-assistant-service` in a terminal after having launched the docker-compose. Copy the IP address in the config file.

