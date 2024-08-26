from flask import *
from file_utils import FileUtils  # Import your existing classes/functions here
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from zip_utils import create_zip


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
upload_folder = os.path.join(base_dir,'assets','uploads')
output_folder = os.path.join(base_dir,'assets','outputs')
zip_folder = os.path.join(base_dir, 'assets','zips')

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['OUTPUT_FOLDER'] = output_folder
app.config['ZIP_FOLDER'] = zip_folder
app.secret_key = 'Drmhze6EPcv0fN_81Bj-nA'

def ensure_directories_exist():
    """Ensures that the necessary directories exist."""
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(zip_folder, exist_ok=True)


@app.route('/',methods=['POST','GET']) 
def index():
    if request.method == 'POST':
        if request.form.get("action") == "return_home":
            return render_template("form.html")
        if "studio_file" not in request.files:
            return redirect(url_for('redirect_message',message_type="notfound"))
        f = request.files['studio_file']
        if f.filename == '':
            return redirect(url_for('redirect_message',message_type="result"))

        uploaded_files_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(uploaded_files_path)

        file_processor = FileUtils(uploaded_files_path, output_folder)
        file_processor.run_studio_keys()

       # print(f"calling create zip with filename {f.filename}")
        zip_path = create_zip(output_folder,f.filename,app.config['ZIP_FOLDER'])
        zip_filename = os.path.basename(zip_path)
        download_link = url_for('download',filename=zip_filename)

        return render_template('form.html',download_link = download_link, download_filename=zip_filename)
    return render_template("form.html")


@app.route('/redirect/<message_type>')
def redirect_message(message_type):
    if message_type == "result":
        message = "You did not upload a file."
    elif message_type == "notfound":
        message = "Relevant file not found in uploads."
    else:
        message = "Uknown error."
    return render_template('redirect.html', message=message)
    #return render_template('acknowledgement.html')



@app.route('/download/<filename>')
def download(filename):
    #zip_path = os.path.join("/Users/avikumar/Desktop/studio keys/studio-keys/assets/zips",filename)
    zip_path = os.path.join(app.config['ZIP_FOLDER'], filename)
    print(f"zip path is {zip_path}")
    return send_file(zip_path,as_attachment=True)

if __name__ == '__main__':
    ensure_directories_exist()
    app.run(debug=True)


'''@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
        if "studio_file" not in request.files:
            return redirect(url_for('notfound'))
        f = request.files['studio_file']
        if f.filename == '':
            return redirect(url_for('result'))

        uploaded_files_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(uploaded_files_path)

        file_processor = FileUtils(uploaded_files_path, output_folder)
        file_processor.run_studio_keys()

       # print(f"calling create zip with filename {f.filename}")
        zip_path = create_zip(output_folder,f.filename,app.config['ZIP_FOLDER'])
        zip_filename = os.path.basename(zip_path)
        download_link = url_for('download',filename=zip_filename)

        return render_template('form.html',download_link = download_link, download_filename=zip_filename)

        #return redirect(url_for('download',filename=os.path.basename(zip_path)))
        #https://github.com/aviomg/studio-keys
        # <button class="bg-green-300 border-green-600 border-b p-4 m-4 rounded">Convert 2</button> '''



