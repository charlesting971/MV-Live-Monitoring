from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from threading import Timer
from scipy import integrate
from flask_socketio import SocketIO, send, emit, join_room
from dataCompile import dataCompile

import json
import time
import numpy as np
import matplotlib.pyplot as plt 
import plotly


app = Flask(__name__)
app.config['SECRET_KEY'] = '9494668968ec5a5bacdd3bbf5f4fe9ca'
socketio = SocketIO(app)
DEVICES = {}
 
#*read data from text file
f=open("capture.txt","r")     
breathdata = f.read()
one=breathdata.split("BE")
i= 0
j= "Continue"
   
@app.route("/")
@app.route("/liveplot")
def home():
    return render_template('liveplot.html')


@socketio.on('requestFromClient')
def provideData():
    if j != "Stopped":
        global i 
        msgObj = dataCompile(i,one)
        i+=1  
        time.sleep(3)
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