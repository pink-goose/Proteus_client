import json

import requests
from io import BytesIO


class ProteusRequests:
    def text_audio(self, sentence):
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        data = {"text": sentence}

        r = requests.post('http://0.0.0.0:5000/dialogue/text', data=json.dumps(data), headers=headers)

        audio_buf = BytesIO(r.content)
        r.close()

        return audio_buf

    def speech_audio(self, audio_file):
        # This sets reference point to the beginning of the file
        audio_file.seek(0)

        r = requests.post('http://0.0.0.0:5000/dialogue/speech', files={'file': audio_file.read()})

        audio_buf = BytesIO(r.content)
        r.close()

        return audio_buf
