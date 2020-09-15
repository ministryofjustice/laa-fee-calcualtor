FROM buildpack-deps:xenial

ENV \
  LANG=en_GB.UTF-8 \
  TZ=Europe/London

ARG DJANGO_SECRET_KEY
ARG VERSION_NUMBER
ARG COMMIT_ID
ARG BUILD_DATE
ARG BUILD_TAG

# pre-create directories
WORKDIR /app

# add non-root user and group with xenial first available uid, 1000, see /etc/login.defs, UID_MIN
RUN addgroup --gid 1000 --system appgroup \
&& adduser --uid 1000 --system appuser --ingroup appgroup

# setup environment
RUN \
  set -ex \
  && apt-get update \
  && apt-get install \
    -y \
    --no-install-recommends \
    locales \
    tzdata \
    software-properties-common \
    build-essential \
    rsync \
    gettext \
    python3-all-dev \
    python3-pip \
    libpq-dev \
    netcat \
  && echo en_GB.UTF-8 UTF-8 > /etc/locale.gen \
  && locale-gen \
  && timedatectl set-timezone Europe/London || true \
  && pip3 install -U setuptools pip wheel

# cache python packages, unless requirements change
ADD ./requirements requirements
RUN pip3 install -r requirements/base.txt

# add app
ADD . /app

# run uwsgi on 8080
EXPOSE 8080
ENV DJANGO_SETTINGS_MODULE=fee_calculator.settings.docker

ENV APPVERSION=${VERSION_NUMBER}
ENV APP_GIT_COMMIT=${COMMIT_ID}
ENV APP_BUILD_DATE=${BUILD_DATE}
ENV APP_BUILD_TAG=${BUILD_TAG}
ENV APP_BUILD_BRANCH=${BUILD_BRANCH}

# temporary "escape hatch" for setuputools > 50.0
# https://github.com/pypa/setuptools/issues/2352
ENV SETUPTOOLS_USE_DISTUTILS=stdlib

# clearing data to prevent UNIQUE constraint violations when rebuilding locally, at least
RUN python3 manage.py migrate --no-input \
    && python3 manage.py cleardata \
    && python3 manage.py loadalldata \
    && python3 manage.py collectstatic --no-input

USER 1000
CMD uwsgi --ini uwsgi.ini
