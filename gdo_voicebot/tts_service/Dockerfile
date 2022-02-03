FROM node:lts-alpine as builder
LABEL maintainer="o.serban@imperial.ac.uk"

WORKDIR /code

COPY . .

RUN npm install && npm run build

# The optimized docker image
FROM node:lts-alpine

ENV APPLICATION_PATH /app
ENV APPLICATION_USER user

WORKDIR $APPLICATION_PATH
ENV LD_LIBRARY_PATH="/app/cereproc/cereproc_lib/cerevoice_eng/lib:${LD_LIBRARY_PATH}"

RUN adduser -D -g '' $APPLICATION_USER && mkdir -p $APPLICATION_PATH && chown -R $APPLICATION_USER $APPLICATION_PATH
USER $APPLICATION_USER

COPY --from=builder /code/dist/index.js .

CMD ["node", "index.js"]