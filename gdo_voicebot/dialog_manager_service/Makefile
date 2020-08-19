docker rasa:
	docker pull rasa/rasa
	docker pull rasa/rasa-sdk
	
build:
	docker build . -t rasa_actions

train:
	docker run -v $(shell pwd):/app rasa/rasa:1.10.9-full train -d config/domain.yml -c config/config.yml

test:
	docker run --user root -v $(shell pwd):/app rasa/rasa:1.10.9-full test

shell:
	docker run -it -v $(shell pwd):/app rasa/rasa:1.10.9-full shell --endpoints config/endpoints.yml
	#docker run -it -v $(shell pwd)):/app -p 5005:5005 --net rasa-net rasa/rasa:1.10.9-full shell --endpoints config/endpoints.yml

network:
	docker network create rasa-net

server:
	docker run -v $(shell pwd):/app rasa/rasa:1.10.9-full run --endpoints config/endpoints.yml --credentials config/credentials.yml

actions:
	docker run -d -v $(shell pwd)/actions:/app/actions --net rasa-net --name action-server rasa/rasa-sdk:2.0.0a1

#with virtual environment
run actions:
	rasa run actions --actions actions

stop actions:
	docker stop action-server

remove action-server:
	docker rm action-server
