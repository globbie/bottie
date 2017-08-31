ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	./recognizer.py --subscribe_to=ipc:///var/run/ear.socket --push_to=ipc:///var/run/bottie.socket --model_dir=usr/share/recognizer/model

install:
	cp $(ROOT_DIR)/etc/systemd/system/recognizer.service /etc/systemd/system/recognizer.service
	cp $(ROOT_DIR)/recognizer.py /usr/bin/recognizer.py
	rm -rf /usr/share/recognizer
	cp -r $(ROOT_DIR)/usr/share/recognizer /usr/share/recognizer
