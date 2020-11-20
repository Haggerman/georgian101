import flask
from flask import flash, request, redirect
import numpy
import cv2

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

georgianApp = flask.Flask(__name__)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@georgianApp.route('/', methods=['GET','POST'])
def home():
    a = numpy.zeros(shape=(5, 2))
    return str(a[1][1])


if __name__ == "__main__":
    georgianApp.run()
        # if request.method == 'POST':
        #     # check if the post request has the file part
        #     if 'file' not in request.files:
        #         flash('No file part')
        #         return redirect(request.url)
        #     file = request.files['file']
        #     # if user does not select file, browser also
        #     # submit a empty part without filename
        #     if file.filename == '':
        #         flash('No selected file')
        #         return redirect(request.url)
        #     if file and allowed_file(file.filename):
        #         flash('Aaaa')
