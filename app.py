from flask import Flask, request, render_template, send_file
from fpdf import FPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def add_image(self, image_path):
        self.add_page()
        self.image(image_path, x=10, y=10, w=190)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        pdf = PDF()
        pdf.add_image(image_path)
        pdf_path = image_path.replace(os.path.splitext(file.filename)[1], '.pdf')
        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True)
    return 'Invalid file format'

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
