from flask import Flask, request, render_template
import pprint
# for uploading audio to blob
from google.cloud import storage   
from blobs import *
from transcribe import *
import config as cf 

# from transcribe import scrib 
app = Flask(__name__)  

@app.route('/')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['GET','POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save('uploads/' + f.filename)  

        # upload the the audio to google cloud and return the uri 
        upload_blob(cf.bucketname, 'uploads/'+f.filename , f.filename)

        # Build uri suing the filename suplied by user 
        gcs_uri = 'gs://' + cf.bucketname + '/' + f.filename

        # execute transcribe function on the gcs_uri
        sample_long_running_recognize(gcs_uri, f.filename)
        
        return render_template("success.html", name = f.filename)  
  
if __name__ == '__main__':  
    app.run(debug = True)  