import json
from dataProcess import dataProcess
from dataArrange import oneBreath


def dataCompile(breathNumber,rawData):
    
    # Extract Breath number, Pressure and Flow rate 
    msg = oneBreath(rawData, breathNumber)

    # Process data
    Ers, Rrs, PEEP, PIP, Vtidal, V = dataProcess(msg)

    compiledfile = {
        'BNum' : msg[0],
        'Pressure' : msg[2::2],
        'FlowRate' : msg[1::2],
        'Ers' : Ers,
        'Rrs' : Rrs,
        'PEEP' : PEEP,
        'PIP' : PIP,
        'Vtidal' : Vtidal,
        'Volume' : list(V)
    }

    output = json.dumps(compiledfile)

    return output



