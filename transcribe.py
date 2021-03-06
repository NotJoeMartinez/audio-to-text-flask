from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import time
import os

moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())

def sample_long_running_recognize(storage_uri, filename):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    full_transcript = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        full_transcript.append(alternative.transcript)
        # print(u"Transcript: {}".format(alternative.transcript))
        print(alternative.transcript)
        print(type(alternative.transcript))

    with open (f'transcripts/{filename}'+'.txt', 'w') as f:
      for x in full_transcript:
        f.write(x+'\n')
    # return the array of full transcript        
    return full_transcript


