#!/bin/sh

# bash scripts daje v chainike est :)

if ! command -v docker
then
  docker build --no-cache -t sitestatuschecker .
  docker run -it sitestatuschecker
  pause
  exit
fi

python3 app.py