import re
import sys
#def preparing_string(fd):




def checking_rule(line):
    origin_binar_operation = ['+', '^', '|', '=>', '<=', '<=>']
    print(line)

    if line[0] == '=' or len(re.findall(r'\?', line)) != 0:
        return #?null?
    if len(re.findall(r'![^A-Z\(]', line)) != 0:
        exit("bad using '!' in line " + line)
    real_binar_operation = re.split(r'(?:!?\(*!?)*[A-Z]\)*', line)
    if real_binar_operation[0] != '' or real_binar_operation[-1] != '':
        exit("incorrect binar operation in line " + line)
    real_binar_operation.pop(0)
    real_binar_operation.pop(-1)
    #print(re.findall(r'(?:!?\(*!?)*[A-Z]\)*', line))
    #print(real_binar_operation)
    if not set(real_binar_operation) <= set(origin_binar_operation):
        exit("incorrect binar operation in line " + line)
    #breckets check
    brackets = re.findall(r'[\(\)]', line)
    brackets_stack = []
    for b in brackets:
        if b == '(':
            brackets_stack.append('(')
        elif len(brackets_stack) == 0:
            exit("non correct brackets in line " + line)
        else:
            brackets_stack.pop()
    if len(brackets_stack) != 0:
        exit("non correct brackets in line " + line)
    print(re.findall(r'[A-Z]', line))
    print(set(re.findall(r'[A-Z]', line)))
    return line, set(re.findall(r'[A-Z]', line))


    #check unar_operation 

    #check this is formula
#def checking_fucts(line):
#def checking_queries(line):

def get_data(fd):
    #queries 
    #facts 
    rules = []
    events = set()

    while True:
        try:
            line = fd.readline()
        except Exception as e:
            print("somthing")
        if line == '':
            fd.close()
            break
        line = re.split(r'\s*#|\s*\n', line)[0]
        line = re.sub(r'\s*', '', line)
        print(line)
        if len(re.findall(r'[^A-Z=<>\?\(\)\+|!^]', line)) != 0:
            sys.exit("non correct symbol in line "+ line)
        if line != '':
            [rule, new_events] = checking_rule(line)
            rules.append(rule)
            events.union(new_events)
    return rules, events
        
#    sys.exit(e)