from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd


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

    llm = load_openai_llm(api_key)

    prompt = PromptTemplate(
        input_variables=["original_budget", "spent_budget", "starting_date", "deadline_date", "task_number", "date"],

        template=f"""You are an expert in project management.
        For task number {{task_number}}, the original budget allocated for the task is {{original_budget}}.
        From this amount we have so far spent {{spent_budget}}, the task starting date is {{starting_date}},
        and task deadline is {{deadline_date}}. Today is {{date}}. Use your understanding of project
        management to return a
        RAG color representing the task status and a recommendation for task {{task_number}}.
        Your recommendation must include 3 expert exdvices about three important aspects of current
        status of the task number {{task_number}}.
        IMPROTANT: RETURN in this format [COLOR, Recommendations].
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
    print(f"askai chain response: {response}")
    status = response.split(",")[0].strip().lower()
    status = status.replace("[", "").replace("]", "").strip()

    return task_number, status, response


def update_status_and_budget_in_csv(task_number, new_status, spent_budget, csv_file, recommendation):
    valid_statuses = ["r", "red", "g", "green", "a", "amber", "o", "orange"]
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

        df.to_csv("tasks.csv", sep=';', index=False, encoding='utf-8')

    else:
        print(f"No task found with task number: {task_number}")
