import json
import numpy as np
from dataProcess2 import dataProcess2
from dataArrange import oneBreath


def dataCompile2(bNum,rawData):
    
    # Extract Breath number, Pressure and Flow rate 
    # msg = oneBreath(rawData, breathNumber)

    # Process data
    P, Q, Ers, Rrs, PEEP, PIP, Vtidal, V = dataProcess2(rawData,bNum)

    compiledfile = {
        'BNum' : bNum,
        'Pressure' : P,
        'FlowRate' : Q,
        'Ers' : Ers,
        'Rrs' : Rrs,
        'PEEP' : PEEP,
        'PIP' : PIP,
        'Vtidal' : Vtidal,
        'Volume' : list(V)
    }
    
    duration = np.size(P)*0.02
    output = json.dumps(compiledfile)

    return output, duration



