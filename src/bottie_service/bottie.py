#!/usr/bin/env python3

import optparse
import zmq

def main(options, args):
    address = options.ensure_value('address', None)
    devices = options.ensure_value('devices', None)
    assert address and devices

    context = zmq.Context()
    sock = context.socket(zmq.PULL)
    sock.bind(address)
    for device_id, device_data in devices.items():
        device_sock = context.socket(zmq.REQ)
        device_sock.connect(device_data['address'])
        device_data['socket'] = device_sock
    while True:
        task = sock.recv_json()
        print('Task: %s' % task, flush=True)
        text = task['input']
        if 'turn on' in text or 'turn off' in text:
            kettle = devices['kettle']
            action = 'start' if 'turn on' in text else 'stop'
            print('Sending "action:%s" to the kettle' % action, flush=True)
            kettle['socket'].send_json({'action' : action})
            reply = kettle['socket'].recv_json()
            print('Reply: %s' % reply, flush=True)

def parse_device(option, opt, value, parser):
    devices = parser.values.ensure_value(option.dest, {})
    device_id, device_address = value.split(',')
    devices[device_id] = {'address' : device_address}

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--address', dest='address',
                      help='Publish audio fragments to the specified address')
    parser.add_option('--device', action='callback', callback=parse_device,
                      metavar='<device_id>,<device_address>', type=str, nargs=1, dest='devices',
                      help='Register a device.  Option can be passed multiple times')
    main(*parser.parse_args())
