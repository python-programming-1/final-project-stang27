import requests
import lxml.html as lh

# Function for Moving Averages, input list of closing prices, which day to start, how many day moving average
def MovingAverage(closing_list,start_day,days):
	# Moving average calculation
	# For start day 0 = today, 1 =yesterday, etc
	moving_average_list = []
	# Create moving average list, depending on the start day
	for day in range(days):
		moving_average_list.append(closing_list[start_day+day])

	# Find the sum, then the average
	average = 0
	for day in range(days):
		average = moving_average_list[day] + average

	moving_average = average/days
	return moving_average

# Data analysis for Buying
def Buy(closing_list,moving_average,days):
	# Buy if the closing price crosses below the moving average 
	yesterday_ma = MovingAverage(closing_list,1,days)
	if closing_list[0] > moving_average and closing_list[1] < yesterday_ma:
		return 'You should buy!'
	return 'You should wait!'	

# Data analysis for Selling
def Sell(closing_list,moving_average,days):
	# Sell if the closing price crosses above the moving average
	yesterday_ma = MovingAverage(closing_list,1,days)
	if closing_list[0] < moving_average and closing_list[1] > yesterday_ma:
		return 'You should sell!'
	return 'You should wait!'
	


# Ask user for a stock, moving average days, buy or sell
print('Welcome to Stalk the Stock! Let\'s Stalk Your Stock!')
ticker = input('What is the ticker symbol you want to analyze: ')
day_for_average = input('How many days would you like to analyze: ')
buy_or_sell = input('Do you want to buy or sell: ')

print('---------------------\n' + 'Stalk the Stock Analysis:')


# URL
url='https://finance.yahoo.com/quote/'+ticker+'/history?p=' +ticker
print('URL:' + url)
#Get the information from the website
res = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(res.content)
#Take the data that is stored between <tr>..</tr> of HTML
history_table = doc.xpath('//tr')

#Create empty list
col=[]
i=0
#Store the header
for header in history_table[0]:
    i+=1
    name=header.text_content()
    #Checker for headers
    #print ('%d %s' %(i,name))
    col.append((name,[]))

#Store the data into a dictionary
for date_data in range(1,len(history_table)):

    T=history_table[date_data]
    
    #If row is not of size 7, do not add into column (avoid divdends) 
    if len(T) == 7:
            
	    #i is the index of our column
	    i=0
	    
	    #Iterate through each element of the row
	    for t in T.iterchildren():
	        data=t.text_content() 
	        #Check if row is empty
	        if i>0:
	        #Convert any numerical value to integers
	            try:
	                data=int(data)
	            except:
	                pass
	        #Append the data to the empty list of the i'th column
	        col[i][1].append(data)
	        #Increment i for the next column
	        i+=1

Dict={title:column for (title,column) in col}

closing_list = (Dict['Close*'])

#String to float 
float_closing_list = []
for date in closing_list:
	 float_closing_list.append(float(date))

# Moving average calculation
moving_average = MovingAverage(float_closing_list,0,int(day_for_average))

print('Date: '+ Dict['Date'][0])
print('Today\'s closing: $' + closing_list[0])
print('Moving Average for ' + day_for_average + ' day(s): $'+ str(round(moving_average,2)))

# Data analysis for buying or selling
if buy_or_sell == 'buy':
	print(Buy(float_closing_list,moving_average,int(day_for_average)))
elif buy_or_sell == 'sell':
	print(Sell(float_closing_list,moving_average,int(day_for_average)))
else:
	print('Please try again!')
