FROM node:14.18.1-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 22080
CMD ["npm", "start"]