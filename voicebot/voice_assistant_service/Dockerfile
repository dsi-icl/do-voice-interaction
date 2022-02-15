FROM node:lts-alpine as builder
LABEL maintainer="aurelie.beaugeard20@imperial.ac.uk"

WORKDIR /code/backend
COPY ./voice_assistant_service/ .
RUN npm install && npm run build

WORKDIR /code/ui
COPY ./voice_assistant_client/ .
RUN npm install && npm run build

# The optimized docker image
FROM node:lts-alpine

ENV APPLICATION_PATH /app
ENV APPLICATION_USER user

WORKDIR $APPLICATION_PATH

RUN adduser -D -g '' $APPLICATION_USER && mkdir -p $APPLICATION_PATH && chown -R $APPLICATION_USER $APPLICATION_PATH
USER $APPLICATION_USER

COPY --from=builder /code/backend/dist/ .

RUN mkdir -p $APPLICATION_PATH/public
COPY --from=builder /code/ui/build/ public/

CMD ["node", "index.js"]
