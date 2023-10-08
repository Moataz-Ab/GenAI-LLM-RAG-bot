from flask import Flask, render_template, redirect, url_for
import csv
from flask import request
import datetime
from utils import *
import os

app = Flask(__name__)
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
    task_number = request.form.get('task_number')
    budget = request.form.get('budget')
    date = datetime.date.today()
    task_number, status, response = ask_ai(csv_path, api_key, task_number, budget, date)
    update_status_in_csv(task_number, new_status=status, csv_file=csv_path)


    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)