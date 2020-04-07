#!/bin/bash
PROJ_DIR='/opt/swiper'

PID='cat $PROJ_DIR/logs/gunicorn.pid'
kill -HUP $PID