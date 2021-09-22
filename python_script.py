#!/usr/bin/env python

# requests library to download and authenticate
from requests.auth import HTTPBasicAuth
from requests import get
# matplotlib and numpy to plot the timeseries
import matplotlib.pyplot as plt
import numpy as np
# datetime for date and time handling
from datetime import datetime
# pprint to pretty-print values to the console
from pprint import pprint

# You should probably use command line parameters, dotEnv files,
# or another approach, instead of hard-coding values in your
# script.
USERNAME=''
PASSWORD=''
# example URL https://mintaka.niwa.co.nz/rest/api/V1.1/products/geo/data/1/30277/159396797?startDate=2021-09-01T00:00:00Z&endDate=2021-09-30T00:00:00Z
URL=''

def main():
    # Request data from NIWAData
    response = get(URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    # Successful requests will return HTTP status code 200
    if response.status_code != 200:
        raise Exception('Failed to request EcoConnect: %s' % response.reason)

    # Parse the JSON response
    data = response.json()
    pprint(data)
    
    # You can retrieve the attributes about the dataset,
    start_date = data['startDate']
    product_class = data['productClass']
    name = data['name']
    # and also the values
    values = data['data']

    # Assumes timezone is always Z, you should probably parse that
    dates =  np.array([datetime.strptime(x['validityTime'], '%Y-%m-%dT%H:%M:%SZ') for x in values])
    values = np.array([x['value'] for x in values])

    plt.plot_date(x=dates, y=values, fmt="r-")
    plt.title(name)
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
