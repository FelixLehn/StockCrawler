# pull official base image
FROM node:13.12.0-alpine as build

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
ADD . /app

RUN npm run build

FROM nginx:1.17-alpine

COPY --from=build /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx.conf /etc/nginx/conf.d 

EXPOSE 80 

CMD ["nginx", "-g", "daemon off;"]