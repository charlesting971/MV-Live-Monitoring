from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from threading import Timer
from scipy import integrate
from flask_socketio import SocketIO, send, emit, join_room
from dataCompile2 import dataCompile2

import json
import time
import numpy as np
import matplotlib.pyplot as plt
import plotly 
import scipy.io as spio


app = Flask(__name__)
app.config['SECRET_KEY'] = '9494668968ec5a5bacdd3bbf5f4fe9ca'
socketio = SocketIO(app)
DEVICES = {}
 
#*read data from text file
f=open("capture.txt","r")     
breathdata = f.read()
one=breathdata.split("BE")

#*read data from matlab file
data = spio.loadmat('Testing_data.mat')


i= 0
j= "Continue"
   
@app.route("/")
@app.route("/liveplot3")
def home():
    return render_template('liveplot3.html')


@socketio.on('requestFromClient')
def provideData():
    while j != "Stopped":
        global i 
        msgObj, duration = dataCompile2(i,data)
        i+=1  
        time.sleep(duration)
        emit('send2Client',msgObj )
        

@socketio.on('stoprequestFromClient')
def stopProvideData():
    global j 
    j="Stopped"
    
    
    





   





#@socketio.on('my event')
#def handle_my_custom_event(json):
#    print('received json: ' + str(json))
#    emit('my response',jsonfile)



if __name__=='__main__':
   socketio.run(app, debug=True)