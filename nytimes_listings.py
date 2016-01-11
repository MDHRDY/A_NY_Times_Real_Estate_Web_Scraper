import requests
from bs4 import BeautifulSoup
import re
import sys
import csv
import itertools
import datetime

#  Search the New York Times Real Estate section with your desired
#  criteria, and then place url here (confirm that the last three characters are 'p=1':
url = "http://www.nytimes.com/real-estate/homes-for-sale/?location=park-slope-brooklyn-ny-usa&locations%5B%5D=200040000017310986&selectedSuggestion=park+slope&priceMin=0&priceMax=1000000000&sort=PRICE-HIGH-sort&p=1"

# These are the names of the two output files
raw_output = "raw_output_txt_file.txt"
clean_output = "name_of_your_query.csv"
count = 1

r = requests.get(url)
soup = BeautifulSoup(r.content)


#  obtain listing prices found in given url & 
#  the total number of listings, which is likely spread across multiple pages

# the total number of listings 
num_of_listings = soup.find("span", {"id": "total-listings"}).text

#  the total number of pages - assume ~19 listings per page
num_of_webpages = int(re.sub("[^0-9]","", num_of_listings)) /19 

all_prices = soup.find_all("p", {"class": "listing-price"})

#  write listings to output file
f = open(raw_output,'w')
for price in all_prices:
	print "Listing #: %d, price: %s" %(count, price.text)
	f.write(price.text)
	count +=1



#  loop through the remaining web pages & append additional 
#  listings to output file
for i in range(num_of_webpages):
	if i + 2 <= 10:
		url = url[:-1] + str(i+2)
	elif i + 2 <= 100:
		url = url[:-2] + str(i+2)
	elif i + 2 <= 1000:
		url = url[:-3] + str(i+2)
	elif i + 2 > 1000:
		url = url[:-4] + str(i+2)
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	all_prices = soup.find_all("p", {"class": "listing-price"})
	for price in all_prices:
		print "Listing #: %d, webpage: %d " %(count, i+2)
		print "price: %s" %(price.text)
		f.write(price.text)
		count += 1 
f.close()


#  clean up raw output file & store result in a csv
with open(raw_output, 'r') as in_file:
    stripped = (line.strip().replace(",","").replace('$',"") for line in in_file)
    lines = (line for line in stripped if line) # removes blank lines
    grouped = itertools.izip(*[lines])
    with open(clean_output, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('%s Search - Listings in Dollars' %datetime.date.today(), ),) 
        writer.writerows(grouped)


