ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	./lip_service.py --address=ipc:///var/run/lip_service.socket --status_to=ipc:///var/run/ear_ctrl.socket

install:
	cp $(ROOT_DIR)/etc/systemd/system/lip_service.service /etc/systemd/system/lip_service.service
	cp $(ROOT_DIR)/lip_service.py /usr/bin/lip_service.py
