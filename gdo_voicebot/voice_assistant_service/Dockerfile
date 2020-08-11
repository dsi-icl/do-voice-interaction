FROM node:lts
LABEL maintainer="aurelie.beaugeard20@imperial.ac.uk"

ENV APPLICATION_PATH /app

WORKDIR $APPLICATION_PATH

COPY . .
RUN npm install && npm run build

CMD ["node", "src/app.js"]
