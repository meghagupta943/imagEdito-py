from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2


UPLOAD_FOLDER = '.venv\\static'                              #uploaded image
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#allowed_file simply checks if a particular file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img= cv2.imread(f".venv\\static\\{filename}")           #reading image from uploads folder 
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename=f".venv\\processed\\{filename}"
            cv2.imwrite(newfilename, imgProcessed)
            return newfilename
        case "cgreen":
            imgProcessed=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            newfilename=f".venv\\processed\\{filename}"
            cv2.imwrite(newfilename, imgProcessed)
            return newfilename
        case "cwebp":
            newfilename = f".venv\\processed\\{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cjpg":
            newfilename=f".venv\\processed\\{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cpng":
            newfilename=f".venv\\processed\\{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename
    pass

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/howtu')
def howtu():
    return render_template("howtu.html")

@app.route('/contactus')
def contactus():
    return render_template("contactus.html")


@app.route("/edit", methods=["GET","POST"])                            #18.00 minutes
def edit():
    if request.method=="POST":  
        operation= request.form.get("operation")                  
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error file not selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename, operation)
            flash(f"Your image has been processed")
            return render_template("index.html")
        
    return render_template("index.html")

app.run(debug= True, port=5001)


#newfilename = f"processed/{filename.split('.')[0]}_{operation}.webp" .venv\\processed\\{filename.split('.')[0]}.webp
#.venv\processed\exampleimage.jpg