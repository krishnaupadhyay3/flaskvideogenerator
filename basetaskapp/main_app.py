from flask import Flask  , redirect , flash , request , url_for
import os
from rq import Queue
from rq.job import Job
from ffmp import RunFFmpeg
from worker import conn
import uuid
app = Flask(__name__)
q = Queue(connection=conn)

@app.route("/")
def index():
    return "hello world"

@app.route('/upload')
def file_upload():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action=/uploads>
      <input type=file name=file>

       <input type="text" name="time" id="url-box" placeholder="Enter time..." style="max-width: 300px;">

      <input type=submit value=Upload>
    </form>
    '''
url_path ="/home/krishna/startproject/onlinetasKqueue/basetaskapp/"
@app.route('/uploads',methods=["POST"])
def file_uploads():
    files = request.files['file']
    time_dur = request.form.get('time',10)
    
    if files.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if files :
        filename = files.filename
        src_path = os.path.join(url_path, filename)
        files.save(src_path)
        #return "success" #redirect(url_for('uploaded_file',
                 #               filename=filename))
        data_dict = {"src_path":src_path,"time_duration":time_dur}
        job = q.enqueue_call(func=RunFFmpeg, args=(data_dict,), )
        print(job.get_id())
        return  job.get_id()

app.run()