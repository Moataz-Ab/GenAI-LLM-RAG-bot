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
    '''
    - Creates OpenAI model
    '''
    llm = OpenAI(openai_api_key=api_key, model=model, temperature=temperature)
    return llm

def ask_ai(csv_file, api_key, task_number, original_budget, spent_budget, starting_date, deadline_date, date):
    '''
    - Takes in csv and farmats it into a single string
    - Creates an OpenAI model
    - Propts the model to return task status color and recommendations
    - Returns the task number, status color, and recommendation response
    '''
    formatted_file_contents = load_and_format_file(csv_file)
    llm = load_openai_llm(api_key)

    prompt = PromptTemplate(
        input_variables=["original_budget", "spent_budget", "starting_date", "deadline_date", "task_number", "date"],
        template=f"""You are an expert in project management. you are given this file which contains data of tasks in a project {formatted_file_contents} For task number {{task_number}}, the original budget allocated for the task is {{original_budget}}. From this amount we have so far spent {{spent_budget}}, the task starting date is {{starting_date}}, and task deadline is {{deadline_date}}. Today is {{date}}. Use your understanding of project management to return a RAG color representing the task status and a recommendation in this format [COLOR, Recommendation] for task {{task_number}}. Your recommendation must include 3 expert exdvices about three important aspects of current status of the task number {{task_number}}
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({
        'original_budget' : original_budget,
        'spent_budget' : spent_budget,
        'starting_date' : starting_date,
        'deadline_date' : deadline_date,
        'task_number': task_number,
        'date' : date
    })

    status = response.split(",")[0].strip().lower()
    status = status.replace("[", "").replace("]", "").strip()

    return task_number, status, response

def update_status_and_budget_in_csv(task_number, new_status, spent_budget, csv_file, recommendation):
    '''
    - Takes in the csv file, task number, the spent budget, the new status and recommendation from the model
    - Locates the status datapoint of the selected task and updates the status
    - Adds the task recommendation in the recommendation column
    '''

    valid_statuses = ["r", "red", "g", "green", "a", "amber", "o", "orange"]

    if new_status not in valid_statuses:
        return

    with open(csv_file, "r", newline='', encoding='utf-8') as file:
        rows = file.readlines()

    header = rows[0].strip().split(';')  # Change from ',' to ';'
    status_index = header.index('Status')
    budget_index = header.index('Spent budget')

    # Check if the recommendation column exists, if not, add it
    if 'Recommendation' not in header:
        header.append('Recommendation')
        rows[0] = ";".join(header) + "\n"

    recommendation_index = header.index('Recommendation')

    for index, row in enumerate(rows):
        row_elements = row.strip().split(';')
        if row_elements[0] == str(task_number):
            row_elements[status_index] = new_status
            row_elements[budget_index] = str(spent_budget)
            # Check if row already has recommendation column data, if not, add a placeholder
            if len(row_elements) <= recommendation_index:
                row_elements.append("")
            formatted_recommendation = f'[{new_status}, "{recommendation.strip()}"]'
            row_elements[recommendation_index] = formatted_recommendation
            rows[index] = ";".join(row_elements) + "\n"  # ensure newline at end of row

    with open(csv_file, "w", newline='', encoding='utf-8') as file:
        file.writelines(rows)
