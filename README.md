# Mihir_SASP_2022_Exam

## Prepare an exam for evaluation
To evaluate how various LLMs perform on this exam, the following steps are needed:

1) From .pdf file create a .txt file of the test document.
2) Split the .txt document into two parts, questions and answers. (Note: Some exams have questions and answers intertwined, for these you would have to adjust program read_test.py. See read_test.py in radOnc ACR exams repo for an example.)
3) Generate .pickle file of the test which consists of a list of Question() objects with question text, options for answer, and a 'key'.

To prepare a given test's .pickle file that contains the question, options for the answer (A-E) and answer key, use command such as:

python read_test.py -y 2022  -i exams/text/SASP_2022_V2_cleaned_questions.txt  -a exams/text/SASP_2022_V2_answers.txt -p exams/text/SASP_2022_V2.QA.pickle

## Evaluation a Test
To evaluate the text against a given LLM do:

python run_llm.py  -i exams/text/SASP_2022_V2.QA.pickle  --skip `cat image_questions_list.txt `  --pace 20 > 2023-10-24_gpt-3.5-turbo_results.txt

The file image_questions_list.txt contains questions that have images associated w/ them. For now test are skipped. Please note that in some cases you must pace the rate at which questions are asked of the model by using --pace <sec> argument. Use '-h' to see cmdline options explanation.

## Tabulating Model's Score

After the run is complete, obtain a .csv file of the results summary by:

cat 2023-10-25_gpt-4_results.txt | python process_run_output.py > 2023-10-25_gpt-4_summary.csv

This .csv file can then be used in a Google Sheet to obtain further summarization.
