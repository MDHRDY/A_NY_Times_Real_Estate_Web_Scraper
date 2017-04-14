import requests
import re
from bs4 import BeautifulSoup
from datetime import date
from time import localtime
import math as m



def valid_url(url):
    
    url_counter = 0
    
    while not( (url[len(url)-4:] == 'desc') or ( url[len(url)-4:] == '-asc') ):
        
        if url[len(url)-1:] in "&p=1234567890": url = url[:len(url)-1]
            
        if (len(url) < 50) or (url_counter >= 12): 
            print 'Please check that the url is valid'
            return False
        
        url_counter += 1
    
    url += '&p='
    
    return url



def get_soup(url, page_num):
    
    r = requests.get(url + str(page_num))
    soup = BeautifulSoup(r.content)
    
    return soup, page_num



def num_pages_to_scrape(soup):

    pages = soup.h1.string.split()
    current_listing = int(pages[1].split('-')[1])
    total_listings = int(pages[3])
    pages_to_iterate_over = int( m.ceil(total_listings * 1.0 /24) )
    
    return pages_to_iterate_over



def scrape_single_web_page(soup):

    bed_bath_html = soup.find_all("p", \
                    class_="listing-detail-text size-description")
    prices_html = soup.find_all("p", {"class": "listing-price"})
    neighborhood_html = soup.find_all("p", {"class": "listing-neighborhood"})
    addresses_html = soup.find_all("p", \
                    class_="listing-detail-text listing-address")
    lat_html = soup.find_all("div", {"data-latitude":True})
    long_html = soup.find_all("div", {"data-longitude":True})

    return [bed_bath_html,prices_html,neighborhood_html,addresses_html, lat_html, long_html]



def clean_data(scraped_data):
    
    listings, beds, baths, neighborhood = [],[],[],[]
    addresses, latitudes,longitudes = [], [], []
    
    bed_bath_html,prices_html,neighborhood_html,addresses_html, lat_html, long_html = scraped_data
    
    for i in range( len(prices_html) ):

        raw_listing = prices_html[i].text
        clean_listing = raw_listing.strip().replace(",","").replace('$',"")
        listings.append(clean_listing)

        list_w_bd_bth = bed_bath_html[i].contents
        beds_raw = list_w_bd_bth[1].get_text()
        baths_raw = list_w_bd_bth[5].get_text()
        beds.append( int(re.search(r'\d+', beds_raw).group())  )
        baths.append( int(re.search(r'\d+', baths_raw).group()) )

        raw_address = addresses_html[i].get_text()
        clean_address = raw_address.strip().replace("\n","").replace(",","")
        addresses.append(clean_address)

        raw_neighborhood = neighborhood_html[i].text
        clean_neighborhood = raw_neighborhood.strip().replace("\n","").replace(",","") 
        neighborhood.append(clean_neighborhood)

        latitudes.append(lat_html[i]['data-latitude'])
        longitudes.append(lat_html[i]['data-longitude'])

        housing_data = [listings,beds,baths,neighborhood, latitudes,longitudes,addresses]
        
    return housing_data



def create_output_file(soup):
    # Output file name contains user's search query, date, and time
    search_name = soup.h3.string
    output_file  =  "%s_%s_%shr_%smin.csv" %(search_name, 
                        date.today(),localtime()[3],localtime()[4])

    f = open(output_file,'w')
    header = "Listing Price,Bed,Bath,Neighborhood,Latitude,Longitude,Address\n"
    f.write(header)
    
    return [f, output_file]



if __name__ == '__main__':

    print "\nPlease copy and paste a url (see readme for formatting details)"
    print "into the command prompt here: "
    
    user_url=  raw_input()

    #user_url = obtain_url()
    url = valid_url(user_url)

    soup, page_num = get_soup(url, 1)
    pages_to_iterate_over = num_pages_to_scrape(soup)

    f, output_file = create_output_file(soup)

    while page_num <= pages_to_iterate_over:
        listings, beds, baths, neighborhood = [],[],[],[]
        addresses, latitudes,longitudes = [], [], []

        print "Scraping page %s of %s" % (page_num, pages_to_iterate_over)
        scraped_data = scrape_single_web_page(soup)
        housing_data = clean_data(scraped_data)
        listings,beds,baths,neighborhood, latitudes,longitudes,addresses = housing_data

        for p in range( len(listings) ):
            addrs = addresses[p].encode('ascii','ignore')
            nghbrhd = neighborhood[p].encode('ascii','ignore')
            line = "%s,%s,%s,%s,%s,%s,%s\n" %(listings[p],beds[p],baths[p], \
                                nghbrhd,latitudes[p],longitudes[p],addrs)
            f.write(line)

        page_num += 1

        soup, page_num = get_soup(url, page_num)

    f.close()

    print "\nPlease check the following file in this directory for listings:", output_file, "\n"
