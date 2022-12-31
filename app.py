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
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

classifier = load_model('tl_covid_model_93.h5')
class_names = np.array(['COVID', 'NORMAL', 'PNEUMONIA'])
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
	
	myimage    = load_img(full_filename, target_size=(160, 160))
	test_image = img_to_array(myimage)
	test_image = np.expand_dims(test_image, axis = 0)
	result     = classifier.predict(test_image,verbose=0)
	
	predicted_id = tf.math.argmax(result, axis=-1)
	predicted_class_label = class_names[predicted_id]
	
	pr_result = tf.math.softmax(result[0])
	prediction = predicted_class_label
	prediction_proba = pr_result[predicted_id[0]].numpy()
	
	return render_template('predicted.html', prediction_text='Prediction: '+prediction, prediction_percent='Probability: '+str(round(prediction_proba*100,2))+'%', user_image = ff)

	
@app.route('/ok', methods = ['GET', 'POST'])
def okk():
	return render_template('index.html')
	
@app.route('/gohome')
def gohome():
	return redirect('https://scholarlabfoundation.tech/')

if __name__ == "__main__":
	#app.run(debug=False,threaded=False)
    app.run(debug=True)