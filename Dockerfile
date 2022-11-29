
# improve build time by pulling images from gitlab and not dockerhub

#React production files builder
FROM node:14 AS front-builder

ARG PROJECT_DIR=/app/
ARG ASSETS_DIR=/app/web/

ENV BUILD_TARGET_FOLDER=/app/api

WORKDIR $ASSETS_DIR

COPY ./web/package.json ./web/package-lock.json ./
RUN npm install --omit=optional --no-audit

COPY ./web ./

RUN mkdir -p $BUILD_TARGET_FOLDER
COPY ./scripts/post_npm_build.sh ../scripts/post_npm_build.sh

RUN rm -f .env*.local && npm run build

#------------------------------------------------------------------
FROM python:3.9-slim as back-builder

ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/app/api/.venv/bin:$PATH"

WORKDIR /app/api
RUN pip install -U pip pipenv
COPY ./api/Pipfile ./api/Pipfile.lock ./
RUN pipenv install

#------------------------------------------------------------------
FROM python:3.9-slim

ARG HTTPS_PROXY=
ARG HTTP_PROXY=
ARG FTP_PROXY=
ARG NO_PROXY="localhost,127.0.0.1"
ARG VERSION_TAG="?"

ENV https_proxy=$HTTPS_PROXY
ENV http_proxy=$HTTP_PROXY
ENV ftp_proxy=$FTP_PROXY
ENV no_proxy=$NO_PROXY

ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/app/api/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/api

# copy scripts
COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/*.sh

# Copy the current directory contents into the container
COPY ./api /app/api
RUN chmod 0744 /app/api/manage.py

# Copy built react files from builder into this container
COPY --from=front-builder /app/api/static_web /app/api/static_web
COPY --from=front-builder /app/api/templates_web /app/api/templates_web

# Copy Python dependencies from back-builder into this container
COPY --from=back-builder /app/api/.venv /app/api/.venv

# write version number in backend filetree to make it visible to django
RUN echo "__version__ = '${VERSION_TAG}'" >> /app/api/app/version.py


RUN python manage.py collectstatic --noinput

#RUN apt-get update && apt-get -y install locales rsync curl && apt-get clean autoclean && apt-get autoremove --yes --purge && rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN apt-get update && apt-get upgrade && apt-get clean autoclean && apt-get autoremove --yes --purge && rm -rf /var/lib/{apt,dpkg,cache,log}/
# set locales. fr_FR and en_US must be available for sia urls to be computed correctly
# RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
  sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
  locale-gen
ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8

# Make port 8000 available for the app
EXPOSE 8000

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
CMD python3 manage.py runserver 0.0.0.0:8000


