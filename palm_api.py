import pprint,sys,re,time,os
import google.generativeai as palm

palm.configure(api_key=os.environ["PALM_API_KEY"])

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

def ask_palm(ques, args):
    prompt = 'There will be a question stem below followed by 4 possible answers - A,B,C,D. Must provide an answer A,B,C,D only. \n '
    qpart = '\n'.join(ques.q)
    prompt += qpart

    for opt in ques.options:
        prompt += '\n'.join(opt)

    print(f'{ques.num=}  {prompt=}')
        
    start = time.time()
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=args.temperature,
        # The maximum length of the response
        max_output_tokens=800,
    )
    end = time.time()
    delta = end - start
    key = ques.key[0].strip()
    print(f'{completion.result=}')
    if completion.result == None:
        palm_answer = None
    else:
        m = re.match(r'\(?(\w)\)?', completion.result)
        if m:
            palm_answer = m.group(1)
        else:
            print(f'{completion.result=} not in expected form')
            sys.exit(1)
    print(f'{key=} {palm_answer=}')
    return key, palm_answer, delta
