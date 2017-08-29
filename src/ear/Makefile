ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	$(ROOT_DIR)/ear.py --publish_to=ipc:///var/run/ear.socket --control_by=ipc:///var/run/ear_ctrl.socket

ear_capture:
	sudo python3 -c "import zmq; sock = zmq.Context().socket(zmq.PUSH); sock.connect('ipc:///var/run/ear_ctrl.socket'); sock.send_json({'action':'capture', 'duration':3})"

install:
	ln -s $(ROOT_DIR)/etc/systemd/system/ear.service /etc/systemd/system/ear.service
	ln -s $(ROOT_DIR)/ear.py /usr/bin/ear.py
