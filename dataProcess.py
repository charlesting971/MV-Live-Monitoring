from scipy import integrate

import numpy as np
import matplotlib.pyplot as plt 

# Data Processing using Flow and Pressure
def dataProcess(breathData):
    P = np.array(breathData[2::2])
    Q = (np.array(breathData[1::2]))/60   
    b_points = np.size(Q)
    # Consider instance where P size and Q size **
    Time = list(np.linspace(0,(b_points-1)*0.02,b_points))

   # PEEP = np.array(round(np.min(P))*b_points)
    PEEP = min(P)
    PIP = max(P)
    V = integrate.cumtrapz(Q, x=Time, initial=0)
    Vtidal = max(V)
    # Seperate inspiration/expiration

    # Constructing Ax=B to obtain Ers and R
    A = np.vstack((V,Q)).T #Transpose 
    B = P-PEEP
    Ers, Rrs = np.linalg.lstsq(A, B)[0]
    # positive lstsq**

    # Time varying elastance Edrs
    #Edrs = (Pressure-(Rrs*Q)-PEEP)/Volume

    # Simulated Pressure Psim
    #Psim = Ers*V + Rrs*Q + PEEP

    #plt.figure()
    #plt.plot(Time,P,label = "P")
    #plt.plot(Time,Psim,label = "Psim")
    #plt.xlabel('Time')
    #plt.ylabel('Pressure')
    #plt.title('Graph of P and Psim against Time')
    #plt.legend() 
    #plt.show()
    
    return Ers, Rrs, PEEP, PIP, Vtidal, V