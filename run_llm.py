#!/usr/bin/env python

import re, sys, time, pickle
import argparse, random
from palm_api import *
#from chatgpt_api import *
#from llama_2_api import *

parser = argparse.ArgumentParser(description='A program to read an exam\'s .pickle file and call various LLM API for all or subset of exam questions as specified by commandline args. Many cloud LLM servers meter the rate at which calls can be made to the API. Use --pace option to slow down the calls.')

parser.add_argument('-s', '--skip', help="skip this question number", type=int, nargs='*', default=[])
parser.add_argument('--only', help="only do these numbered questions", type=int, nargs='*',default=[])
parser.add_argument('-i', '--input', help='test text input file', required=True)
parser.add_argument('-d', '--debug', help='debug level. an int, default=0', type=int, default=0, required=False)
parser.add_argument('-l', '--limit', help='stop after these many questions (default=0, do all)', type=int, default=0, required=False)
parser.add_argument('--pace', help='how many seconds to wait between each invocation. (default=0)', type=int, default=0, required=False)
parser.add_argument('--temperature', help='"temperature" parameter to provide to the LLM api call. (default=0.0)', type=float, default=0.0, required=False)
parser.add_argument('--test', help='only read the test file and do all processing except actually calling the LLM API. Randomly pick an answer from [A, B, C, D].', action='store_true', required=False)
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

# init the currect and wrong answer counts
qcount = sum_c = sum_w = no_answer_count = 0
last_qnum = None  # no previous question seen
qnums_skipped = list()  # which ques.num  were not considered
for ques in all_ques:
    if len(args.only) > 0 and ques.num not in args.only:
        continue
    if len(args.skip) > 0 and ques.num in args.skip:
        continue

    if args.test:
        key, answer = ques.key, random.sample( ['A', 'B', 'C', 'D', 'E'], k = 1 )[0]
        delta = 0
        print(f'test_mode answer_is_random: {ques.num=} {key=} {answer=}')
    else:
        #key, answer, delta = do_openai_call(ques)
        key, answer, delta = ask_palm(ques, args)
        #key, answer, delta = ask_llama_2(ques)
    if answer == None:
        no_answer_count += 1
    result = answer != None and answer in key
    if result:
        sum_c += 1
    else:
        sum_w += 1
    qcount += 1
    print(f'{qcount=}  {ques.num=}  {delta=} {result=}  {sum_c=}  {sum_w=}  fraction_correct={float(sum_c)/(sum_c + sum_w)}')
    print('=================================', flush=True)
    if last_qnum != None:
        if ques.num != last_qnum + 1:
            qnums_skipped += list(range(last_qnum+1, ques.num))
    last_qnum = ques.num
    if args.limit > 0 and qcount >= args.limit:
        break
    if args.pace > 0: time.sleep(random.randint(args.pace, 2*args.pace))

print(f'{no_answer_count=}')
print(f'{len(qnums_skipped)=} {qnums_skipped=}')
