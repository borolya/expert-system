#bonuses :
    # input format
    # the rule without aplicaton
    # right side of implication 
    # add !A to facts

import argparse
import mparser as pars
import sys
import reverse_polish_notation as rev_pn
import cnf
import time

def main(filename):
    start = time.time()
    if filename == None:
        arg_pr = argparse.ArgumentParser(description=' ', add_help=True, conflict_handler='resolve')
        arg_pr.add_argument('-f', '--file', action='store', type = str, dest='file_name', help='to use file name format')
        arg_pr.add_argument('-n', '--input', action='store_true', dest='input', help='to use input format and stop it by cntr+D')

        args = arg_pr.parse_args(sys.argv[1::])
        if args.file_name == None and args.input != True:
            arg_pr.print_help()
        elif args.file_name != None:
            filename = args.file_name
        else:
            filename = 0
    
    try:
        fd = open(filename)
    except IOError as e:
        exit(e)

    data = pars.get_data(fd)
    fd.close()
    
    rpn_rules = []
    left_side = set()
    right_side = set()

    for rule in data["rules"]:
        rpn_rule, l, r = rev_pn.rpn(rule)
        rpn_rules.append(rpn_rule)
        left_side.update(l)
        right_side.update(r)
    data["rpn_rules"] = rpn_rules
    data["left_side"] = left_side
    data["right_side"] = right_side

    result = cnf.analyze_problem(data)
    for q in data["unknown_queries"]:
        print(str(q) + " is False")

    result = {key: result[key] for key in result.keys() if key in data['queries']} #then del
    true_result = data['queries'].intersection(data["facts"]) #then del
    for i in true_result: #then del
        result[i] = True #then del
    for i in data["unknown_queries"]:
        result[i] = False #then del
    print("second", time.time() - start)
    return result #then del

if __name__ == '__main__':
    main(None)
