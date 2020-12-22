import re

#double !! i dont implement

PRIOPIRY = {
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
    i = 0
    while i < len(rule):
        r = re.match(r'<?=>?', rule[i:])
        if r != None:
            symbol = r.group(0)
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
        elif len(operation_stack)!=0 and PRIOPIRY[symbol] <= PRIOPIRY[operation_stack[-1]]:
            rpn_stack.append(operation_stack.pop())
            operation_stack.append(symbol)
        else:
            operation_stack.append(symbol)
        #print("\ni = ", i)
        #print("symbol = ", symbol)
        #print("stack_rpn", rpn_stack)
        #print("operation_stack", operation_stack)
        i += len(symbol)
    while len(operation_stack) != 0:
        rpn_stack.append(operation_stack.pop())
    return rpn_stack
     