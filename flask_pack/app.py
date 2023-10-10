from flask import Flask, render_template, redirect, url_for
import csv
from flask import request
import datetime
from utils import *
import os
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec'
csv_path = 'tasks.csv'
OPENAI_API_KEY = os.environ.get('api_key')
api_key = OPENAI_API_KEY

def read_csv(csv_path):
    data = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def index():
    data = read_csv(csv_path)
    return render_template('index.html', data=data)

@app.route('/update')
def update_page():
    return render_template('update.html')


@app.route('/update_status', methods=['POST'])
def update_status():
    csv_df = pd.read_csv(csv_path)
    task_number = request.form.get('task_number')
    spent_budget = request.form.get('budget')
    date = datetime.date.today()
    original_budget = csv_df.iloc[(int(task_number)-1),1]
    starting_date = csv_df.iloc[(int(task_number)-1),3]
    deadline_date = csv_df.iloc[(int(task_number)-1),4]
    task_number, status, response = ask_ai(csv_path, api_key, task_number, original_budget, spent_budget, starting_date, deadline_date, date)
    update_status_and_budget_in_csv(task_number, new_status=status, csv_file=csv_path, spent_budget=spent_budget, recommendation=response.split(",")[1])
    return redirect(url_for('index'))

#run
if __name__ == '__main__':
    app.run(debug=False)
