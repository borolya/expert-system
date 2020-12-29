import pandas as pd

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

def build_df(vars_list):
	df = pd.DataFrame(columns=vars_list)
	for num in range(2 ** len(vars_list)):
		tmp = str(bin(num))[2:]
		row = '0' * (len(vars_list) - len(tmp)) + tmp
		df.loc[num] = list(row)
	df = df.apply(pd.to_numeric)
	return df

def compute_value(rule, coll):
	stack = list()
	for el in rule:
		if el not in operands:
			stack.append(coll[el])
		else:
			if (el == '!'):
				stack.append(neg(stack.pop()))
			else:
				vars = [stack.pop()]
				vars.append(stack.pop())
				stack.append(oper_to_func[el](vars[1], vars[0]))
	# print(len(stack))
	return stack.pop()


def compute_values_for_rule(rule, df, length):
	res_col = list()
	for i in range(length):
		res_col.append(compute_value(rule, df.loc[i]))
	df['result'] = res_col
	return df.loc[df['result'] == 0]

def generate_full_cnf(cnf_df, vars_list, all_vars_list):
	free_vars = list()
	for el in all_vars_list:
		if el not in vars_list:
			free_vars.append(el)
	free_df = build_df(free_vars)
	free_df = free_df.astype(str)
	# dic = {el: list() for el in all_vars_list}
	rule_cnf = set()
	for _, row in cnf_df.iterrows():
		for _, frow in free_df.iterrows():
			bit_code = '0b'
			for var in all_vars_list:
				try:
					bit_code += row[var]
				except KeyError:
					bit_code += frow[var]
			print(bit_code)
			rule_cnf.add(int(bit_code, 2))
			# for dep_var in vars_list:
			# 	dic[dep_var].append(row[dep_var])
			# for free_var in free_vars:
			# 	dic[free_var].append(frow[free_var])
	# full_cnf = pd.DataFrame(columns=all_vars_list)
	# for el in all_vars_list:
	# 	full_cnf[el] = dic[el]
	# full_cnf = full_cnf.apply(pd.to_numeric)
	return rule_cnf

def process_rule(rule, all_vars_list, data):
	# print(rule)
	vars_list = set(rule)
	for operand in operands:
		if operand in vars_list:
			vars_list.remove(operand)
	vars_list = list(vars_list)
	# print(vars_list)
	df = build_df(vars_list if len(vars_list) < len(all_vars_list) else all_vars_list)
	# print(df)
	cnf_df = compute_values_for_rule(rule, df, 2 ** len(vars_list))
	# print(df)
	# print(cnf_df)
	# print(data['all_vars_list'])
	cnf_df = cnf_df.astype(str)
	if len(vars_list) < len(all_vars_list):
		return generate_full_cnf(cnf_df, vars_list, all_vars_list)
	return {int('0b' + ''.join(row), 2) for _, row in cnf_df.iterrows()}
	# if len(vars_list) < len(all_vars_list):
	# 	full_rule_cnf = generate_full_cnf(cnf_df, vars_list, all_vars_list)
	# else:
	# 	full_rule_cnf = pd.DataFrame(columns=all_vars_list)
	# 	for el in all_vars_list:
	# 		full_rule_cnf[el] = cnf_df[el]
	# return full_rule_cnf

def process_fact(fact, all_vars_list, data):
	cnf_df = pd.DataFrame(columns=[fact])
	cnf_df[fact] = ['0']
	# print(cnf_df)
	if 1 < len(all_vars_list):
		return generate_full_cnf(cnf_df, [fact], all_vars_list)
	return set([0])
	# return full_rule_cnf

def build_cnf(data):
	all_vars_list = list(data['events'])
	# full_cnf = pd.DataFrame(columns=all_vars_list)
	# print("RULES PART")
	full_cnf = set()
	for rule in data['rpn_rules']:
		full_rule_cnf = process_rule(rule, all_vars_list, data)
		full_cnf.update(full_rule_cnf)
		# full_cnf = pd.concat([full_cnf, full_rule_cnf], ignore_index=True)
	# print("FACTS PART")
	
	for fact in data['facts']:
		# print(fact)
		full_fact_cnf = process_fact(fact, all_vars_list, data)
		full_cnf.update(full_fact_cnf)
		# print("full_rule_cnf")
		# print(full_fact_cnf)
		# full_cnf = pd.concat([full_cnf, full_fact_cnf], ignore_index=True)
	print(full_cnf)
	exit()
	full_cnf = full_cnf.apply(pd.to_numeric)
	full_cnf.drop_duplicates(inplace=True, ignore_index=True)
	print(full_cnf)
	return full_cnf, all_vars_list

def check_queries(data, full_cnf, all_vars_list):
	result = dict()
	for var in data['queries']:
		full_query_cnf = process_fact(var, all_vars_list, data)
		check_cnf = pd.concat([full_cnf, full_query_cnf], ignore_index=True)
		check_cnf = check_cnf.apply(pd.to_numeric)
		check_cnf.drop_duplicates(inplace=True, ignore_index=True)
		result[var] = (len(full_cnf.index) == len(check_cnf.index))
	return result