import contextlib

from pydub import AudioSegment
from pydub.playback import play
with contextlib.redirect_stdout(None):
    from pygame import mixer


class AudioPlayer:
    def __init__(self):
        pass

    def play(self, audio_buf):
        mixer.init()
        mixer.music.load(audio_buf)
        mixer.music.play()

    def pydub_play(self, audio_buf):
        audiofile = AudioSegment.from_file(audio_buf, format="wav")
        play(audiofile)

    def stop(self):
        pass

    def quieter(self):
        pass
