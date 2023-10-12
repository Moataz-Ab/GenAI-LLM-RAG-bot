from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd


def load_openai_llm(api_key, model="gpt-3.5-turbo-instruct-0914", temperature=0.4):
    '''
    Initialize and load the OpenAI language model for processing requests.

    Parameters:
        api_key (str): API key for accessing the OpenAI language model.
        model: The OpenAI model.
        temperature (float): controls the randomness of the model's output. min-max is 0.0-1.0.

    Returns:
        An instance of the OpenAI language model ready for use.
    '''
    llm = OpenAI(openai_api_key=api_key, model=model, temperature=temperature)
    return llm

def ask_ai(api_key, task_number, original_budget, spent_budget, starting_date, deadline_date, date):
    '''
    Processes project management data and prompts an OpenAI language model for task RAG status and expert recommendations.

    Parameters:
        api_key (str): API key for accessing the OpenAI language model.
        task_number (int): The identifier of the task. In the csv sample, task_number is 1:5.
        original_budget (float): The original budget allocated for the task.
        spent_budget (float): The amount of budget spent on the task.
        starting_date (str): The starting date of the task.
        deadline_date (str): The deadline date for completing the task.
        date (str): Today's date.

    Returns:
        A tuple containing task number, status RAG color, and the AI expert recommendation response.
    '''
    llm = load_openai_llm(api_key)

    prompt = PromptTemplate(
        input_variables=['original_budget', 'spent_budget', 'starting_date', 'deadline_date', 'task_number', 'date'],

        template=f'''You are an expert in project management.
        For task number {{task_number}}, the original budget allocated for the task is {{original_budget}}.
        From this amount we have so far spent {{spent_budget}}, the task starting date is {{starting_date}},
        and task deadline is {{deadline_date}}. Today is {{date}}. Use your understanding of project
        management to return a
        RAG color representing the task status and a recommendation for task {{task_number}}.
        Your recommendation must include 3 expert exdvices about three important aspects of current
        status of the task number {{task_number}}.
        IMPROTANT: RETURN in this format [COLOR, Recommendations].
        '''
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

    print(f'askai chain response: {response}')
    status = response.split(",")[0].strip().lower()
    status = status.replace("[", "").replace("]", "").strip()

    return task_number, status, response


def update_status_and_budget_in_csv(task_number, new_status, spent_budget, csv_file, recommendation):
    '''
    Updates the task RAG status, spent budget, and AI recommendation in a CSV file corresponding to a specific task number.

    Parameters:
        task_number (int): The identifier of the task. In the csv sample, task_number is 1:5.
        new_status (str): The new status of the task. Should be one of those elements ["r", "red", "g", "green", "a", "amber"].
        spent_budget (float): The amount of budget spent on the task.
        csv_file (str): The path to the CSV file containing project information.
        recommendation (str): AI expert recommendation according to the task status.

    Returns:
        None: The function updates the CSV file in place.
    '''
    valid_statuses = ['r', 'red', 'g', 'green', 'a', 'amber']
    print(task_number, spent_budget, recommendation)
    if new_status not in valid_statuses:
        print(new_status)
        return

    df = pd.read_csv(csv_file, sep=';', encoding='utf-8')

    if 'Recommendation' not in df.columns:
        df['Recommendation'] = ""

    task_number = int(task_number)-1

    if 0 <= task_number < len(df):
        df.loc[task_number, 'Status'] = new_status
        df.loc[task_number, 'Spent budget'] = spent_budget
        formatted_recommendation = f'{recommendation.strip().split(",", 1)[1].replace("]", "")}'
        df.loc[task_number, 'Recommendation'] = formatted_recommendation

        df.to_csv('tasks.csv', sep=';', index=False, encoding='utf-8')

    else:
        print(f'No task found with task number: {task_number}')
