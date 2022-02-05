import sys, json
from createChomsky import formChomsky

def main(file):

    with open(file) as jsonFileRead:
        jsonData = json.load(jsonFileRead)
        variables = jsonData['glc'][0]
        terminals = jsonData['glc'][1]
        rules =     jsonData['glc'][2]
        start =     jsonData['glc'][3]
        formChomsky(variables, terminals, rules, start)

main(sys.argv[1])