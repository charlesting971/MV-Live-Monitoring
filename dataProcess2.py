from scipy import integrate

import numpy as np
import matplotlib.pyplot as plt 

# Data Processing using Flow and Pressure
def dataProcess2(data,bNum):

    P = []
    Q = []

    for i in range(len(data['BreathData'][0][bNum][0])):
        P.append(data['BreathData'][0][bNum][0][i][0])
        Q.append(data['BreathData'][0][bNum][1][i][0])

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
    
    return P, Q, Ers, Rrs, PEEP, PIP, Vtidal, V