ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	./bottie.py --address=ipc:///var/run/bottie.socket --device=kettle,ipc:///var/run/kettle.socket --device=light,ipc:///var/run/light.socket --device=lip_service,ipc:///var/run/lip_service.socket

install:
	ln -sf $(ROOT_DIR)/etc/systemd/system/bottie.service /etc/systemd/system/bottie.service
	ln -sf $(ROOT_DIR)/bottie.py /usr/bin/bottie.py
