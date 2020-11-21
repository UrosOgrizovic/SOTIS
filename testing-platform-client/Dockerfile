FROM node:12-alpine3.10

WORKDIR /app
CMD ["yarn", "serve", "-H", "0.0.0.0"]

COPY package.json yarn.lock ./
RUN set -ex && \
	yarn

COPY ./ ./
RUN set -ex && \
	yarn build

