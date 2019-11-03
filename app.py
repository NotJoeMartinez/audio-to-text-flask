from flask import *  
from transcribe import scrib 
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  

    # execute transcribe function with argument of f

        return render_template("success.html", name = f.filename)  
  
if __name__ == '__main__':  
    app.run(debug = True)  