# write a function that adds an mp3 file to the storage gpc storage bucket and returns it's uri 

from google.cloud import storage   
from blobs import *
from transcribe import *
import config as cf 

bucketname = cf.bucketname
audio_file_name = 'audio/bled.mp3'

upload_blob( bucketname, audio_file_name , 'bled.mp3')

gcs_uri = 'gs://' + bucketname + '/' + 'bled.mp3'

sample_long_running_recognize(gcs_uri)
## TO DO: delete the blob after upload.