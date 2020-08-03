def oneBreath(one,ini): 
    two=one[ini].replace('\n',',')    
    three=two.replace('BS','')
    four=three.replace('S:','')
    five=four.split(",")

    while (""in five):
        five.remove("")

    six = [float(j) for j in five]

    return six