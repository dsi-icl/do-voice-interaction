FROM node:current-buster
LABEL maintainer="o.serban@imperial.ac.uk"

ENV APPLICATION_PATH /app

WORKDIR $APPLICATION_PATH

COPY . .
RUN npm install

CMD ["npm", "start"]