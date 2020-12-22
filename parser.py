import re
import sys

def get_rule(line):
    origin_binar_operation = ['+', '^', '|', '=>', '<=', '<=>']
    if line[0] == '=' or len(re.findall(r'\?', line)) != 0:
        return None, None
    if len(re.findall(r'![^A-Z\(]', line)) != 0:
        exit("bad using '!' in line \n\t" + line)
    real_binar_operation = re.split(r'[!\()]*[A-Z]\)*', line)
    if real_binar_operation[0] != '' or real_binar_operation[-1] != '':
        exit("incorrect binar operation in line \n\t" + line)
    real_binar_operation.pop(0)
    real_binar_operation.pop(-1)
    if not set(real_binar_operation) <= set(origin_binar_operation):
        exit("incorrect binar operation in line \n\t" + line)
    #breckets check
    brackets = re.findall(r'[\(\)]', line)
    brackets_stack = []
    for b in brackets:
        if b == '(':
            brackets_stack.append('(')
        elif len(brackets_stack) == 0:
            exit("non correct brackets in line \n\t" + line)
        else:
            brackets_stack.pop()
    if len(brackets_stack) != 0:
        exit("non correct brackets in line \n\t" + line)
    return line, set(re.findall(r'[A-Z]', line))

def get_facts(line):
    if line[0] != '=':
        return set()
    if len(re.findall(r'[^A-Z]', line[1:])) != 0:
        exit("non correct facts in line \n\t" + line)
    return (set(line[1:]))

def get_queries(line):
    if line[0] != '?' or len(line) == 1:
        exit("bad line \n\t" + line)
    if len(re.findall(r'[^A-Z]', line[1:])) != 0:
        exit("non correct queries in line \n\t" + line)
    return (set(line[1:]))


def get_data(fd):
    rules = []
    events = set()
    queries = set()
    facts = set()
    
    while True:
        try:
            line = fd.readline()
        except Exception as e:
            exit(e)
        if line == '':
            fd.close()
            break
        line = re.split(r'\s*#|\s*\n', line)[0]
        line = re.sub(r'\s*', '', line)
        if len(re.findall(r'[^A-Z=<>\?\(\)\+|!^]', line)) != 0:
            sys.exit("non correct symbol in line \n\t"+ line)
        if line != '':
            [rule, new_events] = get_rule(line)
            if rule == None:
                new_facts = get_facts(line)
                facts = facts.union(get_facts(line))
                if new_facts == set():
                    queries = queries.union(get_queries(line))
            else:
                rules.append(rule)
                events = events.union(new_events)
    data = {
        "rules": rules, 
        "events": events,
        "queries": queries,
        "facts": facts
    }
    for d in data:
        if len(data[d]) == 0:
            exit("There is no information about " + d)
    return data