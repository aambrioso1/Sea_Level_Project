import json, requests, time
# import C:\Users\Alex\PycharmProjects\matplotlib\scatterplot.py

# This is a module that I created to create a scatter plot using matplotlib: 
# 	https://matplotlib.org/index.html
import plot as sp
"""
Example of using the request package for json data from NOAA.
Here are Links to the documentation for these important libraries and the home of JSON.
https://docs.python.org/3/library/json.html
https://docs.python.org/3/library/sys.html
https://pypi.org/project/requests/
http://json.org/
Website with NOAA API information:
https://tidesandcurrents.noaa.gov/api/
"""

"""
Things to do
************
(1) Command line argument for station choice.
(2) Make line graphs for temp/time for all stations.
"""

# Typical URL for the request.
# url = 'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130808 15:00&end_date=20130808 15:06&station=8454000&product=water_temperature&units=english&time_zone=gmt&application=ports_screen&format=json'


TM = time.strftime('%m %d %Y %H %M %S') # TM = 01 06 20 34 07
YEAR = time.strftime('%Y') 
MON = time.strftime('%m')
DAY = time.strftime('%d')
HOUR = time.strftime('%H')
MIN = time.strftime('%M')

# Adjust the start time to one hour before the current time.
def start_hour_day(str_hour, str_day):
	hour = int(str_hour)
	day = int(str_day)
	if hour > 0:
		return [str(hour - 1), str_day]
	else:
		return ['23', str(day - 1)]

start = '20130808 15:00'
end = '20130808 15:06'
start2 = '20200104 14:00'
end2 = '20200104 15:00'

def start_hour(time):
    time_str = str(int(time) - 1)
    if len(time_str) == 1:
        return '0' + time_str
    else:
        return time_str
    
# start3 = YEAR + MON + DAY + ' ' + str(int(HOUR) - 1) + ':' + MIN
start3 = YEAR + MON + DAY + ' ' + start_hour(HOUR) + ':' + MIN
end3 = YEAR + MON + DAY + ' ' + HOUR + ':' + MIN

print('time', start3, end3)

# Stations that around Tampa Bay that have temperature data available.
station1 = '8726520' # St Petersburg
station2 = '8726384' # Port Manatee
station3 = '8726607' # Old Port Tampa Bay
station4 = '8726667' # Mckay Bay Entrance
station5 = '8726724' # Clearwater Beach

STATION = station2 # Pick one of the stations listed above

# Time Zones
zone1 = 'gmt' # Greenwich Mean Time.
zone2 = 'lst'  # Local Standard Time. The time local to the requested station.
zone3 =  'lst_ldt' # Local Standard/Local Daylight Time. The time local to the requested station.


# This url is needed to request the jsom data from an NOAA station.  See 
# 		https://tidesandcurrents.noaa.gov/api/ 
# for details.
part1 = f'https://tidesandcurrents.noaa.gov/api/datagetter?'
part2 = f'begin_date={start}&end_date={end}&station={STATION}'
part3 = f'&product=water_temperature&units=english&time_zone={zone2}'
part4 = f'&application=ports_screen&format=json'

# url = f'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={start3}
# &end_date={end3}&station={STATION}&product=water_temperature&units=english
# &time_zone={zone2}&application=ports_screen&format=json'

url = part1 + part2 + part3 + part4

response = requests.get(url)
response.raise_for_status()

# Load JSON data into a Python variable.
data = json.loads(response.text)
print(data)


TIME_STR = f'The current time is = {TM}'
REPEAT = len(TIME_STR)

def pr():
	"Prints asterisks to frame the output."
	print('*' * REPEAT)

# Print one hour of temperature data for the chosen station (STATION) along with 
# the station location and time.
pr()
print('Station: ' + data['metadata']['name'])
pr()
print(TIME_STR)
pr()
d = data['data']
# print('Station data:\n', d)


time_list = []
temp_list = []
for item in d:
    time_list.append(int(item['t'][14:16]))
    temp_list.append(float(item['v']))
    print('Time: {}: temp: {}'.format(item['t'], item['v']))

print(f'time list = {time_list}')
print(f'temp list = {temp_list}')

x_s = [-6*i for i in range(len(temp_list))]
sp.plot(x_s, temp_list)