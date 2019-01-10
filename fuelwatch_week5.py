import requests
import feedparser
import pprint
import datetime

def get_fuel(which_day):
	data = feedparser.parse('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Day='+str(which_day))
	return data['entries']

def takeprice(f_lsit):
	return f_lsit['price']

def build_table_items(f_list):
	table_items = ''
	print(len(f_list))
	now = datetime.datetime.now()

	for e in f_list:
		date_info = datetime.datetime.strptime(e['date'], "%Y-%m-%d")
		if date_info > now:
			items = make_tomorrow_fuel(e)
		else:
			items = make_today_fuel(e)

		table_items += items

	return table_items

def make_today_fuel(e):
	item = '''
			<tr><td>{}</td><td>{}</td><td>{}</td></tr>
		'''.format(e['title'], e['description'], e['brand'])
	return item

def make_tomorrow_fuel(e):
	item = '''
			<tr bgcolor="#00FF00"><td>{}</td><td>{}</td><td>{}</td></tr>
		'''.format(e['title'], e['description'], e['brand'])
	return item

def collect_info(feed):
	
	f_list = feed
	print(len(f_list))
	f_list.sort(key=takeprice, reverse=False)
	t_items = build_table_items(f_list)
	return t_items
def get_today_date():
	response = requests.get('https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS')
	feed = feedparser.parse(response.content)
	#print(feed.feed.updated)
	return feed.feed.updated

feed = get_fuel("today") + get_fuel("tomorrow")

content = '''
    <table>
        <tr><td></td><td>{this_feed_date}</td><td></td>
		</tr>{this_items}
    </table>'''.format(this_feed_date = get_today_date(), this_items=collect_info(feed))

with open('list.html', 'w') as f:
	f.write(content)