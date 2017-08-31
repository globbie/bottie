ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	$(ROOT_DIR)/ear.py --publish_to=ipc:///var/run/ear.socket

install:
	cp $(ROOT_DIR)/etc/systemd/system/ear.service /etc/systemd/system/ear.service
	cp $(ROOT_DIR)/ear.py /usr/bin/ear.py
