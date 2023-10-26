import pprint,sys,re,time
import replicate


# model = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
#"model = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
# model = "meta/llama-2-70b:a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00",
model = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"

print_model = True

def ask_llama_2(ques):
    global print_model

    if print_model:
        print('model', model)
        print_model = False

    qpart = '\n'.join(ques.q)

    options_part = ''
    for opt in ques.options:
        options_part += '\n'.join(opt)

    prompt = f"""{qpart}

    {options_part}
    """


    print(f'{ques.num=}  {prompt=}')

    start = time.time()
    output = replicate.run(
        model,
        input={"prompt": prompt,
               "system_prompt": 'Act as if you are taking an exam. Select which answer A, B, C, D or E is the correct answer in the prompt below. Only respond with a single letter A, B, C, D or E and provide no explanation.'

               }
    )
    end = time.time()

    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    answer = ''
    for item in output:
        answer += item
        print(item, end='')
    print()

    delta = end - start
    key = ques.key[0].strip()
    #print(f'{answer=}')
    if answer == '':
        llama_answer = None
    else:
        m = re.match(r'\s*\(?(\w)\)?', answer)
        if m:
            llama_answer = m.group(1)
        else:
            print(f'{answer=} not in expected form')
            llama_answer = answer
    print(f'{key=} {llama_answer=}')
    return key, llama_answer, delta
