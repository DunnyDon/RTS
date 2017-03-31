from datetime import datetime, date, time
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
fd = open("C:\Users\Conor\Desktop\Group4_ntpdata.txt",'r')
data_headers = ["remote","refid","st","t","when","poll","reach","delay","offset","jitter"]
float_headers = ["st","when","poll","reach","delay","offset","jitter"]
saved_data = ["remote","delay","offset","jitter"]
plot_colours = {'62.236.120.71':'r','77.73.232.17':'b','92.62.34.78':'g','85.114.26.194':'c','193.224.65.146':'m','89.234.64.77':'y','194.100.206.70':'k','131.188.3.220':'#f77402','193.227.197.2':'#7c01f7'}
count = 0
header = 0
time_data = {}
data_store =[]
fig, ax = plt.subplots()
# Use plot_date rather than plot when dealing with time data.
myFmt = mdates.DateFormatter('%d/%m')
ax.xaxis.set_major_formatter(myFmt)
plt.xlim([datetime(1900, 3, 27,15,30,00), datetime(1900, 3, 31,11,00,00)])
plt.ylabel('Offset (ms)')
plt.xlabel('Date')
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
					
for key, value in time_data.iteritems():
	date = key
	for k,val in value.iteritems():
		#print type(date), type(date.strftime("%Y-%m-%d %H:%M:%S")),date,value[date]
		#print k.strip('-').strip('+').strip('*'),val
		col_dict = k.strip('-').strip('+').strip('*').strip('x')
		print date,val['offset'],plot_colours[col_dict]
		plt.scatter(date,val['offset'],color=plot_colours[col_dict])
		plt.pause(0.01)
	#print key, type(key)

plt.show()