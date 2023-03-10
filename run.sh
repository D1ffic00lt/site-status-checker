#!/bin/sh
#!/bin/bash

#docker network connect --ip 172.20.128.2 multi-host-network container2
docker build -t foo .
docker run -it foo
pause