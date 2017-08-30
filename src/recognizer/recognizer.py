#!/usr/bin/env python2

import codecs
import os
import optparse
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import sys
import zmq

MODELDIR = "pocketsphinx/model"

def recognize(buf, decoder):
    decoder.start_utt()
    decoder.process_raw(buf, False, False)
    decoder.end_utt()
    return decoder.hyp().hypstr

def main(options, args):
    subscribe_to = options.ensure_value('subscribe_to', None)
    push_to = options.ensure_value('push_to', None)
    model_dir = options.ensure_value('model_dir', None)
    assert subscribe_to and push_to and model_dir

    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_float('-samprate', 44100.0)
    config.set_int('-nfft', 2048)
    config.set_string('-hmm', os.path.join(model_dir, 'en-us/en-us'))
    config.set_string('-lm', os.path.join(model_dir, 'en-us/en-us.lm.bin'))
    config.set_string('-dict', os.path.join(model_dir, 'en-us/cmudict-en-us.dict'))
    decoder = Decoder(config)

    context = zmq.Context()
    sub_sock = context.socket(zmq.SUB)
    sub_sock.connect(subscribe_to)
    sub_sock.setsockopt(zmq.SUBSCRIBE, '')
    ctrl_sock = context.socket(zmq.PUSH)
    ctrl_sock.connect(push_to)
    while True:
        print 'Waiting...'; sys.stdout.flush()
        data = sub_sock.recv_json()
        frame = codecs.decode(bytes(data['frame']), 'base64')
        print 'Frame length: %s' % len(frame); sys.stdout.flush()
        recognized = recognize(frame, decoder)
        ctrl_sock.send_json({'input' : recognized})
        print 'Sent: %s' % {'input' : recognized}

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--subscribe_to', dest='subscribe_to',
                      help='Listen audio frames from the ear')
    parser.add_option('--push_to', dest='push_to',
                      help='Send recognized commands to the controller')
    parser.add_option('--model_dir', dest='model_dir',
                      help='Path to pocketsphinx\'s model directory')
    main(*parser.parse_args())
