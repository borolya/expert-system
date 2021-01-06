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

# def build_df(vars_list, queries, facts):
# 	queries_index = [vars_list.index(el) for el in queries.difference(facts)]
# 	facts_index = [vars_list.index(el) for el in facts]
# 	# print(queries.difference(facts))
# 	# print(facts)
# 	df = pd.DataFrame(columns=vars_list)
# 	for row in product('01', repeat=len(vars_list)):
# 		if ('0' in ''.join([row[ind] for ind in queries_index]) #try to add 1 for facts
# 			and '0' * len(facts) == ''.join([row[ind] for ind in facts_index])):
			
# 			df.loc[''.join(row)] = list(row)
# 	df = df.apply(pd.to_numeric)
# 	df.reset_index(inplace=True)
# 	# print(df)
# 	return df

def compute_value(rule, coll, allVars):
	# print(rule)
	stack = list()
	for el in rule:
		if el not in operands:
			# print(el)
			# print(coll)
			# print(allVars[el])
			# print(coll[allVars[el]])
			stack.append(int(coll[allVars[el]]))
		else:
			if (el == '!'):
				stack.append(neg(stack.pop()))
			else:
				vars = [stack.pop()]
				vars.append(stack.pop())
				stack.append(oper_to_func[el](vars[1], vars[0]))
		# print("stack_tmp:", stack)
	# print("stack:", stack)
	return stack.pop()

# def compute_values_for_rule(rule, collections_list):
# 	new_zero_index = set()
# 	for index, row in collections_list.iterrows():
# 		if compute_value(rule, row) == 0:
# 			new_zero_index.add(index) 
# 	return new_zero_index

# def process_rule(rule, collections_list, index_equal_one, index_equal_zero):
# 	new_zero_index = compute_values_for_rule(rule, collections_list.loc[index_equal_one])
# 	index_equal_one.difference_update(new_zero_index)
# 	index_equal_zero.update(new_zero_index)
# 	return

# def process_fact(fact, collections_list, index_equal_one, index_equal_zero):
# 	new_zero_index = set(collections_list.loc[index_equal_one].loc[collections_list[fact] == 0].index)
# 	index_equal_one.difference_update(new_zero_index)
# 	index_equal_zero.update(new_zero_index)
# 	return

def build_cnf(data):
	allVarsList = list(data['events'])
	allVarsList.sort()
	allVars = {el[1]: el[0] for el in enumerate(allVarsList)}
	# print(allVars)
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
	# for el in cnf:
	# 	print(el)
	return cnf, notCnf, allVars







	# collections_list = build_df(all_vars_list, data['queries'], data['facts'])
	# # print('collections are built')
	# index_equal_one = set(collections_list.index)
	# index_equal_zero = set()
	# for rule in data['rpn_rules']:
	# 	# print(rule)
	# 	process_rule(rule, collections_list, index_equal_one, index_equal_zero)
	# for fact in data['facts']:
	# 	# print(fact)
	# 	process_fact(fact, collections_list, index_equal_one, index_equal_zero)
	# return collections_list, index_equal_one

# def throw_away_vars1(collections_list, index_equal_one, data):
# 	vars = data['events'].difference(data['queries']).difference(data['facts'])
# 	index_to_ignore = set()
# 	for index, row in collections_list.loc[index_equal_one].iterrows():
# 		if '1' in ''.join([str(el) for el in row[vars]]):
# 			index_to_ignore.add(index)
# 	return index_equal_one.difference(index_to_ignore)

def analyzeVars(cnf, allVars, queries):
	resTmp = {query: [0, 0] for query in queries}
	for coll in cnf:
		for query in queries:
			if coll[allVars[query]] == '0':
				resTmp[query][0] += 1
			else:
				resTmp[query][1] += 1
	half = 2 ** (len(allVars) - 1)
	result = {query: False for query in queries}
	# print(resTmp)
	for query in queries:
		if resTmp[query][0] == half and resTmp[query][1] == half:
			print("Contradiction! Any statement might be obtained!")
			return None
		if resTmp[query][0] == half:
			result[query] = True
	return result

def addFalseVars(cnf, notCnf, freeVars, allVars):
	for row in notCnf:
		for var in freeVars:
			if freeVars[var] == False and row[allVars[var]] == '1':
				cnf.add(row)
				break

# def detectFalseVars(cnf, allVars, freeVars):


def analyze_problem(data):
	# print("diff", data['events'].difference(data['facts']).difference(['queries']))
	cnf, notCnf, allVars = build_cnf(data)
	# for el in cnf:
	# 	print(el)
	# tmpSet = data['events'].difference(data['facts']).difference(data['queries'])
	# print("tmpSet", tmpSet)
	freeVars = analyzeVars(cnf, allVars, data['events'].difference(data['facts']).difference(data['queries']))
	# print(freeVars)
	addFalseVars(cnf, notCnf, freeVars, allVars)
	result = analyzeVars(cnf, allVars, data['queries'])
	if result is None:
		return
	# if resQ is None:
	# 	return
	# result[query] = resQ
	print(result)
	# collections_list, index_equal_one = build_cnf(data)
	# print(collections_list)
	# index_equal_one = throw_away_vars1(collections_list, index_equal_one, data)
	# result = {el: True for el in data['queries']}
	# for el in data['queries']:
	# 	if len(collections_list.loc[index_equal_one].loc[collections_list[el] == 0]) > 0:
	# 		result[el] = False
	# print(collections_list.loc[index_equal_one].loc[collections_list[el] == 0])
	# print(result)
	# return result
