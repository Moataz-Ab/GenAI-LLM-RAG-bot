from flask import Flask, render_template, redirect, url_for
import csv
from flask import request
import datetime
from utils import *
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec'
csv_path = 'tasks.csv'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
api_key = OPENAI_API_KEY

def read_csv(csv_path):
    data = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/') #calling index home url
def index():
    data = read_csv(csv_path)
    return render_template('index.html', data=data)

@app.route('/update') #calling update url
def update_page():
    return render_template('update.html')

<<<<<<< HEAD

@app.route('/update_status', methods=['POST']) #retrieving user input from update url
=======
#comment
@app.route('/update_status', methods=['POST'])
>>>>>>> 4653cd42aab69d2462f2ef509e891701e3b0ee83
def update_status():
    task_number = request.form.get('task_number')
    budget = request.form.get('budget')
    date = datetime.date.today()
    task_number, status, response = ask_ai(csv_path, api_key, task_number, budget, date)
<<<<<<< HEAD
    update_status_in_csv(task_number, new_status=status, csv_file=csv_path)


    return redirect(url_for('index')) #sending back the user to home index page
=======
    update_status_and_budget_in_csv(task_number, new_status=status, csv_file=csv_path, new_budget=budget, recommendation=response.split(",")[1])
    return redirect(url_for('index'))
>>>>>>> 4653cd42aab69d2462f2ef509e891701e3b0ee83


if __name__ == '__main__':
    app.run(debug=False)
