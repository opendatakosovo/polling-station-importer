import csv
import unicodedata

from slugify import Slugify
from pymongo import MongoClient

csv_filename = 'polling-stations-general-elections-2014.csv'

# Connect to default local instance of mongo
client = MongoClient()

# Get database and collection
db = client.kdi
collection = db.generalelectionspollingstations2014

# Clear data
collection.remove({})

def remove_diacritic(str):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    
    :param str: The string tor remove dicritical marks from.
    '''
    return unicodedata.normalize('NFKD', str.decode('utf-8')).encode('ASCII', 'ignore')
    
def slugify(str):
	''' Generates a slug for the given string.
	:param str: The string to slugify. 
	'''

def parse_csv():
	'''
	Reads the election polling station CSV file.
	Creates Mongo document for each polling station.
	Stores document.
	'''
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
			
			slugify = Slugify(to_lower=True)
				
			polling_station = {
				'_id': polling_station_id,
				'name': {
					'sq': polling_station_name_sq.strip(),
					'sr': polling_station_name_sr.strip(),
					'slug':{
						'sq': slugify(polling_station_name_sq),
						'sr': slugify(polling_station_name_sr)
					}
					
				},
				'city': {
					'sq': city_sq.strip(),
					'sr': city_sr.strip(),
					'slug':{
						'sq': slugify(city_sq),
						'sr': slugify(city_sr)
					}
				},
				'commune': {
					'id': commune_id,
					'sq': commune_name_sq.strip(),
					'sr': commune_name_sr.strip(),
					'slug':{
						'sq': slugify(commune_name_sq),
						'sr': slugify(commune_name_sr)
					}
				},
				'coordinates': {
					'lon': 0,
					'lat': 0
				}
			}
			
			# Store polling station as document in mongo.
			collection.insert(polling_station)
		
parse_csv()
