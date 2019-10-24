def fix(filename):
    new = []
    with open(filename) as f:
        content = f.readlines()
        
        for line in content:
            if '\\xff\\x0b' in line:
                new.append(line.replace('\\xff\\x0b','**************,'))
                
            else:
                new.append(line)

    with open(filename+'_fixed_.txt','w') as f:
        for l in new:
            print(l,file=f)
            

for i in range(1,5):
    fix('res-%d.txt'%i)
