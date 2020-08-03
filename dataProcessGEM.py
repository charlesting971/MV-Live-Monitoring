from scipy import integrate
from scipy.optimize import curve_fit


import numpy as np
import matplotlib.pyplot as plt 
import scipy.io as spio


dataProcessGEM('Testing_Data.mat')



# Data Processing using Flow and Pressure
def dataProcessGEM(breathData):

    data = spio.loadmat(breathData)

    P = []
    Q = []
    for i in range(len(data['BreathData'][0][0][0])):
        P.append(data['BreathData'][0][0][0][i][0])
        Q.append(data['BreathData'][0][0][1][i][0])

    P = np.array(P)
    Q = np.array(Q)/60

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
    Psim = Ers*V + Rrs*Q + PEEP

    plt.figure()
    plt.plot(Time,P,label = "P")
    plt.plot(Time,Psim,label = "Psim")
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Graph of P and Psim against Time')
    plt.legend() 
    plt.show()

    # Comparing P and Psim and find region that doesn't match.
    j = 0
    timePsim_P = []
    
    for i in Psim:
        if i>P[j]:
            timePsim_P.append(1)
        else:
            timePsim_P.append(0)
    j = j+1

    timePsim_P1 = timePsim_P.insert(0,0)
    timePsim_P2 = timePsim_P.append(0)

    j = 0
    mismTime = []

    for i in timePsim_P:
        if timePsim_P1[j] != timePsim_P2[j]:
            mismTime = j
    j = j+1

    # Computing mismatch area
    area = np.full(np.size(mismTime),np.nan)
    AreaError = np.full(np.size(mismTime),np.nan)

    for a in range(0,np.size(mismTime)-1,2):
        if mismTime[a] == mismTime[a+1]:
            area[a] = 1
        else:
            area[a] = abs((np.trapz(Psim[mismTime[a]:mismTime[a+1]+1]))-(np.trapz(P[mismTime[a]:mismTime[a+1]+1])))
            AreaError[a] = abs(((np.trapz(Psim[mismTime[a]:mismTime[a+1]+1]))-(np.trapz(P[mismTime[a]:mismTime[a+1]+1])))*100/(np.trapz(P[mismTime[a]:mismTime[a+1]+1])))

    # Numbering every area and find index of maximum area
    j = 0
    for i in area:
        if i != np.nan:
            area[j]=i
            j = j+1

    maxA_i = area.index(max(area))

    t_i = range(len(P))

    if (maxA_i*2+1) <= (len(mismTime)-1):
        #P_peak_1 = max(P[0:mismTime[maxA_i*2-1]])
        #P_peak_t1 = P.index(max(P[0:mismTime[maxA_i*2-1]]))
        P_peak_t1 = np.where(P == np.amax(P[0:mismTime[maxA_i*2-1]]))[0]
        #P_peak_2 = max(P[mismTime[maxA_i*2]-1:mismTime[maxA_i*2+1]])
        #P_peak_t2 = P.index(max(P[mismTime[maxA_i*2]-1:mismTime[maxA_i*2+1]]))
        P_peak_t2 = np.where(P == np.amax(P[mismTime[maxA_i*2]-1:mismTime[maxA_i*2+1]]))[0]
   # else:
        #P_peak_1 = max(P[0:mismTime[maxA_i*2-1]])
        #P_peak_t1 = P.index(max(P[0:mismTime[maxA_i*2-1]]))
        #P_peak_2 = max(P[mismTime[maxA_i*2]-1:-1])
        #P_peak_t2 = P.index(max(P[mismTime[maxA_i*2]-1:-1]))





    # Compare with threshold
    if max(AreaError) >= 5:
        P_eff = np.array(P[P_peak_t1:P_peak_t2])
        P_eff_norm = (P_eff-min(P_eff)/(max(P_eff)-min(P_eff)))-1    
        t_eff = range(len(P_eff))

        # Non linear regression to compute u (location of centroids)
        def P_eff_func(x,u,A1,A2,A3):
            return A1*np.exp(-(x+u)**2)+A2*np.exp(-(x**2))+A3*np.exp(-(x-u)**2)

        ini_guess = [0]*4
        c,cov = curve_fit(P_eff_func,P_eff_norm,P_eff_norm,ini_guess)

        # 
        phi_1 = [0]*len(P)
        phi_2 = [0]*len(P)
        phi_3 = [0]*len(P)

        phi_1[P_peak_t1:P_peak_t2] = np.exp(-((P_eff_norm+c[0])**2))
        phi_2[P_peak_t1:P_peak_t2] = np.exp(-((P_eff_norm)**2))        
        phi_3[P_peak_t1:P_peak_t2] = np.exp(-((P_eff_norm-c[0])**2))

        def P_fitted_func(x,A1,A2,A3,Ers,Rrs):
            return Ers*V+Rrs*Q+A1*np.exp(-(x+u)**2)+A2*np.exp(-(x**2))+A3*np.exp(-(x-u)**2)

#return Ers, Rrs, PEEP, PIP, Vtidal, V