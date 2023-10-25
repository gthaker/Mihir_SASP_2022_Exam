# Mihir_SASP_2022_Exam

To evaluate how various LLMs perform on this exam.

To prepare a given test's .pickle file that contains the question, options for the answer (A-E) and answer key, use command such as:

python read_test.py -y 2022  -i exams/text/SASP_2022_V2_cleaned_questions.txt  -a exams/text/SASP_2022_V2_answers.txt -p exams/text/SASP_2022_V2.QA.pickle

To evaluate the text against a given LLM do:

python run_llm.py  -i exams/text/SASP_2022_V2.QA.pickle  --skip `cat image_questions_list.txt `  --pace 20 > 2023-10-24_gpt-3.5-turbo_results.txt

The file image_questions_list.txt contains questions that have images associated w/ them. For now test are skipped.
