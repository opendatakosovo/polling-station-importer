import csv
from pymongo import MongoClient

csv_filename = 'polling-stations-general-elections-2014.csv'

# Connect to default local instance of mongo
client = MongoClient()

# Get database and collection
db = client.generalelections2014
collection = db.pollingstations

with open(csv_filename, 'rb') as csvfile:
	reader = csv.reader(csvfile)
	
	# Skip the header
	next(reader, None)
	
	# Iterate through the rows, retrieve desired values.
	for row in reader:
		polling_station_id = row[3]
		commune_id = row[1]
		
		if('/' in row[2]):
			commune_names = row[2].split('/')
			commune_name_sq = commune_names[0]
			commune_name_sr = commune_names[1]
		else:
			commune_name_sq = row[2]
			commune_name_sr = row[2]
			print 'Missing commune name translation for polling station {0}: {1}'.format(polling_station_id, commune_name_sq)
		
		if('/' in row[4]):
			cities = row[4].split('/')
			city_sq = cities[0]
			city_sr = cities[1]
		else:
			city_sq = row[4]
			city_sr = row[4]
			print 'Missing city name translation for polling station {0}: {1}'.format(polling_station_id, city_sq)
		
		polling_station_name_sq = row[5]
		polling_station_name_sr = row[6]
			
		polling_station = {
			'_id': polling_station_id,
			'name': {
				'sq': polling_station_name_sq.strip(),
				'sr': polling_station_name_sr.strip()
			},
			'city': {
				'sq': city_sq.strip(),
				'sr': city_sr.strip()
			},
			'commune': {
				'id': commune_id,
				'sq': commune_name_sq.strip(),
				'sr': commune_name_sr.strip()
			},
			'coordinates': {
				'lon': 0,
				'lat': 0
			}
		}
		
		# Store polling station as document in mongo.
		collection.insert(polling_station)
