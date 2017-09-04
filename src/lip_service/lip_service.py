#!/usr/bin/env python2

import festival
import optparse
import time
import sys
import zmq

def main(options, args):
    address = options.ensure_value('address', None)
    status_to = options.ensure_value('status_to', None)
    assert address and status_to

    context = zmq.Context()
    sock = context.socket(zmq.PAIR)
    sock.bind(address)
    status_sock = context.socket(zmq.PUSH)
    status_sock.connect(status_to)
    while True:
        print 'Waiting...'; sys.stdout.flush()
        task = sock.recv_json()
        print 'Task: %s' % task; sys.stdout.flush()
        if task['action'] == 'say':
            status_sock.send_json({'sender' : 'lip_service', 'status' : 'speaking'})
            festival.sayText(task['text'])
            time.sleep(0.125)
            status_sock.send_json({'sender' : 'lip_service', 'status' : 'waiting'})

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--address', dest='address',
                      help='Bind to this address')
    parser.add_option('--status_to', dest='status_to',
                      help='Send status update to the specified address')
    main(*parser.parse_args())
