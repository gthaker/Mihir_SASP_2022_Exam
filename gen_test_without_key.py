import re, sys, time, pickle
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help='test text input file', required=True)
parser.add_argument('-d', '--debug', help='debug level. an int, default=0', type=int, default=0, required=False)
args = parser.parse_args()

print('args', args)

from question import Question

def log(*pargs):
    if not args.debug: return
    print(*pargs)

fp =  open(args.input, 'rb')
all_ques = pickle.load(fp)
fp.close()

print(f'{len(all_ques)=}')
print(f'{all_ques[0]=}')

def delx(o, a):
    # delete and attribute but do not complain if attribute was missing
    try:
        delattr(o, a)
    except AttributeError:
        pass
    

for q in all_ques:
    delx(q, 'key')
    delx(q, 'domain')
    delx(q, 'rationale')
    delx(q, 'citations')
    
#print(f'{all_ques[0].__str__(truncated=True)=}')
print(f'{all_ques[0]=}')
sys.exit()
fname = args.input
fname = fname.replace('parsed.', 'parsed.ques_only.')
print(f'{fname=}')

with open(fname, 'wb') as fp:
    pickle.dump(all_ques, fp)

