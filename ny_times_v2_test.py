""" A unit testing script for the New York Times Web Scraper: ny_times_v2.py """
import unittest
import codecs
from bs4 import BeautifulSoup
import ny_times_v5 as nyt


class NYTimesTestCase(unittest.TestCase):
    """Unit Tests for NYTimes Web Scraper"""       
        
    def setUp(self):
        """ Load two soup objects, from two separate files, for testing """
        # Open file of Soup Containing 13 Property Listings in Manhattan
        f=codecs.open(r'test_files/Manhattan_13_listings_over_4M_4_13_2017_soup.html', 'r')
        soup_1 =  f.read()
        f.close()
        self.soup_1 = BeautifulSoup(soup_1)
        
        # Open soup file containing 181 Property Listings(on 8 web pages) in Manhattan 
        f2=codecs.open(r'test_files/Manhattan_181_listings_over_4M_4_13_2017_soup.html', 'r')
        soup_2 =  f2.read()
        f2.close()
        self.soup_2 = BeautifulSoup(soup_2)
        

    def test_modify_user_url_function_has_proper_ascending_format(self):
        """ Test that user-entered url is modified to end with '-asc&p=' """
        self.assertEqual(
            nyt.modify_user_url(
               'https://www.nytimes.com/real-estate/homes-for-sale/-ny-usa&sortBy=dateposted-asc')[-7:],\
                    '-asc&p=')
        
        
    def test_modify_user_url_function_has_proper_descending_format(self):
        """ Test that user-entered url is modified to end with '-desc&p=' """
        self.assertEqual(
            nyt.modify_user_url(
               'https://www.nytimes.com/real-estate/homes-for-sale/?&sortBy=dateposted-desc')[-8:],\
                    '-desc&p=')
        
        
    def test_modify_user_url_function_truncates_tail_properly(self):
        """ Test to see if modify_user_url function removes 'p=2' from tail of user-entered url 
        and correctly changes tail to '-asc&p=' """
        self.assertEqual(
            nyt.modify_user_url(
                'https://www.nytimes.com/real-estate/homes-for-sale/?&sortBy=bedrooms-ascp=2')[-7:],\
                   '-asc&p=')
        
        
    def test_modify_user_url_function_raises_error_when_url_is_too_short(self):
        """ Test to see if modify_url function raises ValueError when url is too short """
        with self.assertRaises(ValueError):
            nyt.modify_user_url(
                'https://www.nytimes.com/real-estate/homes-for-sale')
        
          
    def test_num_pages_to_scrape(self):
        """ Test if num_pages_to_scrape determines correct number of pages to iterate through """
        self.assertEqual( nyt.num_pages_to_scrape(self.soup_1.h1.string.split()),1 )
        self.assertEqual( nyt.num_pages_to_scrape(self.soup_2.h1.string.split()),8 )


    def test_single_web_page_extract_method_for_listing_price(self):
        """Test if an individual listing price is correctly extracted """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()        
        self.assertEqual(
            str(swp.soup.find_all("p", {"class": "listing-price"})[0]), \
           '<p class="listing-price">\n                $17,750,000                            </p>')

        
    def test_single_web_page_extract_method_for_bed_bath(self):
        """Test if bed/bath html soup is correctly extracted """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()        
        self.assertEqual(
                str(swp.soup.find_all("p", class_= "listing-detail-text size-description")[0]),\
                    '<p class="listing-detail-text size-description">\n<span>3 Beds</span>\n<span class="border">|</span>\n<span>3 Baths</span>\n<span class="border">|</span>\n<span>Condo</span>\n</p>')


    def test_single_web_page_extract_method_for_neighborhood(self):
        """Test if 'neighborhood' is correctly extracted """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()        
        self.assertEqual(
            str(swp.soup.find_all("p", {"class": "listing-neighborhood"})[0]), \
                    '<p class="listing-neighborhood" data-city="New York">\n                West Village            </p>')
        

    def test_single_web_page_extract_method_for_address(self):
        """Test if an individual address is correctly extracted """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()        
        self.assertEqual(
                 str(swp.soup.find_all("p",class_= "listing-detail-text listing-address")[0]),\
                            '<p class="listing-detail-text listing-address" title="155 West 11th Street">\n                155 West 11th Street            </p>')

        
    def test_single_web_page_transform_method_listing_price(self):
        """ Test if transform_data method cleans html listing price for output """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()
        self.assertEqual(swp.transform_data()[0][0],u'17750000')
   

    def test_single_web_page_transform_method_beds(self):
        """ Test if transform_data method cleans bed/bath html for output """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()
        self.assertEqual(
                         str(swp.soup.find_all("p",\
                            class_= "listing-detail-text size-description")[0]\
                                                            .contents[1].get_text()), \
                                                                                '3 Beds')
     
    
    def test_single_web_page_transform_method_for_neighborhood(self):
        """Test if 'neighborhood' extract is properly transformed for output """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()        
        self.assertEqual(
            str(swp.soup.find_all("p",\
                                 {"class": "listing-neighborhood"})[0].text.strip() \
                                        .replace("\n","") \
                                        .replace(",","") \
                                        .encode('ascii','ignore')),'West Village')


    def test_single_web_page_latitude(self):
        """ Test end to end functionality of latitude feature """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()
        self.assertEqual(
            swp.soup.find_all("div", {"data-latitude":True})[0]['data-latitude'], '40.736173')

        
    def test_single_web_page_longitude(self):
        """ Test end to end functionality of longitude feature """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()
        self.assertEqual(
            swp.soup.find_all("div", {"data-latitude":True})[0]['data-longitude'], '-74.000069')


    def test_single_web_page(self):
        """ Test end to end functionality of single_web_page Class by observing a single listing """
        swp = nyt.single_web_page(self.soup_1)
        swp.extract_data()
        self.assertEqual(swp.transform_data()[0],[u'17750000', 3,3,\
                                                  'West Village','40.736173','-74.000069',\
                                                     '155 West 11th Street'])

        
    def test_input_to_create_output_file_function(self):
        """test if location-query is extracted from soup """
        self.assertEqual(self.soup_1.h3.string, u'Manhattan')
        

        
if __name__ == '__main__':
    unittest.main()
    
