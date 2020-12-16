#bonuses 1) input format

import argparser

arg_pr = argparse.ArgumentParser(description=' ', add_help=True, conflict_handler='resolve')
parser.add_argument('-f', '--file', action='store', type = str, dest='file_name', help='file name')
parser.add_argument('-n', '--input', action='store_true', dest='input', help='to use input format')

args = parser.parser_args(sys.argv[1::])

if args.file_name == None and args.input != True:
    #print args help
    print("add file or choose input format")
    exit()


if (args.file_name != None):
    try:
        fd = open(args.file_name)
    except IOError as e:
        sys.exit(e)
    else:
        fd = sys.stdin
fd.close()


