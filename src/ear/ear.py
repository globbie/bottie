#!/usr/bin/env python3

import codecs
import optparse
import subprocess
import zmq

import pyaudio
import numpy as np

CHUNKSIZE = 1024

def wait_signal(audio):
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNKSIZE)
    while True:
        str_data = stream.read(CHUNKSIZE)
        raw_data = numpy.fromstring(str_data, dtype=numpy.int16)
        for i in raw_data:
            if i > 30000:
                return
    stream.close()

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
    assert publish_to

    audio = pyaudio.PyAudio()

    context = zmq.Context()
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind(publish_to)
    while True:
        print('Waiting...', flush=True)
        wait_signal(audio)
        task = {'action' : 'capture', 'duration' : 3}
        print('Task: %s' % task, flush=True)
        if task['action'] == 'capture':
            frame = capture_frame(task['duration'])
            pub_sock.send_json({'frame' : codecs.encode(frame, 'base64').decode('ascii')})

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--publish_to', dest='publish_to',
                      help='Publish audio fragments to the specified address')
    main(*parser.parse_args())
