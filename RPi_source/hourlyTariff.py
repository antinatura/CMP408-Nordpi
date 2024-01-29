"""
Name: hourlyTariff.py
Desc: changes LED hourly based on tariff label
Auth: Ance Strazdina
Date: 11/12/2023
"""

# imports
import sys, datetime
import pandas as pd
import RPi.GPIO as GPIO

# led pins
ledG = 24
ledA = 18
ledR = 14

# gpio setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledG, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(ledA, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(ledR, GPIO.OUT, initial = GPIO.LOW)

def main():
    try:
        # read in the csv with daily tariffs, set Time column as index
        df = pd.read_csv('elspot.csv') # or tariff.csv
    except FileNotFoundError:
        sys.exit("Couldn't find elspot.csv.")
    
    df.set_index('Time', inplace=True)

    now = datetime.datetime.now(datetime.timezone.utc) # get current date and time

    # get row and column to use based on current date and time
    col = df.columns[df.columns.get_loc(now.strftime('%d.%m')) + 1] # tariff label column to use (the column next to date column)
    row = now.strftime('%H') + " - " + (now + datetime.timedelta(hours=1)).strftime('%H') # represents current hour interval as "[current hour] - [next hour]"
    label = df.loc[row][col] # get label for the current hour interval

    # print("Tariff on " + now.strftime('%d.%m') + " during " + row + " is: " + label)
    
    # light a led based on label
    if label == 'G':
        GPIO.output(ledG, GPIO.HIGH)
    elif label == 'A':
        GPIO.output(ledA, GPIO.HIGH)
    elif label == 'R':
        GPIO.output(ledR, GPIO.HIGH)

# call main
if __name__ == '__main__':
    main()
