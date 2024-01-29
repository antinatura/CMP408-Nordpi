"""
Name: flask_app.py
Desc: read in CSV data and render index page with a html table
Auth: Ance Strazdina
Date: 11/12/2023
"""

# imports
import csv
from flask import Flask, render_template 

app = Flask(__name__) 

@app.route('/') 
def index():
    # read in csv with data and render site
    with open('elspot.csv') as file:
        reader = csv.reader(file)
        header = next(reader)
        return render_template('index.html', header=header, rows=reader)

if __name__ == "__main__": 
	app.run() 