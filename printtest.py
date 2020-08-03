from scipy import integrate
from scipy.optimize import curve_fit, nnls, lsq_linear



import numpy as np
import matplotlib.pyplot as plt 
import scipy.io as spio

# function to find the index where inspiration ends (for GEM)
def find_negative(lst):
    for index, item in enumerate(lst):
        if item < 0 and index >= 5:
            output = index
            break          
    return output

numB = 0
data = spio.loadmat('Testing_Data.mat')

P_insp = []
Q_insp = []
P = []
Q = []

for i in range(len(data['BreathData'][0][numB][0])):
    P.append(data['BreathData'][0][numB][0][i][0])
    Q.append(data['BreathData'][0][numB][1][i][0])

P = np.array(P)
Q = np.array(Q)/1

b_points = np.size(Q)
# Consider instance where P size and Q size **
Time = list(np.linspace(0,(b_points-1)*0.02,b_points))
zer0s1 = [0]*len(Time)

plt.figure()
plt.plot(Time,P,label = "P")
plt.plot(Time,Q,label = "Q")
plt.plot(Time,zer0s1)
plt.xlabel('Time')
plt.ylabel('Pressure and Flow rate')
plt.title('Graph of P and Flow rate against Time')
plt.legend() 
plt.show()






# PEEP = np.array(round(np.min(P))*b_points)
PEEP = P[-1]
PIP = max(P)
V = integrate.cumtrapz(Q, x=Time, initial=0)
Vtidal = max(V)
# Seperate inspiration/expiration

# Constructing Ax=B to obtain Ers and R
A = np.vstack((V,Q)).T #Transpose 
B = P-PEEP
#Ers, Rrs = nnls(A, B)[0]
res = lsq_linear(A, B, bounds=(0,40))
print(res['x'])
Ers = res['x'][0]
Rrs = res['x'][1]
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

#-----------------------------------GEM MODEL---------------------------------------------------
# Comparing P and Psim and find region that doesn't match.

insp_ind = find_negative(Q)+10

print('insp_ind:')
print(insp_ind)
P_insp= np.array(P[0:insp_ind])
Q_insp = np.array(Q[0:insp_ind])/1
V_insp = np.array(V[0:insp_ind])
Psim_insp= np.array(Psim[0:insp_ind])

b_points = np.size(Q_insp)
Time_insp = list(np.linspace(0,(b_points-1)*0.02,b_points))

j = 0
timePsim_P = []
    
for i in Psim_insp:
    if i>P_insp[j]:
        timePsim_P.append(1)
    else:
        timePsim_P.append(0)
    j = j+1
print(timePsim_P)
timePsim_P.insert(0,0)
timePsim_P.append(0)

timePsim_P1 = timePsim_P[0:-1]
timePsim_P2 = timePsim_P[1:]

j = 0
mismTime = []
#print('this is P1')
#print(timePsim_P1)
#print('this is P2')
#print(timePsim_P2)
for i in timePsim_P1:
    if timePsim_P1[j] != timePsim_P2[j]:
        mismTime.append(j)
    j = j+1

# Computing mismatch area
area = np.full(np.size(mismTime),np.nan)
AreaError = np.full(np.size(mismTime),np.nan)

for a in range(0,np.size(mismTime)-1,2):
    if mismTime[a] == mismTime[a+1]:
        area[a] = 1
    else:
        area[a] = abs((np.trapz(Psim_insp[mismTime[a]:mismTime[a+1]+1]))-(np.trapz(P_insp[mismTime[a]:mismTime[a+1]+1])))
        AreaError[a] = abs(((np.trapz(Psim_insp[mismTime[a]:mismTime[a+1]+1]))-(np.trapz(P_insp[mismTime[a]:mismTime[a+1]+1])))*100/(np.trapz(P_insp[mismTime[a]:mismTime[a+1]+1])))
print('mismTime:')
print(mismTime)
print('AreaError%^%')
print(AreaError)
# Numbering every area and find index of maximum area
area2 = []
for i in area:
    if i*0 == 0:
        area2.append(i)
        


print('area2')
print(area2)
maxA_i = np.where(area2 == max(area2))[0][0]

print('maxA_i:')
print(maxA_i)



print('GEM Model?:')

if max(AreaError) >= 25:
    #P_peak_1 = max(P[0:mismTime[maxA_i*2-1]])
    #P_peak_t1 = P.index(max(P[0:mismTime[maxA_i*2-1]]))
    P_peak_t1 = np.where(P_insp == np.amax(P_insp[0:mismTime[maxA_i*2]]))[0][0]
    #P_peak_2 = max(P[mismTime[maxA_i*2]-1:mismTime[maxA_i*2+1]])
    #P_peak_t2 = P.index(max(P[mismTime[maxA_i*2]-1:mismTime[maxA_i*2+1]]))
    P_peak_t2 = np.where(P_insp == np.amax(P_insp[mismTime[maxA_i*2+1]:]))[0][0]

    print('Yes')
    print('peak1')
    print(P_peak_t1)
    print('peak2')
    print(P_peak_t2)



# Compare with threshold

    P_eff = np.array(P_insp[P_peak_t1:P_peak_t2])
    P_eff_norm = ((P_eff-min(P_eff))/(max(P_eff)-min(P_eff)))-1    
    t_eff = np.array(Time_insp[P_peak_t1 : P_peak_t2])
    sigma = np.std(t_eff)
    print('sigma')
    print(sigma)
    
    u = np.mean(t_eff)
    u_array = np.full(np.size(P_eff_norm),u)
    sig_array = np.full(np.size(P_eff_norm),sigma)
    print(u)
    #t_eff_norm = np.array(np.linspace(u-1*sigma, u+1*sigma, np.size(P_eff_norm)))
    t_eff_norm = np.array(Time_insp[P_peak_t1 : P_peak_t2]) 

    #print('t_eff')
    #print(t_eff)
    #print('t_eff_min')
    #print(max(t_eff)-min(t_eff))
    #print('t_eff_max')
    #print(max(t_eff))
    print('t_eff_norm')
    print(t_eff_norm)

    plt.figure()
    plt.plot(t_eff_norm,P_eff_norm,label = "P")
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Graph of P_norm against Time_norm')
    plt.legend() 
    plt.show()

    # Non linear regression to compute u (location of centroids)
    def P_eff_func(xin,p1,A1,A2,A3):
        u, x, sigma = xin
        cnt = 2*sigma 
        return A1*np.exp((-(x-p1)**2)/(2*sigma/cnt)) + A2*np.exp((-(x-u)**2)/(2*sigma/cnt)) + A3*np.exp((-(x-(2*u-p1))**2)/(2*sigma/cnt))

    #  bounds=([u-sigma, u-sigma, -np.inf, -np.inf, -np.inf], [u+sigma, u+sigma, np.inf, np.inf, np.inf])
    ini_guess = [0]*4
    c,cov = curve_fit(P_eff_func, (u_array, t_eff_norm, sig_array),P_eff_norm, p0=ini_guess,maxfev=100000 )
    print('p1:')
    print(c[0])
    print('A1:')
    print(c[1])
    print('A2:')
    print(c[2])
    print('A3:')
    print(c[3])

    p1 = c[0]
    A1 = c[1]
    A2 = c[2]
    A3 = c[3]
    x = t_eff_norm
    Psim_eff = A1*np.exp((-(x-p1)**2)) + A2*np.exp((-(x-u)**2)) + A3*np.exp((-(x-(2*u-p1))**2))

    plt.figure()
    plt.plot(t_eff_norm,P_eff_norm,label = "P")
    plt.plot(t_eff_norm,Psim_eff,label = "Psim")
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Graph of P and Psim against Time')
    plt.legend() 
    plt.show()

        # 
        #phi_1 = [0]*len(P)
        #phi_2 = [0]*len(P)
        #phi_3 = [0]*len(P)



        #phi_1[P_peak_t1:P_peak_t2 + 1] = np.exp(-((P_eff_norm+c[0])**2))
        #phi_2[P_peak_t1:P_peak_t2 + 1] = np.exp(-((P_eff_norm)**2))        
        #phi_3[P_peak_t1:P_peak_t2 + 1] = np.exp(-((P_eff_norm-c[0])**2))

    def P_fitted_func(x,A1,A2,A3,Ers,Rrs):
        V, Q, t_eff, u, p1, cond, sigma = x
        cnt = 2*sigma
        return  (Ers*V) + (Rrs*Q) + (cond*A1*np.exp((-(t_eff-p1)**2)/(2*sigma/cnt))) + (cond*A2*np.exp((-(t_eff-u)**2)/(2*sigma/cnt))) + (cond*A3*np.exp((-(t_eff-(2*u-p1))**2)/(2*sigma/cnt)))

    #t_eff2 = np.array([0]*len(P_insp))
    #t_eff2[P_peak_t1:P_peak_t2] = t_eff_norm
    t_eff2 = np.array(Time_insp)

    cond = np.array([0]*len(P_insp))
    onearray = np.full(np.size(t_eff_norm),1)
    cond[P_peak_t1:P_peak_t2] = onearray       
        
    p1_array = np.array(np.full(np.size(P_insp),c[0]))
    p2_array = np.array(np.full(np.size(P_insp),2*u-c[0]))
    u_array = np.array(np.full(np.size(P_insp),u))
    sig_array = np.array(np.full(np.size(P_insp),sigma))


 #, bounds=([-np.inf, -np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, 40, np.inf])
    ini_guess2 = [0]*5
    param,cov2 = curve_fit(P_fitted_func,(V_insp, Q_insp, t_eff2, u_array, p1_array, cond, sig_array),P_insp)

    A1 = param[0]
    A2 = param[1]
    A3 = param[2]
    Ers = param[3]
    Rrs = param[4]
    
    
    print('New parameters:')
    print('A1:')
    print(A1)
    print('A2:')
    print(A2)
    print('A3:')
    print(A3)


#    return P, Q, Ers, Rrs, PEEP, PIP, Vtidal, V, A1, A2, A3, u, t_eff2, cond

    Psim_insp = (Ers*V_insp)+(Rrs*Q_insp)+(cond*A1*np.exp((-(t_eff2-p1_array)**2)/(2*sigma)))+(cond*A2*np.exp((-(t_eff2-u_array)**2)/(2*sigma)))+(cond*A3*np.exp((-(t_eff2-(2*u_array-p1_array))**2)/(2*sigma))) +PEEP
        
print('Ers:')
print(Ers)
print('Rrs:')
print(Rrs)
print(cond)

plt.figure()
plt.plot(Time_insp,P_insp,label = "P")
#plt.plot(Time_insp,Psim_insp,label = "Psim")
plt.xlabel('Time')
plt.ylabel('Pressure')
plt.title('Graph of P and Psim against Time')
plt.legend() 
plt.show()