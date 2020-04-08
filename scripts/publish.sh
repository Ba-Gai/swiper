#!bin/bash/
HOST='193.112.128.44'
USER='gai'
REMOTE_DIR='/opt/swiper/'
LOCAL_DIR='./'

rsync -crvP --exclude={logs, venv} --delete $LOCAL_DIR $USER@HOST:$REMOTE_DIR


# 重启远程服务器
ssh @$USER@HOST "$REMOTE_DIR/scripts/restart.sh"