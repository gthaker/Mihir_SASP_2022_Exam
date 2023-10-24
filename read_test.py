import re, sys, time, pickle
import argparse, random
# from palm_api import *
from chatgpt_api import *

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--skip', help="skip this question number", type=int, nargs='*')
parser.add_argument('-i', '--input', help='test text input file', required=True)
parser.add_argument('-a', '--answers', help='file containing test answer', required=True)
parser.add_argument('-d', '--debug', help='debug level. an int, default=0', type=int, default=0, required=False)
parser.add_argument('-y', '--year', help='which year input we are processing. An int.', type=int, required=False)
args = parser.parse_args()

if args.skip == None:
    args.skip = []
print('args', args)

from question import Question

p = 1  # line pointer where search will start from
nextq = 0 # will be incremented to 1 before we start (if '1' not in args.skip)

def log(*pargs):
    if not args.debug: return
    print(*pargs)

def update_nextq():
    global nextq
    nextq += 1
    while nextq in args.skip:
        nextq += 1

update_nextq()

fp =  open(args.input)

lines = fp.readlines()
lines = ['index-0:ignore'] + lines # make things 1 based by adding dummy entry at front
nlines = len(lines)
print(f'{nlines=}')

def trim_newlines_at_end(ans):
    if len(ans) == 0 or len(ans) == 1:
        return ans
    count = 0
    ans2 = ans[:]
    ans2.reverse()
    for e in ans2:
        if re.match(r'^\s*$', e):
            count += 1
        else:
            break   # first non-empty line we exit the loop
    if count == 0:
        return ans
    return ans[:-count]

def get_block(starting_re, nre, prev_line_blank=False ):   # nre=next_section_re
    global p
    ans = []
    while p < nlines:
        log(f'lines[{p}]={lines[p]}  {starting_re=} {nre=} {prev_line_blank=}')
        m = re.match(starting_re, lines[p])
        if m and (not prev_line_blank or re.match(r'^\s*$', lines[p-1])):  # we have a match and prev. line was blank
            ans.append(lines[p]) # this line is part of answer
            p += 1
            while p < nlines and not re.match(nre, lines[p]): # any line that does not match 'next_section_re'
                ans.append(lines[p])  # are gathered
                p += 1
            while p < nlines and re.match(r'^\s*$', lines[p]):  # skip all the blank lines that follow our block
                p += 1
            # trim all trailing blank lines from back.
            ans = trim_newlines_at_end(ans)
            log(f' ++  get_block returning {ans=}')
            return ans
        p += 1

discarded_ques = []
all_ques = []

# when we are reading the answer options, this dict tells us the next_section_regex
opt_nre_vals = {'A': r'(?i)B\. ', 'B': r'(?i)C\. ', 'C': r'(?i)D\. ', 'D': r'(?i)E\.', 'E': r'^\d+\. ',
                }

while p < nlines:
    log('===========================================================================')
    nre = r'^A\. '

    q = get_block(r'^\s?%s\. ' % nextq, nre, prev_line_blank=False)   # find block starting with "1. xxx"  "2. yyy" etc
    if q == None:
        log(f'question {nextq=} not read, existing loop.')
        break
    log('1: q', q)
    m = re.match(r'^\s?(\d+)\.\s+(.*)', q[0])  # q is a list, recheck 1st line has "1. xxx"
    if not m:
        print('something wrong, can not find qnum in', q)
        sys.exit(1)
    qnum = int(m.group(1))
    keep_question = True
    q[0] = m.group(2)       # we drop the question num from text we will send to LLMs
    log(' ==', qnum, q)

    opts = []
    opt_list = 'ABCDE'

    for opt in opt_list:
        opts.append(get_block(r'^\s*(?i)%s\.? ' % opt, opt_nre_vals[opt]))
    log(f'{opts=}')

    key, domain, citations, rationale = [None] * 4   # we don't have these fields in this exam.
    # we will get 'key' later, however.
    ques = Question(args.year, qnum, q, opts, key, domain, citations, rationale)
    if keep_question:
        print(ques)
        all_ques.append(ques)
    else:
        discarded_ques.append(ques)
    update_nextq()   # even if we don't keep this question increment the count

print()
print('========= All input has been read ============')
print(f'{len(all_ques)=}')
print(f'{len(discarded_ques)=}')

fname = args.input
if fname.endswith('.txt'):
    fname = fname.split('.', 1)[0]
fname = fname + '.parsed.pickle'
print(f'{fname=}')
with open(fname, 'wb') as fp:
    pickle.dump(all_ques, fp)
