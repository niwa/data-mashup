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
URL=''

def main():
    # Request data from NIWAData
    response = get(URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    # Successful requests will return HTTP status code 200
    if response.status_code != 200:
        raise Exception('Failed to request NIWAData: %s' % response.reason)

    # Parse the JSON response
    data = response.json()
    
    # You can retrieve the attributes about the dataset,
    analysis_time = data['data']['analysisTime']
    measure_mame = data['data']['measureName']
    name = data['data']['name']
    unit_symbol = data['data']['unitSymbol']
    # and also the values
    values = data['data']['values']
    pprint(data)

    # Plot the values, where x[0] has the datetime, and x[1] the current float value
    # Note that we are sorting the values by datetime, as they may
    # not always come sorted
    dates =  np.array([datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S%z') for x in sorted(values.items())])
    values = np.array([x[1] for x in sorted(values.items())])

    plt.plot_date(x=dates, y=values, fmt="r-")
    plt.title(name)
    plt.ylabel("Value in %s" % unit_symbol)
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
