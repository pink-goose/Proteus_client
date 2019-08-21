import logging

from services.recorder import Recorder
from services.audio_player import AudioPlayer
from services.requester import ProteusRequests
from configuration import ConfigurationManager
from services.hotword_detector.hotword_detector import HotwordDetector


logger = logging.getLogger(__name__)


def text_request(text):
    player = AudioPlayer()
    requester = ProteusRequests()

    try:
        answer_audio = requester.text_audio(text)
    except Exception:
        logger.error('Connection Error: server unreachable')
        return

    logger.info('Playing...')
    try:
        player.play(answer_audio)
    except Exception as e:
        logger.error(e)


def detected_callback():
    logger.info('Hotword detected')
    player = AudioPlayer()
    conf_manager = ConfigurationManager()
    config = conf_manager.instance()
    player.play(config['DETECT_SOUND'])
    recorder = Recorder()
    recorded_file = recorder.record()
    requester = ProteusRequests()
    try:
        answer_audio = requester.speech_audio(recorded_file)
    except Exception:
        logger.error('Connection Error: server unreachable')
        return
    logger.info('Playing...')
    player.play(answer_audio)


def run():
    logger.info('Starting listening')
    hw_detector = HotwordDetector(detected_callback)
    hw_detector.listen()


if __name__ == '__main__':
    run()
