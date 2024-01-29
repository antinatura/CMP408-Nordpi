"""
Name: elspot.py
Desc: gets Nordpool hourly spot prices for today and tomorrow in Latvia, saves to a CSV, and labels hourly tariffs based on their value.
Auth: Ance Strazdina
Date: 10/12/2023
"""

# imports
from nordpool import elspot
from requests.exceptions import ConnectionError
import datetime, os.path, csv, sys, subprocess
import pandas as pd

area = 'LV' # area to get spot prices for
# this script gets data for Latvia, however, the rest of the Baltic States have the same tariffs

# label tariffs as affordable, OK, expensive based on price distribution
def label(c, n):
    df = pd.read_csv('elspot.csv')
    
    # read in todays prices, caluclate quartiles, and label hourly tariffs
    prices = df[c['end'].strftime('%d.%m')]
    q1, q3 = prices.quantile([0.25, 0.75])
    df['label' + str(len(df.columns)-2)] = pd.cut(prices, bins=[float('-inf'), q1, q3, float('inf')], labels=['G', 'A', 'R'])

    # read in tomorrows prices, caluclate quartiles, and label hourly tariffs
    prices = df[n['end'].strftime('%d.%m')]
    q1, q3 = prices.quantile([0.25, 0.75])
    df['label' + str(len(df.columns)-2)] = pd.cut(prices, bins=[float('-inf'), q1, q3, float('inf')], labels=['G', 'A', 'R'])

    """
    R(ed) - Expensive
    A(mber) - OK
    G(reen) - Affordable
    """

    # reorder columns and save
    col = df.pop('label1')
    df.insert(2, col.name, col)
    df.to_csv('elspot.csv', index=False)

# write spot prices to csv
def writedata(c, n):
    # overwrite the existing file (if one exists)
    if os.path.isfile('elspot.csv'):
        f = open('elspot.csv', "w+")
        f.close()

    # add column labels 
    with open('elspot.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            row = ['Time', c['end'].strftime('%d.%m'), n['end'].strftime('%d.%m')] # Time, [todays date], [tomorrows date]
            writer.writerow(row)

    # write spot prices to csv
    for x in c['areas']['LV']['values']:
        with open('elspot.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # [current hour] - [next hour], todays tariff, tommorows tariff. tariffs in kWh rounded to 3 decimal points.
            row = [x['start'].strftime('%H') + " - " + x['end'].strftime('%H'), round(x['value']/1000, 3), round(n['areas']['LV']['values'][c['areas']['LV']['values'].index(x)]['value']/1000, 3)]
            writer.writerow(row)

# main function
def main():
    # get spot prices for today and tomorrow
    # dates in 'yyyy-mm-dd' format
    try:
        if datetime.datetime.now(datetime.timezone.utc).time() >= datetime.time(11, 50):
            current_day = elspot.Prices().hourly(end_date=datetime.datetime.now(datetime.timezone.utc).date(), areas=[area])
            next_day = elspot.Prices().hourly(end_date=datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days=1), areas=[area])
        else:
            # if its too early to get data for tommorow: current day = previous day; next day = current day
            current_day = elspot.Prices().hourly(end_date=datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days=-1), areas=[area])
            next_day = elspot.Prices().hourly(end_date=datetime.datetime.now(datetime.timezone.utc).date(), areas=[area])
    except ConnectionError:
        sys.exit("No connection.") 
    
    if current_day['areas']['LV']['Average'] == float('inf') or next_day['areas']['LV']['Average'] == float('inf'):
        sys.exit("Cannot get data right now.") 

    writedata(current_day, next_day) # write data to a csv
    label(current_day, next_day) # label tariffs based on their value
    
    # trigger mqtt
    subprocess.run(['python3', 'mqtt_publisher.py'])

# call main
if __name__ == '__main__':
    main()
