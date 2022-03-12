
FROM python:3.10-alpine3.14 as minimal-base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

RUN set -xe; \
    apk add --update --no-cache  tzdata gcc build-base bash\
     # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime

RUN echo "Europe/Paris" >  /etc/timezone

FROM minimal-base AS base

# Install pipenv and compilation dependencies
RUN  pip install --upgrade pip ; \
     pip install pipenv --no-cache-dir


ENV SHELL="/bin/bash"
RUN mkdir /photowall
WORKDIR /photowall
COPY . .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

EXPOSE 5000
CMD ["pipenv", "run","python", "app.py"]
