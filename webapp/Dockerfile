FROM node:14-alpine as builder

LABEL maintainer="NMDP Bioinformatics"

COPY package.json package-lock.json ./

RUN npm ci && mkdir /ng-app && mv ./node_modules ./ng-app

WORKDIR /ng-app

COPY . .

ARG CONFIGURATION=production
RUN npm run ng build -- --configuration=$CONFIGURATION


FROM nginx:1.19-alpine

LABEL maintainer="NMDP Bioinformatics"

RUN rm -rf /usr/share/nginx/html/*

## The "ng build" creates artifact in  dist/dpb1-pred-ui-tool directory, should be updated 
COPY --from=builder ./ng-app/dist/dpb1-pred-ui-tool /usr/share/nginx/html
COPY nginx-conf/default.conf /etc/nginx/conf.d/

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]