FROM node:lts
LABEL maintainer="o.serban@imperial.ac.uk"

ENV APPLICATION_PATH /app

WORKDIR $APPLICATION_PATH

COPY download_models.sh .
RUN ./download_models.sh

COPY . .
RUN npm install -g n
RUN n 12.22.9
RUN npm install -g npm@8.5.1
RUN npm install

CMD ["npm", "start"]