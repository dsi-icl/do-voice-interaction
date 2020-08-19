
# Dialog manager service

This service implements a [rasa assistant](https://rasa.com/docs/) to manage the dialog between the user and the voicebot. Our assistant uses [custom actions](https://rasa.com/docs/rasa/core/actions/#id2) which require connection to the [GDO GraphQL](https://github.com/dsi-icl/gdo-project-launcher). So, please, if you'd like to use it, make sure that [ove server](https://github.com/dsi-icl/gdo-project-launcher/tree/master/server) is launched by entering `npm start` in your console in the [proper directory](https://github.com/dsi-icl/gdo-project-launcher/tree/master/server). Else, you won't be able to use custom actions.

Moreover, you'll also have to update demo and tag entities each day, before training your model. Do `python update_demos_tags.py` with over server running.

## Virtual environment

### Install Rasa on virtual environment

Please, follow this [documentation](https://rasa.com/docs/rasa/user-guide/installation/) to install rasa on a virtual environment. 

### Build models 

You will not have to init a rasa-project, you can use the proposed project and adapt it as you wish. However, before any other actions, if you change the training data or the hyperparameters, polycies and so on, you'll have to retrain your model doing `rasa train -d config/domain.yml -c config/config.yml` in your virtual environment.

### Test your model

Just do `rasa test` in your virtual environment

### Use shell server

Execute `rasa shell` if you don't use any custom actions and `rasa shell --endpoints config/endpoints.yml` else, always in your virtual environment. 

## Run actions

Execute `rasa run actions --actions actions` in your virtual environment. 

## Run tests

In the [tests](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/dialog_manager_service/utilities/tests) folder, execute `python -m unittest test_utils_graphql.py` and `python -m unittest test_utils.py` in your virtual environment.

## How to use it with docker 

In [dialog_manager_service](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/dialog_manager_service), there's a [Makefile](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/dialog_manager_service/Makefile) which wille help you to execute the different rasa commands on docker. Plese, see, the [Rasa documentation on Docker](https://rasa.com/docs/rasa/user-guide/docker/building-in-docker/) to have more information about how the different commands work. 

### Build rasa on docker

Rasa provides several [docker images](https://hub.docker.com/u/rasa/#!). First, do `make docker rasa` to build rasa and rasa-sdk images on your docker. 

### Train

To train your assistant, use `make train`

### Test 

To test your assistant, use `make test`

### Shell

To communicate with your assistant on shell server, execute `make shell`. Please, take into account that if you want to use custom actions you'll have the following steps to consider:

1. For the first time, create a network with `make network`. 
2. Then, run actions with `make actions`.
3. Go to [endpoints.yml](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/dialog_manager_service/config/endpoints.yml), comment the localhost action endpoint and uncomment this : `url: "http://action-server:5055/webhook"`. 
4. In the [Makefile](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/dialog_manager_service/Makefile), uncomment `docker run -it -v $(shell pwd)):/app -p 5005:5005 --net rasa-net rasa/rasa:1.10.9-full shell --endpoints config/endpoints.yml` in shell part and comment the old command. 
5. Now, you can `make shell`.

Once you have finished, you can `make stop actions` to stop actions server running on docker. It happens that the server is still running and leads to errors when restarting the action-server. In this case, you can `make remove action-server`.

### Run 

Do `make server` to simply run rasa server. Please if you use custom actions for the first time, please follow the 2nd and 3rd steps of [Shell](#shell). 

### Use docker-compose

If you want to use [docker-compose](https://github.com/dsi-icl/do-voice-interaction/blob/master/gdo_voicebot/docker-compose.yml), `make build` to build the rasa_actions docker image for the first time. Then you can execute `docker-compose up` in the [gdo_voicebot](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot) folder

## Where to find the documentation

In the [docs](https://github.com/dsi-icl/do-voice-interaction/tree/master/gdo_voicebot/dialog_manager_service/docs) folder, ou'll find python documentation about the Dialog manager service.

To generate your own documentation, please use `pdoc --html -o docs/ <file_1.py> <file_2.py>` replacing `<file_n.py>`by the files containing documentation. If you want to use python scripts already implemented and to modify or update them just with nes documentation, do `pdoc --html --force -o docs/ actions/actions.py utilities/utils_graphql.py utilities/utils_actions.py utilities/actions_tools.py utilities/utils.py`.
