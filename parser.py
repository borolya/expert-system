import re

#def preparing_string(fd):

def formula_parsing(line):
    formuls = []
    #check this is formula



def get_data(fd):
    while True:
        try:
            line = fd.readline()
            if line == '':
                fd.close()
                break
            line = re.split(r'\s*#|\s*\n', line)[0]
            line = line.strip()
            if len(re.findall(r'[^\D=<>?\(\)+|!^]', line) != 0:
                sys.exit("non correct symbol in line "+ line)
            if line != '':


        except Exception as e:
            sys.exit(e)