# Install node dependencies
FROM node:21-slim as build

COPY ./server /code

WORKDIR /code/clerq/node_tools

RUN npm install

# Django
FROM python:3.10-slim

RUN apt update
RUN pip install --upgrade pip

COPY --from=build /code/clerq /code/clerq
COPY ./docker/django/entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]