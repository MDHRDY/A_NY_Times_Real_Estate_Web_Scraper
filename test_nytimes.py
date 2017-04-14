import unittest
from bs4 import BeautifulSoup
import codecs
from ny_times_listings_v3 import valid_url
from ny_times_listings_v3 import num_pages_to_scrape
from ny_times_listings_v3 import scrape_single_web_page




class NYTimesTestCase(unittest.TestCase):
    """Tests for NYTimes Web Scraper"""       
        
        
    def test_is_valid_url(self):
        """are urls wth the proper endind valid>"""
        
        self.url_asc = 'https://www.nytimes.com/real-estate/homes-for-sale/-ny-usa&sortBy=dateposted-asc'
        self.url_desc = 'https://www.nytimes.com/real-estate/homes-for-sale/?&sortBy=dateposted-desc'
        self.url_trunc_end = 'https://www.nytimes.com/real-estate/homes-for-sale/?&sortBy=bedrooms-ascp=2'
        self.url_too_short = 'https://www.nytimes.com/real-estate/homes-for-sale/'      
  
        self.assertTrue(valid_url(self.url_asc))
        self.assertTrue(valid_url(self.url_desc))
        self.assertTrue(valid_url(self.url_trunc_end))
        self.assertFalse(valid_url(self.url_too_short))

      
    
    def test_num_pages_to_scrape(self):
        """ Determine if script iterates through the correct number of pages """
        
        f=codecs.open(r'test_files/Manhattan_13_listings_over_4M_4_13_2017_soup.html', 'r')
        soup_1 =  f.read()
        f.close()
        soup_1 = BeautifulSoup(soup_1)
        
        f2=codecs.open(r'test_files/Manhattan_181_listings_over_4M_4_13_2017_soup.html', 'r')
        soup_2 =  f2.read()
        f2.close()
        soup_2 = BeautifulSoup(soup_2)
        
        self.assertEqual( num_pages_to_scrape(soup_1),1 )
        self.assertEqual( num_pages_to_scrape(soup_2),8 )


    def test_scrape_single_web_page(self):

        f=codecs.open(r'test_files/Manhattan_13_listings_over_4M_4_13_2017_soup.html', 'r')
        soup_L =  f.read()
        f.close()
        
        soup_html = BeautifulSoup(soup_L)
        method_output = str( scrape_single_web_page(soup_html)[1] )
        
        fs=codecs.open(r'test_files/thirteen_scraped_Manhattan_listings.csv', 'r')
        scraped_listings =  fs.read()
        fs.close()
        
        #saved_scraped_file = str( scrape_single_web_page(soup_L)[1] )
        
        self.assertEqual(method_output,scraped_listings)


if __name__ == '__main__':
    unittest.main()