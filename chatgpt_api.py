import openai
import os, time, re

print_model = True

def get_completion(prompt, model="gpt-4"):
    global print_model
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    if print_model:
        print('response.model', response.model)
        print_model = False
    return response.choices[0].message["content"]

def do_openai_call(ques):
    qpart = '\n'.join(ques.q)
    prompt = f"""

Only return the answer A, B, C, D or E in response to the prompt below

{qpart}

"""
    for opt in ques.options:
        prompt += '\n'.join(opt)

    print(f'{ques.num=}  {prompt=}')
    key = ques.key
        
    num_tries = 0
    success = False
    while not success and num_tries < 10:
        start = time.time()
        try:
            response = get_completion(prompt)
        except Exception as e:
            print('exception %s' % e)
            num_tries += 1
            print('num_tries', num_tries, ' Will retry after waiting 600 sec')
            time.sleep(600)   # wait 10 minutes and retry
            continue
        end = time.time()
        delta = end - start
        success = True

    m = re.match(r'\(?(\w)\)?', response)
    if m:
        openai_answer = m.group(1)
    else:
        print(f'{response=} not in expected form')
        sys.exit(1)

    print(f'{key=} {response=} {delta=}')
    return key, openai_answer, delta


