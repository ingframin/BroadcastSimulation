import re

MSG = re.compile(r'D[0-9]+-.*')
SENT = re.compile(r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+')

received = {}
def cleanup(line):
    return line.replace('(','').replace("'","").replace(')','').replace('b','').replace('\\t',',').replace('\\r\\n','').replace('"','').strip()
    
def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
        
        for l in lines:
            lc = cleanup(l)
            ls = lc.split(',')
            print(ls[1])
            input()
            if MSG.match(ls[1]):
                print(ls[1])
                input()
                
if __name__ == "__main__":
    read_data('res-1.txt')