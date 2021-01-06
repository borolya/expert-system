#bonuses 1) input format

import argparse
import mparser as pars
import sys
import reverse_polish_notation as rev_pn
import cnf
import time

def main(filename):
    #start_time = time.time()
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
    false_prior = set()
    non_prior = set()

    for rule in data["rules"]:
        rpn_rule, fl_pr, non_fl_pr = rev_pn.rpn(rule)
        #print(rpn_rule)
        rpn_rules.append(rpn_rule)
        if fl_pr != None:
            false_prior.update(fl_pr)
            non_prior.update(non_fl_pr)
        #false_prior.discard(set(non_fl_pr))
    data["rpn_rules"] = rpn_rules
    data["false_event_priority"] = false_prior.difference(non_prior)
    #print(data)
    # full_cnf, events_list = 
    #print("START TASK")
    result = cnf.analyze_problem(data)
    # result = cnf.check_queries(data, full_cnf, events_list)
    # print(result)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return result

if __name__ == '__main__':
    main(None)