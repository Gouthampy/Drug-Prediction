from flask import Flask,render_template,jsonify,request
import numpy as np
import pandas as pd
import sklearn
import json
import pickle as p
import requests


app=Flask(__name__)   # to define the app name 
@app.route('/')  # this is default route 
def index():
    return render_template("diabetesmainpage.html")
    # render_template  which is used to display the html 

@app.route("/diabetesprediction", methods=['POST'])
def predictdiabetes():
    print(model)
    data=request.get_json()
    prediction=np.array2string(model.predict(data))
    return jsonify(prediction)
@app.route('/diabetescondition',methods=['POST'])
def diabetescondition():
    url="http://localhost:5000/diabetesprediction"
    Pregnancies = request.form['Pregnancies']
    Glucose = request.form['Glucose']
    BP = request.form['BP']
    ST = request.form['ST']
    Insulin = request.form['Insulin']
    BMI = request.form['BMI']
    DPF = request.form['DPF']
    Age = request.form['Age']
    data=[[Pregnancies,Glucose,BP,ST,Insulin,BMI,DPF,Age]]
    j_data=json.dumps(data)
    headers={'content-type':'application/json','Accept-Charset':'UTF-8'}
    r=requests.post(url,data=j_data,headers=headers)
    r1=list(r.text)
    stat=""
    if r1[2]=='0':
        stat="patient is not affected with Diabetes" 
    else:
        stat="patient affected with Diabetes"
    return render_template("result.html",result=stat)

if __name__=='__main__':
    model_file='final_diabetes_model.pickle'
    model=p.load(open(model_file,'rb'))
    app.run()
