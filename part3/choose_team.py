#!/usr/local/bin/python3

import sys

def load_people(filename):
    people = []
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people.append( [ l[0] ] + [ float(l[1]) ] + [ float(l[2]) ] )
    
    return people

#checks for all possible combinations
def comb(people):
    comb = [[]]
    for people in people:
        newset = [r+[people] for r in comb]
        comb.extend(newset)
    return comb

#Looks for best combination which satisfies our condition
def approx_solve(people, budget):
    solution = []
    skill = 0
    x = comb(people)
    for elem in x:
        set_skill = sum([e[1] for e in elem])
        set_budget = sum([e[2] for e in elem])
        if set_budget < budget:
            skill += set_skill
            solution = elem
    
    total_skill = round(sum(elem[1] for elem in solution), 2)
    total_cost = round(sum(elem[2] for elem in solution), 2)
    
    return solution, total_skill, total_cost
            
if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution, total_skill, total_cost = approx_solve(people, budget)
    
    print("Found a group with %d people costing %f with total skill %f" % \
                   ( len(solution), total_cost, total_skill ))
    
    for s in solution:
        print(s[0], float(1))
