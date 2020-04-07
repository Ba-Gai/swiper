#!/bin/bash
PROJ_DIR='/opt/swiper'

workon swipe
gunicorn -c "$PROJ_DIR/swiper/gunicorn-config.py" swiper.wsgi
deactivate