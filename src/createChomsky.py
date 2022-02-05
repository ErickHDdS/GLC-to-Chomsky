import pprint, time

from normalChomsky import stepONE, stepFIVE, stepTWO, stepTHREE, stepFOUR

def formChomsky(variables, terminal, rules, start):
    variable = {}
    finalRules = []

    ruleONE                 = stepONE(rules, start)
    ruleTWO                 = stepTWO(variables, ruleONE)
    ruleTHREE, variable[0]  = stepTHREE(variables, terminal, ruleTWO, start)
    ruleFOUR, variable[1]   = stepFOUR(variable[0], terminal, ruleTHREE)
    ruleFIVE, variable[2]   = stepFIVE(variable[1], ruleFOUR)

    variableInitial = {}
    variableFinal = {}
    rules = {}
    char = {}
    variables = {}
    data = {}

    newVariables =  []
    rules[start] = []
   
    position = 0

    while position < len(variable[0]) or position < len(variable[2]): 
        if position < len(variable[0]):
            char[0] = variable[0][position]
            if(char[0] != start): 
                variableInitial[char[0]] = []
        
        if position < len(variable[2]):     
            char[1] = variable[2][position]
            if char[1] not in variable[0]:
                variableFinal[char[1]] = [] 
        position += 1

    rules.update(variableInitial)  
    rules.update(variableFinal)
    rules.items()

    position = {} 
    count = 0

    for position in rules.keys():
        variables[count] = position
        count +=1

    count = 0
    while count < len(variables):
        newVariables.append(variables.get(count))
        count +=1

    # PRINT CHOMSKY
    data["glc"] = [newVariables, terminal, ruleFIVE, start]
    
    pprint.pprint(data, indent=2)