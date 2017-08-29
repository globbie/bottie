ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	./recognizer.py --subscribe_to=ipc:///var/run/ear.socket --push_to=ipc:///var/run/bottie.socket --model_dir=usr/share/recognizer/model

install:
	ln -s $(ROOT_DIR)/etc/systemd/system/recognizer.service /etc/systemd/system/recognizer.service
	ln -s $(ROOT_DIR)/recognizer.py /usr/bin/recognizer.py
