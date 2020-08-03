import numpy as np

def calcRate(i, durations, Vtidals):
    total_dur = 0
    if i <5 :
        for x in durations:
            total_dur = total_dur + x
        RR = (i+1)*60/total_dur
    else:
        durations.pop(0)
        Vtidals.pop(0)
        for x in durations:
            total_dur = total_dur + x
        RR = 5*60/total_dur
        
    VE = RR*np.mean(Vtidals)
    return RR, VE, durations, Vtidals
        