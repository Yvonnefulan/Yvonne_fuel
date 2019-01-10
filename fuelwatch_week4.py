import requests
import feedparser

import pprint


def get_fuel(product_id):
	
	data = feedparser.parse('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product='+str(product_id)+'&Suburb=Cloverdale')
	
	return data['entries']



def takeprice(f_lsit):
	
	return f_lsit['price']



def build_table_items(f_list):
	
	table_items = ''

	
	for e in f_list:
		
		items = '''
			
			<tr><td>{}</td><td>{}</td><td>{}</td></tr>
'''.format(e['title'], e['description'], e['brand'])

		table_items += items
 
	
	return table_items



def collect_info(feed):
	
	f_list = feed['entries']

	f_list.sort(key=takeprice, reverse=True)
 

	t_items = build_table_items(feed['entries'])


	return t_items



response = requests.get('https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS')


feed = feedparser.parse(response.content)

content = '''

    <table>

        <tr><td></td><td>{this_feed_date}</td><td></td></tr>

	{this_items}
    </table>
'''.format(this_feed_date = feed.feed.updated, this_items=collect_info(feed))




with open('list.html', 'w') as f:
    
	f.write(content)