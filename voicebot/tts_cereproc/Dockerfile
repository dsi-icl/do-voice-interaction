FROM node:10.19-alpine as builder
LABEL maintainer="ben.kirwan21@imperial.ac.uk"

WORKDIR /code

COPY . .

RUN npm install && npm run build

# The optimized docker image
FROM node:10.19-alpine

ENV APPLICATION_PATH /app
ENV APPLICATION_USER user
# ENV LS_LIBRARY_PATH 

WORKDIR $APPLICATION_PATH

RUN adduser -D -g '' $APPLICATION_USER && mkdir -p $APPLICATION_PATH && chown -R $APPLICATION_USER $APPLICATION_PATH


USER $APPLICATION_USER

COPY --from=builder /code/dist/index.js .

ENV LD_LIBRARY_PATH /app/cerevoice/sdk/cerevoice_eng/lib/

CMD ["node", "index.js"]