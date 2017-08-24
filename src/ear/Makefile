run:
	./ear.py --publish_to=ipc:///var/run/ear.socket --control_by=ipc:///var/run/ear_ctrl.socket

ear_capture:
	sudo python3 -c "import zmq; sock = zmq.Context().socket(zmq.PUSH); sock.connect('ipc:///var/run/ear_ctrl.socket'); sock.send_json({'action':'capture', 'duration':3})"
