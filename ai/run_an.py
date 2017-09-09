# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 20:30:58 2016

@author: john
"""
import os
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
import cv2, numpy as np

from PIL import Image

from flask import Flask,request,render_template,url_for
from flask_cors import CORS, cross_origin
from scipy import misc
from sklearn.externals import joblib

from werkzeug import secure_filename


app = Flask(__name__)
CORS(app)

def VGG_16(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(3,224,224)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1000, activation='softmax'))

    if weights_path:
        model.load_weights(weights_path)

    return model

def predict(image_url):
    im = load_image(image_url)
    model = VGG_16('vgg16_weights.h5')
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy')

    f = open('synset_words.txt','r')
    lines = f.readlines()
    f.close()
	
    out = model.predict(im)
    i1 = np.argsort(-out[0])[0]
    i2 = np.argsort(-out[0])[1]
    i3 = np.argsort(-out[0])[2]
    i11 = str((out[0])[i1])
    i22 = str((out[0])[i2])
    i33 = str((out[0])[i3])
    predict_name1 = lines[i1]
    predict_name2 = lines[i2]
    predict_name3 = lines[i3]
    var_list = [predict_name1,i11,predict_name2,i22,predict_name3,i33]
    a = '|'
    return a.join(var_list)
	

def load_image(imageurl):
    im = cv2.resize(cv2.imread(imageurl),(224,224)).astype(np.float32)
    im[:,:,0] -= 103.939
    im[:,:,1] -= 116.779
    im[:,:,2] -= 123.68
    im = im.transpose((2,0,1))
    im = np.expand_dims(im,axis=0)
    return im


@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	filename = secure_filename(file.filename)
	image_url = os.path.join('static/images', filename)
	file.save(image_url)
	predict_name = predict(image_url)
	#IMAGE_X1 = int(float(request.form['x']))
	#IMAGE_Y1 = int(float(request.form['y']))
	#IMAGE_X2 = int(float(request.form['w'])+float(request.form['x']))
	#IMAGE_Y2 = int(float(request.form['h'])+float(request.form['y']))
	
	#IMAGE_BAKUP = os.path.join('cache', filename)
	#im = Image.open(image_url)
	#box = (IMAGE_X1,IMAGE_Y1,IMAGE_X2,IMAGE_Y2)
	#region = im.crop(box)
	
	#region.save(IMAGE_BAKUP)
	#predict_name = predict(IMAGE_BAKUP)
	#print predict_name
	return predict_name
	

@app.route('/')
def index():
    return render_template('index.html')
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
