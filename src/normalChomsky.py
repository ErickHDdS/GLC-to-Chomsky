import string

def stepONE(rules, starter): 
    deleteRulesLAMBDA = []
    auxRule = {}
    LAMBDA = {}
    condition = {}
    LAMBDA[0] = set()
    index=0
    for rule in rules:
        if rule[1] == '#': 
            LAMBDA[0].add(rule[0])
    LAMBDA[1] = LAMBDA[0]
    for letter in rule[1]:
        if letter not in LAMBDA[1]:
            condition[0] = False
            break
    condition[0] = True

    while condition[0]:
        leng = len(LAMBDA[1])
        for rule in rules:
            for letter in rule[1]:
                if letter not in LAMBDA[1]:
                    condition[1] = False
                    break
                condition[1] = True
            if condition[1]: 
                LAMBDA[1].add(rule[0])
        if not (len(LAMBDA[1]) > leng): break
        for rule in rules:
            for letter in rule[1]:
                if letter in LAMBDA[1]:
                    parameter = range(0, len(rule[1]))
                    list_ = list(parameter)
                    lenght = len(list_)
                    power = [[list_[j] for j in range(lenght) if i&1<<j] for i in range(2**lenght)]
                    power_=[]
                    for index in power:
                        auxRule = list(rule[1])
                        for number in index:            
                            if auxRule[number] in LAMBDA[1]: 
                                auxRule[number] = ""    
                        auxRule = ''.join(auxRule)                  
                        if auxRule not in power_: 
                            power_.append(auxRule)

                    if len(power_) > 1:
                        for index in power_:
                            complement = [rule[0], index]
                            if complement not in deleteRulesLAMBDA:
                                if complement[0] == starter and complement[1] == '':
                                    complement[1] = '#'
                                deleteRulesLAMBDA.append(complement)
                    else: 
                        deleteRulesLAMBDA.append([rule[0],power_])
                elif rule[0] != starter and rule[1] == '#':
                    power_ = ''
                    complement = [rule[0], power_] 
                    if complement not in deleteRulesLAMBDA: 
                        deleteRulesLAMBDA.append(complement)
                elif rule not in deleteRulesLAMBDA: 
                        deleteRulesLAMBDA.append(rule)

    parameter = range(0, len(deleteRulesLAMBDA))
    for index in parameter:
        if deleteRulesLAMBDA[index][0] == deleteRulesLAMBDA[index][1] and deleteRulesLAMBDA[index][1] == '':
            deleteRulesLAMBDA = deleteRulesLAMBDA.pop(index)
            index=0            
        else: index += 1

    return deleteRulesLAMBDA

def stepTWO (variables, rules):
    closures = {}
    newRules = []
    for var in variables:
        closures[var] = [var]
        for rule in rules:
            if var is rule[0] and len(rule[1]) == 1 and rule[1][0] in variables: 
                closures[var].append(rule[1][0])
    for closure in closures.keys():
        newRulesModify = []
        for rule in rules:
            ruleLenght = len(rule[1])
            if rule[0] == closure:
                if ruleLenght == 1:
                    if rule[1][0] not in variables: 
                        newRulesModify.append(rule)
                else: 
                    newRulesModify.append(rule)
        rules_ = newRulesModify
        for var in closures[closure]:
            if var != closure:
                for rule in rules:
                    if rule[0] == var and len(rule[1]) == 1 and rule[1][0] not in variables: 
                        rules_.append([closure, rule[1]])
        for rule in rules_: 
            if rule not in newRules: 
                newRules.append(rule)

    return newRules

def check (rule, OP, variable, terminals, value):
    if OP:
        for letter in rule[1]:
            if letter in terminals and letter not in value: return False
        return True   
    elif rule[0] not in value: return False
    for letter in rule[1]:
        if letter not in value and letter in variable: return False

    return True
       
def stepTHREE(variables, terminals, rules, starter):
    length = {}
    condition = {}
    auxVariable = set()
    value = set()
    variable = set()

    length[0] = 0
    length[1] = 0
    length[2] = 0

    variable.add(starter)

    ruleONE = []
    newRules = []

    condition[0] = len(auxVariable) > length[0]
    while not condition[0]:
        length[0] = len(auxVariable)
        for rule in rules:
            if rule[1] != '':
                for letter in rule[1]:
                    if letter in terminals or letter in auxVariable: 
                        auxVariable.add(rule[0])
        condition[0] = len(auxVariable) > length[0]
        
    for rule in rules:
        if check(rule, False, variables, None, auxVariable) and rule[1] != '': 
            ruleONE.append(rule)

    condition[1] = (len(variable) > 0 and (not (len(variable) > length[2] and len(value) > length[1])))
    while condition[1]:
        length[1] = len(value)
        length[2] = len(variable)
        for rule in ruleONE:
            if rule[0] in variable:
                for letter in rule[1]:
                    if letter in auxVariable: 
                        variable.add(letter)
                    elif letter in terminals: 
                        value.add(letter)
        condition[1] = (len(variable) > 0 and (not (len(variable) > length[2] and len(value) > length[1])))

    for rule in ruleONE:
        if check(rule, False, auxVariable, None, variable) and check(rule, True, None, terminals, value):  
            newRules.append(rule)

    return newRules, list(variable)

def conditionalFunction(char, newRule, newRules, newVariables, condition):
    if condition: 
        newRule = ''.join(newRule)
    ruleAUX = []
    auxNewVar = False
    var = None
    for rule in newRules:
        if rule[1] == char and rule[0] in newVariables:
            auxNewVar = True
            var = rule[0]
    if not auxNewVar:                    
        for letter in list(string.ascii_uppercase):
            if letter not in newVariables:
                newVariables.append(letter)
                newRules.append([letter, char])
                if condition and newRule.find(letter): 
                    newRule = newRule.replace(char, letter)                   
                else:                                        
                    ruleAUX = list(newRule)
                    for id, item in enumerate(ruleAUX):
                        if item == char: 
                            ruleAUX[id] = letter
                    newRule = ''.join(ruleAUX)
                break
    elif condition:
        if newRule.find(var): 
            newRule = newRule.replace(char, var)
        newRule = ''.join(newRule)
    else: 
        ruleAUX = list(newRule)
        for id, item in enumerate(ruleAUX):
            if item == char: 
                ruleAUX[id] = var
        newRule = ''.join(ruleAUX)

    return newRule, newRules, newVariables

def stepFOUR(variables, terminals, rules):
    newRules = []
    for rule in rules:
        if len(rule[1]) > 1:
            auxNewRule = False
            newRule = rule[1]
            for char in rule[1]:
                if char in terminals:
                    auxNewRule = True
                    newRule, newRules, variables = conditionalFunction(char, newRule, newRules, variables, False)
            if auxNewRule: argument = [rule[0], newRule]
            else: argument = rule
        else: argument = rule
        newRules.append(argument)

    return newRules, variables

def stepFIVE(variables, rules):
    newRules = rules.copy()
    rulesToRemove = []
    auxNewRule = ''
    for rule in rules:
        if len(rule[1]) > 2:
            auxNewRule = ''
            newRule = list(rule[1])
            parameter = range(1, len(newRule))
            for i in parameter:
                auxNewRule = auxNewRule + newRule[i]
                newRule = ''.join(newRule)
            newRule, newRules, variables = conditionalFunction(auxNewRule, newRule, newRules, variables, True)
            argument = [rule[0], newRule]            
        else: argument = rule
        newRules.append(argument)     
        rulesToRemove.append(rule) 
    for rule in rulesToRemove:
        newRules.remove(rule)

    return newRules, variables