import re

#double !! i dont implement

PRIORITY = {
    "(": 0,
    ")": 0,
    "!": 6,
    "+": 5,
    "|": 4,
    "^": 3,
    "=>": 2,
    "<=": 2,
    "<=>": 1 
}

def rpn(rule):
    rpn_stack = []
    operation_stack = []
    prior_events = set()
    non_prior_events = set()
    i = 0
    while i < len(rule):
        r = re.match(r'<?=>?', rule[i:])
        if r != None:
            symbol = r.group(0)
            if symbol != '<=>':
                prior_events = set(re.findall(r'[A-Z]', rule[:i]))
                non_prior_events = set(re.findall(r'[A-Z]', rule[i:]))
                if symbol == '<=':
                    tmp = non_prior_events
                    non_prior_events = prior_events
                    prior_events = tmp
        else:
            symbol = rule[i]
        if symbol.isalpha():
                rpn_stack.append(symbol)
        elif symbol == '(':
            operation_stack.append(symbol)
        elif symbol == ')':
            while (operation_stack[-1] != '('):
                rpn_stack.append(operation_stack.pop())
            operation_stack.pop()
        else:
            while len(operation_stack)!=0 and PRIORITY[symbol] <= PRIORITY[operation_stack[-1]]:
                rpn_stack.append(operation_stack.pop())
            operation_stack.append(symbol)
        i += len(symbol)
    while len(operation_stack) != 0:
        rpn_stack.append(operation_stack.pop())
    if prior_events == set():
        non_prior_events = set(re.findall(r'[A-Z]', rule))
    return rpn_stack, prior_events, non_prior_events
     