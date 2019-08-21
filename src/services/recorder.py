import os
import math
import time
import wave
import struct

import logging
import pyaudio
from io import BytesIO


Threshold = 20

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 1

root_dir = os.path.dirname(os.path.abspath(__file__))
f_name_directory = os.path.join(root_dir, '/resources/')

logger = logging.getLogger(__name__)


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        logger.info('Recording beginning...')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        return self.write_to_buf(b''.join(rec))

    def write_to_buf(self, recording):
        audio_buf = BytesIO()

        wf = wave.open(audio_buf, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        logger.info('Returning to listening')
        return audio_buf

    def write_to_file(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        logger.info('Written to file: {}'.format(filename))
        logger.info('Returning to listening')

    def listen(self):
        logger.info('Listening beginning')
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()
