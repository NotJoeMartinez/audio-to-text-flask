

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud import storage
import config as cf
import time
import os

blob_list = []
url_list = []



def sample_long_running_recognize(storage_uri):

    client = speech_v1.SpeechClient()

    sample_rate_hertz = 16000

    language_code = "en-US"

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
    
    # this array store the text until we can write it to a text file
    full_transcript = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        full_transcript.append(alternative.transcript)
        print(u"Transcript: {}".format(alternative.transcript))

    # remove the everythign before the last forward slash. This is for file nameing 
    file_name = storage_uri.rsplit('/', 1)[-1]
    print(file_name)
    # Save the array of full transcrip to a text file 
    with open (f'transcripts/{file_name}'+'.txt', 'w') as f:
      for x in full_transcript:
        f.write(x+'\n')


# this lists all the names of the files I have stored in my gpc uri 
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()

    # no idea what this does but it's important 
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # appnds it to an array for latter use
    for blob in blobs:
        blob_list.append(blob.name)

# adds all the names of the intened bucket to an array 
list_blobs(cf.bucketname)

# the blob_list holds all the names of the files in the bucket this changes them into urls
for x in blob_list:
    gcs_uri = 'gs://' + cf.bucketname + '/' + x
    url_list.append(gcs_uri)

for url in url_list:
    sample_long_running_recognize(url)

# print(cf.bucketname)
# list_blobs(cf.bucketname)


# print(blob_list)