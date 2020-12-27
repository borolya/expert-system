#bonuses 1) input format

import argparse
import mparser as pars
import sys
import reverse_polish_notation as rev_pn
import cnf


arg_pr = argparse.ArgumentParser(description=' ', add_help=True, conflict_handler='resolve')
arg_pr.add_argument('-f', '--file', action='store', type = str, dest='file_name', help='file name')
arg_pr.add_argument('-n', '--input', action='store_true', dest='input', help='to use input format')

args = arg_pr.parse_args(sys.argv[1::])

if args.file_name == None and args.input != True:
    #print args help
    print("add file or choose input format")
    exit()
if (args.file_name != None):
    try:
        fd = open(args.file_name)
    except IOError as e:
        exit(e)
else:
    fd = sys.stdin

data = pars.get_data(fd)
fd.close()
print (data)
rpn_rules = []
for rule in data["rules"]:
    rpn_rule = rev_pn.rpn(rule)
    print(rpn_rule)
    rpn_rules.append(rpn_rule)
data["rpn_rules"] = rpn_rules
print(data)
full_cnf, events_list = cnf.build_cnf(data)
result = cnf.check_queries(data, full_cnf, events_list)
print(result)