#!/usr/bin/env python3

import optparse
import sys
import zmq

def interpret(text):
    if text == 'cold' or text == 'hot' or text == 'lets' or text == 'make':
        return ('kettle', {'action' : 'stop' if text == 'cold' else 'start'})
    if text == 'dark' or text == 'light':
        return ('light', {'action' : 'stop' if text == 'dark' else 'start'})
    return ('lip_service', {'action' : 'say', 'text' : 'Sorry?'})

def response_to_user(text, lip_service = None, **unknown_devices):
    if lip_service:
        lip_service['socket'].send_json({'action' : 'say', 'text' : text})
    else:
        print('Response to user: %s' % text)

def main(options, args):
    address = options.ensure_value('address', None)
    devices = options.ensure_value('devices', None)
    assert address and devices

    context = zmq.Context()
    sock = context.socket(zmq.PULL)
    sock.bind(address)
    for device_id, device_data in devices.items():
        device_sock = context.socket(zmq.PAIR)
        device_sock.connect(device_data['address'])
        device_sock.RCVTIMEO = 3000  # receive timeout, ms
        device_data['socket'] = device_sock

    response_to_user('At your service!', **devices)
    while True:
        print('Waiting...', flush=True)
        task = sock.recv_json()
        print('Task: %s' % task, flush=True)
        text = task['input']
        device_id, command = interpret(text)
        device = devices[device_id]
        print('Sending %s to the %s' % (command, device_id), flush=True)
        device['socket'].send_json(command)
        try:
            reply = device['socket'].recv_json()
            print('Reply: %s' % reply, flush=True)
            if device_id == 'kettle' and reply['status'] == 'OK':
                response_to_user('The tea will be ready in 2 minutes', **devices)
        except:
            print("Unexpected error: %s" % sys.exc_info()[0])

def parse_device(option, opt, value, parser):
    devices = parser.values.ensure_value(option.dest, {})
    device_id, device_address = value.split(',')
    devices[device_id] = {'address' : device_address}

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--address', dest='address',
                      help='Bind to this address')
    parser.add_option('--device', action='callback', callback=parse_device,
                      metavar='<device_id>,<device_address>', type=str, nargs=1, dest='devices',
                      help='Register a device.  Option can be passed multiple times')
    main(*parser.parse_args())
