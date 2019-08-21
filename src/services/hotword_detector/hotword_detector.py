from .snowboy.snowboy import SnowboyDetector
from configuration import ConfigurationManager


class HotwordDetector:
    def __init__(self, detected_callback):
        self.detected_callback = detected_callback

    def listen(self):
        conf_manager = ConfigurationManager()
        config = conf_manager.instance()

        detector = hotword_detectors[config['HOTWORD_ENGINE']](self.detected_callback)
        detector.listen()


hotword_detectors = {
    'snowboy': SnowboyDetector
    # 'precise': PreciseDetector,
    # 'sphinx': SphinxDetector
}
