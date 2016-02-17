import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import re
import sys
import csv
import itertools
import datetime
import time


"""  	Search the New York Times Real Estate section with your desired
  		criteria, and then paste url below and confirm that the last three 
  						characters of the url end with 'p=1': 			"""

url = "http://www.nytimes.com/real-estate/homes-for-sale/?location=ny-usa&locations%5B%5D=200040&selectedSuggestion=new+york%2C+usa&priceMin=0&priceMax=1000000000&sort=PRICE-HIGH-sort&p=1"

listings = []
beds = []
baths = []
neighborhood = []
addresses = []
latitudes = []
longitudes = []



r = requests.get(url)
soup = BeautifulSoup(r.content)

	
raw_search_name = soup.find_all("button", {"class":"lozenge-button"})
search_name = raw_search_name[0]['title']	
"""			Name of output file						"""
output_file  =  "%s_%s.csv" %(search_name, datetime.date.today())
	
	
print "Determining the number of webpages to open ..."
"""			the total number of listings			""" 
raw_num_of_listings = soup.find("span", {"id": "total-listings"}).text
clean_num_of_listings = int(re.sub("[^0-9]","", raw_num_of_listings))
"""			the total number of pages -> assume ~19 listings per page	"""
num_of_webpages = (clean_num_of_listings /19) + 1 



"""			modifies url to cycle through multiple pages	"""
for i in range(num_of_webpages):
	i+=1
	if i == 1:
		print "Extracting %s listings ..."  %(clean_num_of_listings)
	elif i <= 10:
		url = url[:-1] + str(i)
	elif i <= 100:
		url = url[:-2] + str(i)
	elif i <= 1000:
		url = url[:-3] + str(i)
	elif i > 1000:
		url = url[:-4] + str(i)
	
	
	print "Scraping data from webpage %s of %s" % (i, num_of_webpages)
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.content)
	except HTTPError as e:
		print "ConnectionError raised. Will reconnect in 30 seconds"
		time.sleep(30)
		r = requests.get(url)
		soup = BeautifulSoup(r.content)
		
		
	bed_bath_html_blocks = soup.find_all("p", \
					class_="listing-detail-text size-description")
	prices_html_blocks = soup.find_all("p", {"class": "listing-price"})
	neighborhood_html_blocks = soup.find_all("p", {"class": "listing-neighborhood"})
	addresses_html_blocks = soup.find_all("p", \
					class_="listing-detail-text listing-address")
	latitude_html_blocks = soup.find_all("div", {"data-latitude":True})
	longitude_html_blocks = soup.find_all("div", {"data-longitude":True})
	
	"""				scrapes data off of individual page			"""
	for l in range( len(bed_bath_html_blocks) ):
		# scrape & clean listings
		raw_listing = prices_html_blocks[l].text
		clean_listing = raw_listing.strip().replace(",","").replace('$',"")
		listings.append(clean_listing)

		# scrape & clean # of beds & baths
		list_w_bd_bth = bed_bath_html_blocks[l].contents
		beds_raw = list_w_bd_bth[1].get_text()
		baths_raw = list_w_bd_bth[5].get_text()
		beds.append( int(re.search(r'\d+', beds_raw).group())  )
		baths.append( int(re.search(r'\d+', baths_raw).group()) )
		
		# scrape & clean addresses	
		raw_address = addresses_html_blocks[l].get_text()
		clean_address = raw_address.strip().replace("\n","").replace(",","")
		addresses.append(clean_address)
	
		# scrape & clean neighborhood
		raw_neighborhood = neighborhood_html_blocks[l].text
		clean_neighborhood = raw_neighborhood.strip().replace("\n","").replace(",","") 
		neighborhood.append(clean_neighborhood)

		# latitude and longitude
		latitudes.append(latitude_html_blocks[l]['data-latitude'])
		longitudes.append(latitude_html_blocks[l]['data-longitude'])


#	write data arrays to file
f = open(output_file,'w')
header = "Listing Price,Bed,Bath,Neighborhood,Latitude,Longitude,Address\n"
f.write(header)
 
for p in range( len(listings) ):
	addrs = addresses[p].encode('ascii','ignore')
	nghbrhd = neighborhood[p].encode('ascii','ignore')
	line = "%s,%s,%s,%s,%s,%s,%s\n" %(listings[p],beds[p],baths[p], \
			nghbrhd,latitudes[p],longitudes[p],addrs)
	f.write(line)

f.close()
