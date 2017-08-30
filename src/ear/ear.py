#!/usr/bin/env python3

import codecs
import numpy
import optparse
import pyaudio
import zmq

BITRATE = 16000

def wait_signal(stream):
    while True:
        raw_data = numpy.fromstring(stream.read(BITRATE // 4), dtype=numpy.int16)
        if len([vol for vol in raw_data if vol > 30000]) > 0:
            return

def capture_frame(stream, nsec):
    return stream.read(BITRATE * nsec)

def main(options, args):
    publish_to = options.ensure_value('publish_to', None)
    assert publish_to

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=BITRATE, input=True)

    context = zmq.Context()
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind(publish_to)
    while True:
        print('Waiting...', flush=True)
        wait_signal(stream)
        task = {'action' : 'capture', 'duration' : 3}
        print('Task: %s' % task, flush=True)
        if task['action'] == 'capture':
            frame = capture_frame(stream, task['duration'])
            pub_sock.send_json({'frame' : codecs.encode(frame, 'base64').decode('ascii')})

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--publish_to', dest='publish_to',
                      help='Publish audio fragments to the specified address')
    main(*parser.parse_args())
