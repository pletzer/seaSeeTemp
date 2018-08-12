import netCDF4
import datetime
import numpy

firstYear = 1962
lastTimeIndex = 1957
firstLatIndex, lastLatIndex = 49, 59
firstLonIndex, lastLonIndex = 130, 175
timeSlice = '[{}:{}]'.format(0, lastTimeIndex)
latSlice = '[{}:{}]'.format(firstLatIndex, lastLatIndex)
lonSlice = '[{}:{}]'.format(firstLonIndex, lastLonIndex)
url = 'http://nomads.ncdc.noaa.gov/thredds/dodsC/ersstv3Agg'

# get the data, may want to combine the opendap calls into one
time = netCDF4.Dataset(url + '?time' + timeSlice).variables['time']
lat = netCDF4.Dataset(url + '?lat' + latSlice).variables['lat']
lon = netCDF4.Dataset(url + '?lon' + lonSlice).variables['lon']
sst = netCDF4.Dataset(url + '?sst' + timeSlice + '[0]' + latSlice + lonSlice).variables['sst']

# time is month since 1854-01-15
# we're only interested in August to October period
baseDate = datetime.datetime(year=1854, month=1, day=15)
numDaysPerYear =  365.2425
numDaysPerMonth = numDaysPerYear / 12.0
years = []
timeInds = []
august, october = 8, 10
flip = False
for months in time[:]:
	date = baseDate + datetime.timedelta(days=months * numDaysPerMonth)
	year, month = date.year, date.month
	if flip and month == october:
		timeInds[-1][1] = months
		flip = False
	elif year >= firstYear and not flip and month == august:
		years.append(year)
		timeInds.append([months, None])
		flip = True
	
# average the sst data for Aug-Oct
sstAugOct = [numpy.mean(sst[timeInds[i][0]:timeInds[i][1]+1, :, :]) for i in range(len(years))]

