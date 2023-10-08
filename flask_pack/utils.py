from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



def load_and_format_file(csv_file):
    '''
    - Takes in a csv file and creates file_content list object of the lines in the csv file
    - Returns a single string of concatenated elemnts in file_contents
    '''
    with open(csv_file, "r") as file:
        file_contents = file.readlines()
    return ''.join(file_contents)


def load_openai_llm(api_key, model="gpt-3.5-turbo-instruct-0914", temperature=0.4):
    llm = OpenAI(openai_api_key=api_key, model=model, temperature=temperature)
    return llm


def ask_ai(csv_file, api_key, task_number, budget, date):
    formatted_file_contents = load_and_format_file(csv_file)
    llm = load_openai_llm(api_key)

    prompt = PromptTemplate(
        input_variables=["budget", "date", "task_number"],
        template=f"""You are given this file

    {formatted_file_contents},

    For task number {{task_number}}, the budget total budget invested is currently {{budget}}, and we are {{date}}.

    Return a RAG color and the justification in this format [COLOR, REASON] for task {{task_number}}.

    """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({
        'budget': budget,
        'date': date,
        'task_number': task_number,
    })

    status = response.split(",")[0].strip().lower()
    status = status.replace("[", "").replace("]", "").strip()

    return task_number, status, response

def update_status_in_csv(task_number, new_status, csv_file):
    valid_statuses = ["r", "red", "g", "green", "a", "amber", "o", "orange"]

    if new_status not in valid_statuses:
        return

    with open(csv_file, "r") as file:
        rows = file.readlines()

    header = rows[0].strip().split(',')
    status_index = header.index('Status')

    for index, row in enumerate(rows):
        row_elements = row.strip().split(',')
        if row_elements[0] == str(task_number):
            row_elements[status_index] = new_status
            rows[index] = ",".join(row_elements) + "\n"

    with open(csv_file, "w") as file:
        file.writelines(rows)
