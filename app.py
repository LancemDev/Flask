from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import random

app=Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/next', methods=['POST','GET'])
def next():
    size= request.form.get("size")
    if not size:
        return render_template("failure.html")
    return render_template("load.html")

@app.route('/back_failure', methods=['POST','GET'])
def failure_back():
    return redirect(url_for('index'))

@app.route('/process-csv', methods=['POST','GET'])
def process_csv():
    csv_data=request.data

    """getting my random group code in here

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    # Read in the data from a CSV file
    df = pd.read_csv(csv_data)

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into 8 equally-sized groups
    group_size = len(df) // 8
    groups = [df[i:i+group_size] for i in range(0, len(df), group_size)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by 8
    groups[-1] = groups[-1].append(df[len(df)-len(groups[-1]):])

    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["group"] = i+1

    # Concatenate the groups back into a single DataFrame and save the result to a CSV file
    result = pd.concat(groups)
    final_result=result.to_csv("result.csv", index=False)

    return final_result

if __name__ == '__main__':
    app.run(debug=True)