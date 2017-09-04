#!/usr/bin/env python3

import codecs
import numpy
import optparse
import pyaudio
import threading
import zmq

BITRATE = 16000

def wait_signal(stream):
    while True:
        raw_data = numpy.fromstring(stream.read(BITRATE // 8, exception_on_overflow=False), dtype=numpy.int16)
        vols = [vol for vol in raw_data if vol > 32500]
        #print(len(vols), flush=True)
        if len(vols) > 0:
            return

def capture_frame(stream, nsec):
    return stream.read(BITRATE * nsec, exception_on_overflow=False)

def do_listen(stream, pub_sock, atomic_is_active):
    duration = 3  # Seconds
    while True:
        print('(Listen Thread) Waiting signal...', flush=True)
        wait_signal(stream)
        is_active = atomic_is_active[0]
        if not is_active:
            print('(Listen Thread) Ignore, repeat again', flush=True)
            continue
        print('(Listen Thread) Recording %s seconds...' % duration, flush=True)
        frame = capture_frame(stream, duration)
        pub_sock.send_json({'frame' : codecs.encode(frame, 'base64').decode('ascii')})

def main(options, args):
    publish_to = options.ensure_value('publish_to', None)
    control_by = options.ensure_value('control_by', None)
    assert publish_to and control_by

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=BITRATE, input=True)

    context = zmq.Context()
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind(publish_to)
    ctrl_sock = context.socket(zmq.PULL)
    ctrl_sock.bind(control_by)

    is_active = [True]
    listen_thread = threading.Thread(target=do_listen, args=(stream, pub_sock, is_active))
    listen_thread.start()

    while True:
        print('(Main Thread) Waiting...', flush=True)
        task = ctrl_sock.recv_json()
        print('(Main Thread) Task: %s' % task, flush=True)
        if task['sender'] == 'lip_service' and task['status'] == 'speaking':
            is_active[0] = False
        elif task['sender'] == 'lip_service' and task['status'] == 'waiting':
            is_active[0] = True

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--publish_to', dest='publish_to',
                      help='Publish audio fragments to the specified address')
    parser.add_option('--control_by', dest='control_by',
                      help='Control the ear through this address')
    main(*parser.parse_args())
