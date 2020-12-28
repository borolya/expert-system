import os
import json
from glob import glob
from parse_file import parse_file
from global_graph import Fact
from expert_system import expert_system


DO_PRINT = True
PATH = './samples/check_list/'
with open('./samples/answers.json', 'r') as f:
    dict_answers = json.load(f)

for filename in glob(PATH + "**/**", recursive=True):
    if os.path.isfile(filename):
        try:
            list_rules, init_facts, query = parse_file(filename)
            result = expert_system(list_rules, init_facts, query)
        except SystemExit:
            result = {}
        answer = dict_answers.get(filename, {})
        check = answer == result
        Fact.dict_facts = {}
        Fact.check_contradiction = False
        print(filename, check)
        if DO_PRINT:
            print("result process: ", result)
            print("right answer  : ", answer)
        if not check:
            print('ERROR')
            exit()
