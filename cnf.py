import pandas as pd
from itertools import product

def conj(a, b):
	if a == 1 and b == 1:
		return 1
	return 0

def disj(a, b):
	if a == 0 and b == 0:
		return 0
	return 1

def xor(a, b):
	if (a == 0 and b == 0) or (a == 1 and b == 1):
		return 0
	return 1

def impl(a, b):
	if (a == 1 and b == 0):
		return 0
	return 1

def rev_impl(a, b):
	return impl(b, a)

def eqv(a, b):
	return 1 - xor(a, b)

def neg(a):
	return 1 - a

operands = set(["!", "+", "|", "^", "=>", "<=", "<=>"])

oper_to_func = {
	"!": neg,
	"+": conj,
	"|": disj,
	"^": xor,
	"=>": impl,
	"<=": rev_impl,
	"<=>": eqv
}

def compute_value(rule, coll, allVars):
	stack = list()
	for el in rule:
		if el not in operands:
			stack.append(int(coll[allVars[el]]))
		else:
			if (el == '!'):
				stack.append(neg(stack.pop()))
			else:
				vars = [stack.pop()]
				vars.append(stack.pop())
				stack.append(oper_to_func[el](vars[1], vars[0]))
	return stack.pop()


def build_cnf(data):
	allVarsList = list(data['events'])
	allVarsList.sort()
	allVars = {el[1]: el[0] for el in enumerate(allVarsList)}
	cnf = set()
	notCnf = set()
	for row in product('01', repeat=len(allVarsList)):
		flag = 0
		for fact in data['facts']:
			if row[allVars[fact]] == '0':
				cnf.add(''.join(row))
				flag = 1
				break
		if flag == 1:
			continue
		for rule in data['rpn_rules']:
			if compute_value(rule, row, allVars) == 0:
				cnf.add(''.join(row))
				flag = 1
				break
		if flag == 0:
			notCnf.add(''.join(row))
	return cnf, notCnf, allVars


def analyzeVars(cnf, allVars, queries):
	if len(cnf) == 2 ** len(allVars):
		print("Contradiction! Any statement might be obtained!")
		exit()
	resTmp = {query: [0, 0] for query in queries}
	for coll in cnf:
		for query in queries:
			if coll[allVars[query]] == '0':
				resTmp[query][0] += 1
			else:
				resTmp[query][1] += 1
	half = 2 ** (len(allVars) - 1)
	result = {query: 'Undefined' for query in queries}
	undefVars = {query for query in queries}
	# print(resTmp)
	for query in queries:
		if resTmp[query][0] == half or resTmp[query][1] == half:
			result[query] = True if resTmp[query][0] == half else False
			undefVars.remove(query)
	return result, undefVars

def addFalseVars(cnf, notCnf, vars, allVars):
	totalMovedColls = set()
	for var in vars:
		movedColls = addFalseVar(cnf, notCnf, var, allVars)
		totalMovedColls.update(movedColls)
	return totalMovedColls

def addFalseVar(cnf, notCnf, var, allVars):
	movedColls = set()
	for row in notCnf:
		if row[allVars[var]] == '1':
			cnf.add(row)
			movedColls.add(row)
	notCnf.difference_update(movedColls)
	return movedColls
	

# def recursiveAnalyzer(cnf, notCnf, allVars, result):
# 	for var in result.keys():
# 		if result[var] == 'Undefined':
# 			movedColls = addFalseVars(cnf, notCnf, var, allVars)
# 			if len(cnf) == 2 ** len(allVars):
# 				cnf.difference_update(movedColls)
# 				notCnf.update(movedColls)
# 				return -1
# 			newResult = analyzeVars(cnf, allVars, result.keys())
# 			if 'Undefined' in newResult.values():
# 				if recursiveAnalyzer(cnf, notCnf, allVars, newResult) == -1:
# 					cnf.difference_update(movedColls)
# 					notCnf.update(movedColls)
# 					return -1
# 			else:
# 				return newResult

def analyze_problem(data):
	# print(data)
	cnf, notCnf, allVars = build_cnf(data)
	result, undefVars = analyzeVars(cnf, allVars, data['events'].difference(data['facts']))
	varsInfo = (list(data["left_side"].difference(data["right_side"])) +
		list(data["left_side"].intersection(data["right_side"])) +
		list(data["right_side"].difference(data["left_side"])))
	# print(undefVars)
	# print(varsInfo)
	while len(undefVars) > 0:
		for var in varsInfo:
			if var in undefVars:
				addFalseVar(cnf, notCnf, var, allVars)
				break
		# undefVars = set()
		# for var in result.keys():
		# 	if result[var] == 'Undefined':
		# 		undefVars.add(var)
		# undefVars.intersection_update(data['false_event_priority'])
		# print(undefVars)
		# movedColls = addFalseVars(cnf, notCnf, undefVars, allVars)
		# print(movedColls)
		# print(cnf)
		# result = analyzeVars(cnf, allVars, data['events'].difference(data['facts']))
		# print(result)
		# if 'Undefined' in result.values():
		# 	print("SHIT")
		# 	return
		# for key in result.keys():
		# 	if key in data['queries']:
		# 		print(key, 'is', result[key])
		result, undefVars = analyzeVars(cnf, allVars, data['events'].difference(data['facts']))
	for key in data['queries']:
		if key in data['facts']:
			print(key, 'is True')
		else:
			print(key, 'is', result[key])
