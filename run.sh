#!/bin/sh

# bash scripts daje v chainike est :)

docker build --no-cache -t sitestatuschecker .
docker run -it sitestatuschecker
pause