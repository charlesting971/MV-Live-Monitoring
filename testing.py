from scipy import integrate
from scipy.optimize import curve_fit


import numpy as np
import matplotlib.pyplot as plt 
import scipy.io as spio

data = spio.loadmat('Testing_Data.mat')

#print(np.size(data['BreathData'][0]))
#print(np.size(data['BreathData'][0][0]))
#print((data['BreathData'][0][0][0]))
#print(np.size(data['BreathData'][0][0][0]))
#print(list(data.keys()))




 #   data = spio.loadmat(breathData)

P = []
Q = []

for i in range(len(data['BreathData'][0][0][0])):
    P.append(data['BreathData'][0][0][0][i][0])
    Q.append(data['BreathData'][0][0][1][i][0])

P = np.array(P)
Q = np.array(Q)

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


# Simulated Pressure Psim
Psim = Ers*V + Rrs*Q + PEEP


print(Ers)
print(Rrs)

plt.figure()
plt.plot(Time,P,label = "P")
plt.plot(Time,Psim,label = "Psim")
plt.xlabel('Time')
plt.ylabel('Pressure')
plt.title('Graph of P and Psim against Time')
plt.legend() 
plt.show()
