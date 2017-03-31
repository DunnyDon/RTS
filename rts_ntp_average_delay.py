from datetime import datetime, date, time
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
fd = open("C:\Users\Conor\Desktop\Group4_ntpdata.txt",'r')
data_headers = ["remote","refid","st","t","when","poll","reach","delay","offset","jitter"]
float_headers = ["st","when","poll","reach","delay","offset","jitter"]
saved_data = ["remote","delay","offset","jitter"]
location = {'62.236.120.71':'Finland 1.','77.73.232.17':'Moscow','92.62.34.78':'Trondheim, Norway','85.114.26.194':'St.Petersberg,Russia','193.224.65.146':'Hungary 1.','89.234.64.77':'Dublin','194.100.206.70':'Finland 2.','131.188.3.220':'Bavaria,Germany','193.227.197.2':'Hungary 2.'}
count = 0
header = 0
time_data = {}
data_store =[]

for line in fd:
	header = 0
	data = {}
	if "=====" not in line:
		if "remote" not in line:
			if "TIME" in line:
				date_time= line.strip("TIME:")
				date_time = date_time.replace(" IST 2017:","")
				date_time = date_time.strip(" ").strip('\n')
				dt = datetime.strptime(date_time, "%a %b %d %H:%M:%S")
				#dt.replace(year =2017)
			else:
				temp = line.strip('\n').split(' ')
				if len(temp)>1:
					for j in temp:
						if j and data_headers[header] in float_headers:
							if data_headers[header] in saved_data:
								data[data_headers[header]]=float(j)
							header +=1
						elif j and data_headers[header] == "t":
							if data_headers[header] in saved_data:
								data[data_headers[header]]=j
							header +=1
						elif j and data_headers[header] == "refid":
							if data_headers[header] in saved_data:
								data[data_headers[header]]=j
							header +=1
						elif j and data_headers[header] == "remote":
							if data_headers[header] in saved_data:
								remote = j
							header +=1
					try:
						time_data[dt][remote] = data
					except KeyError as e:
						time_data[dt]={}
						time_data[dt][remote] = data
delay_avg = {}					
for key, value in time_data.iteritems():
	date = key
	for k,val in value.iteritems():
		#print type(date), type(date.strftime("%Y-%m-%d %H:%M:%S")),date,value[date]
		#print k.strip('-').strip('+').strip('*'),val
		col_dict = k.strip('-').strip('+').strip('*').strip('x')
		try:
			delay_avg[location[col_dict]]+=val["delay"]
		except KeyError as e:			
			delay_avg[location[col_dict]]=val["delay"]

print delay_avg
#x = np.array([0,1,2,3,4,5,6,7,8])
#my_xticks = delay_avg.keys()
#plt.xticks(x, my_xticks)
plt.bar(range(len(delay_avg)), delay_avg.values(), align='center')
plt.xticks(range(len(delay_avg)), delay_avg.keys())
plt.title("Total Delay")
plt.xlabel("Location of each server")
plt.ylabel('Total Delay (ms)')
plt.show()