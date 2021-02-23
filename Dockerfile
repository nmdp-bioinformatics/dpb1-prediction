FROM node:14-alpine as angular-builder

LABEL maintainer="NMDP Bioinformatics"

COPY webapp/package.json webapp/package-lock.json ./
RUN npm ci && mkdir /ng-app

WORKDIR /ng-app
COPY ./webapp/ .
RUN npm install -g @angular/cli && npm install
ARG CONFIGURATION=production
RUN npm run ng build -- --configuration=$CONFIGURATION


# Build TCE Prediction Tool Image
FROM nmdpbioinformatics/dpb1-prediction-base-image:0.0.4

LABEL maintainer="nmdp-bioinformatics"

# USER dpb1

COPY dpb1 /home/dpb1/dpb1
COPY server.py /home/dpb1/server.py
COPY config.py /home/dpb1/config.py
COPY wsgi.py /home/dpb1/wsgi.py

COPY --from=angular-builder ./ng-app/dist/dpb1-pred-ui-tool /usr/share/nginx/html
COPY webapp/nginx-conf/default.conf /etc/nginx/sites-enabled/default
COPY docker-entrypoint-tce-app.sh /usr/local/bin/

# Deployed Environment. Used in config.py
ENV FLASK_ENV development
# Webserver worker processes: A positive integer generally in the 2-4 x $(NUM_CORES) range.
# Each process will take the same amount of memory
ENV WORKERS 1
# 1 sets the buffered to go to stdout
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint-tce-app.sh" ]
