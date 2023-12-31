import re
import sys

lines = sys.stdin.readlines()

for l in lines:
    #print(l, end='')
    # This one is for openAI API responses
    m = re.match(r'^key=([\'\"]?\w[\'\"]?)\s+response=[\'"]?(\w)', l)
    if m:
        key = m.group(1)
        key = key.replace(' ', '')
        key = key.replace(',', '/')
        key = key.replace("'", '')
        key = key.replace("[", '')
        key = key.replace("]", '')
        
        response = m.group(2)
        #print(key, response)

    # For PaLM
    m = re.match(r'^key=(.+)\s+palm_answer=(\'\w\'|None)', l)
    if m:
        key = m.group(1)
        key = key.replace(' ', '')
        key = key.replace(',', '/')
        key = key.replace("'", '')
        key = key.replace("[", ' ')
        key = key.replace("]", ' ')
        
        response = m.group(2)
        response = response.replace("'", '')
        #print(key, response)

    # For LLAMA-2
    m = re.match(r'^key=(.+)\s+llama_answer=(\'\w\'|None)', l)
    if m:
        key = m.group(1)
        key = key.replace(' ', '')
        key = key.replace(',', '/')
        key = key.replace("'", '')
        key = key.replace("[", ' ')
        key = key.replace("]", ' ')
        
        response = m.group(2)
        response = response.replace("'", '')
        #print(key, response)

    m = re.match(r'^qcount=.*?ques.num=(\d+).*?result=(\w+)', l)
    if m:
        qnum = m.group(1)
        result=m.group(2)
        print('%s,%s,%s,%s' % (qnum, key, response, result))

        
