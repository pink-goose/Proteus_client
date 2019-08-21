import logging
from . import snowboydecoder


logger = logging.getLogger(__name__)


class SnowboyDetector:
    def __init__(self, detected_callback):
        self.detected_callback = detected_callback
        # pass

    def listen(self):
        detector = snowboydecoder.HotwordDetector(
            "/home/mikhail/PycharmProjects/Proteus_client/src/resources/snowboy.pmdl", sensitivity=0.5, audio_gain=1)
        # detector.start(self.detected_callback)
        detector.start(self.detected_callback)

    def detected_callback(self):
        # print("hotword detected")
        logger.info('Hotword detected')
        return True
