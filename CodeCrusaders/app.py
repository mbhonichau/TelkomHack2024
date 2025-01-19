from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import logging
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define scenarios with careers and levels
scenarios = {
    "Software Developer": [
        {
            "description": "A web application crashes when users submit forms. Write a function to log errors and notify admins.",
            "expected_function": "log_error"
        }
    ],
    "Data Analyst": [
        {
            "description": "You need to generate a report from a CSV file containing sales data. Write a script to analyze total sales per product.",
            "expected_function": "analyze_sales"
        }
    ],
    # Add more careers and scenarios as needed...
}

@app.route('/')
def index():
    return render_template('index.html', careers=scenarios.keys())

@app.route('/exam', methods=['POST'])
def exam():
    career = request.form['career']
    level = request.form['level']
    
    # Start the exam in a separate script
    subprocess.Popen(['python', 'exam_lock.py', career, level])
    
    # Return a response to the user
    return render_template('exam_start.html', career=career)

@app.route('/submit', methods=['POST'])
def submit():
    user_code = request.form['user_code']
    scenario_index = int(request.form['scenario_index'])
    career = request.form['career']

    if assess_code(user_code, scenarios[career][scenario_index]['expected_function']):
        flash('Your code passed the assessment!', 'success')
    else:
        flash('Your code did not pass. Please review it.', 'danger')

    return redirect(url_for('exam', career=career))

def assess_code(user_code, expected_function):
    try:
        local_dict = {}
        exec(user_code, {}, local_dict)

        if expected_function in local_dict:
            if expected_function == "log_error":
                local_dict[expected_function]("Test error")
                return True
            elif expected_function == "analyze_sales":
                result = local_dict[expected_function]("sales_data.csv")
                return isinstance(result, pd.Series)
        return False
    except Exception as e:
        logging.error(f"Error in user code: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
