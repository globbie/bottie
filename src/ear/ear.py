#!/usr/bin/env python3

import codecs
import optparse
import subprocess
import zmq

def capture_frame(nsec):
    arecord = subprocess.Popen(['arecord',
                                '--file-type', 'raw',
                                '--channels', '1',
                                '--format', 'S16_LE',
                                '--rate', '16000',
                                '--duration', str(nsec)],
                               stdout=subprocess.PIPE)
    return arecord.communicate()[0]

def main(options, args):
    publish_to = options.ensure_value('publish_to', None)
    control_by = options.ensure_value('control_by', None)
    assert publish_to and control_by

    context = zmq.Context()
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind(publish_to)
    ctrl_sock = context.socket(zmq.PULL)
    ctrl_sock.bind(control_by)
    while True:
        print('Waiting...', flush=True)
        task = ctrl_sock.recv_json()
        print('Task: %s' % task, flush=True)
        if task['action'] == 'capture':
            frame = capture_frame(task['duration'])
            pub_sock.send_json({'frame' : codecs.encode(frame, 'base64').decode('ascii')})

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--publish_to', dest='publish_to',
                      help='Publish audio fragments to the specified address')
    parser.add_option('--control_by', dest='control_by',
                      help='Control the ear through this address')
    main(*parser.parse_args())
