'''
python=3.7.17
flask=2.1.3
werkzeug=2.0.3
tensorflow=2.9.1
numpy=1.21.5
pillow=9.2.0
gunicorn=20.1.0
'''
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os 
from tensorflow.keras.utils import load_img, img_to_array
#from tensorflow.python.keras.models import load_model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np

#import keras.backend.tensorflow_backend as tb
#tb._SYMBOLIC_SCOPE.value = True

app = Flask(__name__)

#classifier = load_model('D:/FLASK/CNN_CAT_DOG/my_cnn_model5.h5')
classifier = ResNet50(weights='imagenet')
#app.config['UPLOAD_FOLDER'] = 'D:/FLASK/CNN_JANA/static/'
app.config['UPLOAD_FOLDER'] = './static/'

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/upload', methods=['POST'])
def upload():
	f = request.files['file']
	extention = os.path.splitext(f.filename)[1]
	janafile = 'myfile' + extention
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(janafile))
	f.save(full_filename)
	ff = secure_filename(janafile)
		
	return render_template('uploaded.html', user_image = ff)

@app.route('/predict',methods=['POST'])
def predict():
	janafile = request.form['myfile']
	ff = secure_filename(janafile)
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'],ff)
	
	
	myimage    = load_img(full_filename, target_size=(224, 224))
	test_image = img_to_array(myimage)
	
	test_image = np.expand_dims(test_image, axis = 0)
	test_image = preprocess_input(test_image)
	preds      = classifier.predict(test_image,verbose=0)
	result     = decode_predictions(preds, top=1)[0]
		
	return render_template('predicted.html', prediction_text='Prediction: '+result[0][1], prediction_percent='Probability: '+str(round(result[0][2]*100,2))+'%', user_image = ff)

@app.route('/ok', methods = ['GET', 'POST'])
def okk():
	return render_template('index.html')
	
@app.route('/gohome')
def gohome():
	return redirect('https://scholarlabfoundation.tech/')

if __name__ == "__main__":
	app.run(debug=False,threaded=False)
    #app.run(debug=True)