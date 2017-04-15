""" This script scrapes the New York Times Real Estate Section for user 
specified property listings. Each scraped listing contains the 
following: listing price, beds, baths, latitude, longitude, and 
neighborhood. 
"""
import requests
import re
from bs4 import BeautifulSoup
from datetime import date
from time import localtime
import math as m

# Constant: Number NY Times listings per page
listings_per_page = 24

def modify_user_url(url):
    """ Modify user-entered url tail to either of two formats ('desc&p=' or 
    'asc&p=') to allow script to iterate through many pages
    """
    url_counter = 0
    while not((url[len(url) - 4:] == 'desc') or (url[len(url) - 4:] == '-asc')):
        if url[len(url)-1:] in "&p=1234567890":
            url = url[:len(url)-1]
            
        if (len(url) < 50) or (url_counter >= 12): 
            raise ValueError('URL Error. Please input a valid url.')
        url_counter += 1
    return url + '&p='


def num_pages_to_scrape(pages_string):
    """ Determine the number of pages on the NY Times website to scrape """
    current_listing = int(pages_string[1].split('-')[1])
    total_listings = int(pages_string[3])
    pages_to_iterate_over = int( m.ceil(total_listings * 1.0 / listings_per_page))
    return pages_to_iterate_over


class single_web_page (object):
    """ Extract property details from single NY Times web page """
    
    def __init__(self, soup):
        self.soup = soup
    
    
    def extract_data(self):
        """ Organize html soup extracts into lists of property features """ 
        self.bed_bath_html = self.soup.find_all("p", class_= "listing-detail-text size-description")
        self.prices_html = self.soup.find_all("p", {"class": "listing-price"})
        self.neighborhood_html = self.soup.find_all("p", {"class": "listing-neighborhood"})
        self.addresses_html = self.soup.find_all("p",class_= "listing-detail-text listing-address")
        self.lat_html = self.soup.find_all("div", {"data-latitude":True})
        self.long_html = self.soup.find_all("div", {"data-longitude":True})

        
    def transform_data(self):
        """ Clean data for each listing and append result into 'housing_data' """
        housing_data = []
        for i in range(len(self.prices_html) ):
            listing = []
            listing.append(self.prices_html[i].text.strip().replace(",","").replace('$',""))
            bd_bth_lst = self.bed_bath_html[i].contents
            listing.append(int(re.search(r'\d+', bd_bth_lst[1].get_text()).group()))
            listing.append(int(re.search(r'\d+', bd_bth_lst[5].get_text()).group()))
            listing.append(self.neighborhood_html[i].text.strip().replace("\n","").replace(",","") \
                                                    .encode('ascii','ignore'))
            listing.append(self.lat_html[i]['data-latitude'])
            listing.append(self.lat_html[i]['data-longitude'])
            listing.append(self.addresses_html[i].get_text().strip().replace("\n","").replace(",","") \
                                                    .encode('ascii','ignore'))
            housing_data.append(listing ) 
        return housing_data

                           
def create_output_file(search_name):
    """ Name output csv file with user's search-location-query, date, and time """
    output_file_name  =  "%s_%s_%shr_%smin.csv" %(
                                        search_name, date.today(),
                                        localtime()[3],localtime()[4])
    f = open(output_file_name,'w')
    header = "Listing Price,Bed,Bath,Neighborhood,Latitude,Longitude,Address\n"
    f.write(header)
    return [f, output_file_name]


if __name__ == '__main__':
 
    print "\nPlease copy and paste a url (see readme for formatting details)"
    print "into the command prompt here: "

    user_url=  raw_input()
    url = modify_user_url(user_url)
    page_num = 1
        
    soup = BeautifulSoup(requests.get(url + str(page_num)).content)
    pages_to_iterate_over = num_pages_to_scrape(soup.h1.string.split())
    f, output_file_name = create_output_file(soup.h3.string)

    while page_num <= pages_to_iterate_over:
        print "Scraping page %s of %s" % (page_num, pages_to_iterate_over)
        swp = single_web_page(soup)
        swp.extract_data()
        page_data = swp.transform_data()
        for single_property in range( len(page_data) ):
            f.write(','.join([str(detail) for detail in page_data[single_property]]) + '\n')
        page_num += 1
        soup = BeautifulSoup(requests.get(url + str(page_num)).content)
    f.close()
    print "\nPlease check the following file in this directory for listings:", output_file_name, "\n"
    
    
    
    
    
    
