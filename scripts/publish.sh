#!bin/bash/

rsync -crvP --exclude={logs, venv} --delete ./ root@193.112.128.44:/opt/swiper/