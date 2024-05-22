from flask import Flask, request, render_template, send_from_directory, Response
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploadFiles'  # 更改为你的文件存储目录
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    # 获取目录中的文件列表
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # 将文件列表传递给模板
    return render_template('upload.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    return index()


@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/display/<filename>')
def display_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'rb') as f:
            # 文件读取流
            file_content = f.read()
        if filename.endswith('.txt'):
            return Response(file_content, mimetype='text/plain')
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return Response(file_content, mimetype='image/jpeg')
        elif filename.lower().endswith('.pdf'):
            return Response(file_content, mimetype='application/pdf')
        else:
            return "File format not supported for preview."
    except IOError:
        return "File not found."



if __name__ == '__main__':
    app.run(debug=True)
