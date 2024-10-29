from flask import *
from file_utils import FileUtils  # Import your existing classes/functions here
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from zip_utils import create_zip
import shutil


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
    ensure_directories_exist() 
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
        zip_path = create_zip(output_folder,f.filename,app.config['ZIP_FOLDER'],file_processor.session_output_folder)
        zip_filename = os.path.basename(zip_path)
        download_link = url_for('download',filename=zip_filename)

        shutil.rmtree(file_processor.session_output_folder,ignore_errors=True)

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



#d5d887

'''
<html>
<head>
    <link href="{{ url_for('static', filename='output.css') }}" rel="stylesheet">

</head>
<body class="bg-[#dccfec]">
<br>
<h1 class="text-5xl text-center font-bold text-[#F49F0A] ">
    <span class="pagetext">Studio Keys</span></h1>
    <h1 class="text-3xl font-bold text-[#F08700] text-center">
        an InVision Prototype Restoration Tool
        </h1>
    <h1 class="text-xl text-blue-400 text-center">By: Avi Kumar | 
        <span class="text-blue-500">
            <a href="https://github.com/aviomg/studio-keys">Github Repo |</a>
        </span>
        <span class="text-blue-600">
            <a href="https://www.linkedin.com/in/avi-kumar-5041642b0/">My Linkedin</a>
        </span>
    </h1>
<h1 class="m-2 ml-10">
    <span class="text-3xl font-bold text-[#00A6A6]">1.</span>
    <span class="text-lg text-[#00A6A6]">Upload your Invision Files</span>
   </h1>
   <h1 class="ml-10 text-md text-green-600">You will find these in your file explorer as having a ".studio" extension.</h1>
<form method="post" enctype="multipart/form-data" action="/">
   <!-- <label for="studio_file">Upload your .studio file:</label> -->
    <input class="ml-10 my-2" type="file" name="studio_file" id="studio_file" accept=".studio">
  
    <h1 class="ml-10">
        <span class="text-3xl font-bold text-pink-400">2.</span>
        <span class="text-lg text-pink-400">Generate your restored mockups!</span>
        <h1 class="ml-10 text-md text-pink-600">You will receive a zip file containing an SVG for each artboard in the InVision Studio file.</h1>
       </h1>
       <h1>
        <button class="ml-10 bg-pink-500 text-pink-300 border-pink-600 border-b p-4 m-4 mr-0 rounded hover:text-white" type="submit">Generate SVGs</button>
        {% if download_link %}
        <span class="text-md font-bold text-purple-500">&#8594;</span>
        <span id="downloadLink" >
    <a href="{{download_link}}" class="bg-purple-500 hover:bg-purple-700 text-black font-bold py-2 px-4 rounded">
        Download {{download_filename}}
    </a>
</span>
{% endif %}
       </h1>
       
</form>
</body>
</html>'''