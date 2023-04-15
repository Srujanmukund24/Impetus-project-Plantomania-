from django.shortcuts import render
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.tree import DecisionTreeRegressor
import sys
import sqlite3

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

    return render(request,'agro/cropresult.html',{'ans':data[0],'ans1':data1[0],'ans2':data2[0]})
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
    return render(request, 'agro/fertresult.html',{'ans':data[0],'ans1':data1[0],'ans2':data2[0]})
