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
from tensorflow.keras.models import load_model
model123 = load_model('model.h5')
from PIL import Image
def predictd(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)
        image = image.resize((256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)  # create a batch
        predictions = model123.predict(img_array)
        class_names = ['Apple___Apple_scab', 'Strawberry___Leaf_scorch', 'Tomato___Bacterial_spot']
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * (np.max(predictions[0])), 2)
        print(confidence, predicted_class)
        if(predicted_class=='Apple___Apple_scab'):
            var="Apple - Apple scab:Remove infected plant parts and destroy them.Rake up and destroy fallen leaves to reduce overwintering of the fungus.Apply fungicides to the plants."
        elif(predicted_class=='Strawberry___Leaf_scorch'):
            var="Strawberry - Leaf scorch:Remove infected plant parts and destroy them.Water the plants in the morning to give them time to dry during the day.Apply fungicides to the plants."
        # create a context dictionary to pass to the template
        else:
            var="Tomato - Bacterial spot:Remove infected plant parts and destroy them.Avoid working with plants when they are wet to prevent spreading the bacteria.Apply copper-based fungicides to the plants."
        context = {
            'image': image_file,
            'confidence': confidence,
            'predicted_class': predicted_class,
            "var":var
        }
        return render(request, 'agro/predictfff.html', context)

    return render(request, 'agro/predictfff.html')
def disease(request):
    return render(request,'agro/disease.html')