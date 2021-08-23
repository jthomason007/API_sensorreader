#!/usr/bin/env python
# coding: utf-8

# In[48]:


import matplotlib.pyplot as plt
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import pandas as pd
from pandas import DataFrame as df

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams["figure.figsize"] = [10,6]
delta = datetime.timedelta(
days = 7)

#Prints out json objects for easy viewing
def jprint(obj):
    print(json.dumps(obj, sort_keys=True, indent=4))

#Time given in as unix timestamp, this converts it for interpretation
def epochconvert(time):
    z = ['']
    for i in time:
        if len(z[0]) == 10:
            pass
        elif i.isdigit():
            z[0] = z[0]+i
    
    y = int(z[0])
    x = datetime.datetime.fromtimestamp(y).strftime('%m-%d-%Y %H:%M:%S')
    return x

#Enter in login info and API keys
user = 
password = 
APIKeyID = 
APISecretKey = 
sensorID



dates = []
states = []
names = []
parameters = {'sensorID': sensorID}
headers = {'APIKeyID': APIKeyID,
          'APISecretKey': APISecretKey}


#Pings website
response = requests.get("https://www.imonnit.com/json/SensorGet", params = parameters, auth = (user,password), headers = headers)
if response.status_code == 200:
    print('!Successful Connection!')
          
else:
    print('!Connection Error!')

# jprint(response.json())
print('Sensor Name:', response.json()['Result']['SensorName'])
names = 'Sensor Name:', response.json()['Result']['SensorName']
print('Battery Percentage:', response.json()['Result']['BatteryLevel'])
print('Current Status:', response.json()['Result']['CurrentReading'])

# parameters for passing into methods
parameters = {'sensorID': 388778,
              'fromDate': '07/16/21',
             'toDate': '07/23/21'}

data = requests.get("https://www.imonnit.com/json/SensorDataMessages", params = parameters, auth = (user,password), headers = headers)
# jprint(data.json())
results = data.json()['Result']
for i in range(len(results)):
    dates.append(epochconvert(results[i]['MessageDate']))
    states.append(results[i]['DisplayData'])

excel_dates = []
excel_states = []
excel_sensors = []
pour_time = []

#Formatting data to be exported into an excel sheet.
for i in range(len(states)):
    if states[i] == 'Closed':
        time = (datetime.datetime.strptime(dates[i-1],'%m-%d-%Y %H:%M:%S')-datetime.datetime.strptime(dates[i],'%m-%d-%Y %H:%M:%S'))
        pour_time.append(time)
        excel_dates.append(datetime.datetime.strptime(dates[i], '%m-%d-%Y %H:%M:%S'))
        excel_sensors.append(names)

sensor_list = [excel_sensors, excel_dates, pour_time]
sensor_data = df(sensor_list).transpose()
sensor_data.columns = ['Names', 'Date and Start Time', 'Pour Times']
sensor_data.columns = ['Date', 'Pour Times']
sensor_data.to_excel(r'C:/Innovative Ink/Beer Tap/Sensor Data/test.xlsx', index = False)


#Prelimary data plotting
sensor_data.plot.bar("Date and Start Time","Pour Times")
ounces = sensor_data['Pour Times'][1]
for i in range(len(pour_time)-1):
    ounces = ounces + sensor_data['Pour Times'][i +1]
poured = int(ounces.total_seconds())/2
print(f"{names[1]} poured {poured} ounces.")

