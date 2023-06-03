#!/bin/sh

# bash scripts daje v chainike est :)

if ! command -v docker
then
  docker build --no-cache -t sitestatuschecker . && docker run -it sitestatuschecker
  pause
  exit
fi

pip3 install -r requirements.txt
python3 app.py

# docker build -t sitestatuschecker .
# docker tag sitestatuschecker ghcr.io/d1ffic00lt/sitestatuschecker:v1.0.3
# docker push ghcr.io/d1ffic00lt/sitestatuschecker
