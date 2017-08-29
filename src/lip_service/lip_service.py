#!/usr/bin/env python2

import festival
import optparse
import sys
import zmq

def main(options, args):
    address = options.ensure_value('address', None)
    assert address

    context = zmq.Context()
    sock = context.socket(zmq.PAIR)
    sock.bind(address)
    while True:
        task = sock.recv_json()
        print 'Task: %s' % task; sys.stdout.flush()
        if task['action'] == 'say':
            festival.sayText(task['text'])

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--address', dest='address',
                      help='Bind to this address')
    main(*parser.parse_args())
