from django.shortcuts import render
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.tree import DecisionTreeRegressor
import sys
import sqlite3
from store.models import Product
import tensorflow as tf
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
import h5py as h5

# Create your views here.
def options(request):
    return render(request,'agro/options.html')
def cropresult(request):
    model = pickle.load(open('Crop_Prediction.pkl', 'rb'))
    lis=[]
    lis.append(request.GET['N'])
    lis.append(request.GET['P'])
    lis.append(request.GET['K'])
    lis.append(request.GET['temperature'])
    lis.append(request.GET['humidity'])
    lis.append(request.GET['ph'])
    lis.append(request.GET['rainfall'])

    testdata = [lis]
    prediction = model.predict(testdata)
    output = prediction[0]
    name = output
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM my_table WHERE name=?', (name,))
    rows = cursor.fetchall()
    conn.close()
    data = []
    data1=[]
    data2=[]
    for row in rows:
        data.append(row[0])
    for row in rows:
        data1.append(row[1])
    for row in rows:
        data2.append(row[2])
    print(output)
    products = Product.objects.filter(name=name)
    context={
        'ans': data[0], 'ans1': data1[0], 'ans2': data2[0], 'products': products
    }
    return render(request,'agro/cropresult.html',context)
def agrosection(request):
    return render(request,'agro/cropform.html')
def fertilizer(request):
    return render(request,'agro/fertform.html')
def fertresult(request):
    model1 = pickle.load(open('Fertilizer.pkl', 'rb'))
    lis = []
    lis.append(float(request.GET['temperature']))
    lis.append(float(request.GET['humidity']))
    lis.append(float(request.GET['moisture']))
    lis.append(float(request.GET['N']))
    lis.append(float(request.GET['P']))
    lis.append(float(request.GET['K']))
    s=request.GET['soil-type']
    c=request.GET['crop']
    print(lis)
    soil_type=[]
    crop_name=[]
    c_type=['barley',"cotton","groundnut","maize","millet","oilseeds","paddy","pulses","sugarcane","tobacco","wheat"]
    s_type=["black","clayey","loamy","red","sandy"]
    for i in range(5):
        if s==s_type[i]:
            soil_type.append(1)
        else:
            soil_type.append(0)
    for i in range(11):
        if c==c_type[i]:
            crop_name.append(1)
        else:
            crop_name.append(0)
    for i in range(5):
        lis.append(soil_type[i])
    print(lis)
    for j in range(11):
        lis.append(crop_name[j])
    testdata=[lis]
    print(testdata)
    prediction = model1.predict(testdata)
    output = prediction[0]
    name = output
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM my_table WHERE name=?', (name,))
    rows = cursor.fetchall()
    conn.close()
    data = []
    data1 = []
    data2 = []
    for row in rows:
        data.append(row[0])
    for row in rows:
        data1.append(row[1])
    for row in rows:
        data2.append(row[2])
    print(output)
    products = Product.objects.filter(name=name)
    context = {
        'ans': data[0], 'ans1': data1[0], 'ans2': data2[0], 'products': products
    }

    return render(request, 'agro/fertresult.html',context)


def predictd(request):
    data = 'plant_disease.ipynb'
    f = h5.File(data, 'r')
    model_path = 'plant_disease.ipynb'  # Path to your TensorFlow model
    model = tf.keras.models.load_model(model_path)

    if request.method == 'POST':
        image_file = request.FILES['image']
        image_bytes = image_file.read()
        image = tf.image.decode_jpeg(image_bytes, channels=3)
        image = tf.image.resize(image, [224, 224])
        image = tf.expand_dims(image, axis=0)
        image = image / 255.0

        prediction = model.predict(image)
        prediction = np.argmax(prediction)

        if prediction == 0:
            prediction_text = "Healthy Plant"
        else:
            prediction_text = "Diseased Plant"

        return HttpResponse(prediction_text)

    return render(request, 'predict.html')