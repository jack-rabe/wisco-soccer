# syntax=docker/dockerfile:1

# base image from https://hub.docker.com/r/nikolaik/python-nodejs
FROM nikolaik/python-nodejs:python3.10-nodejs12

WORKDIR /app

COPY ["package.json", "package-lock.json*", "requirements.txt", "./"]

RUN npm install

RUN pip install -r requirements.txt

COPY . .

CMD ["node", "server.js"]