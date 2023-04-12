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
