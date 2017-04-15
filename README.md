# Scrape data from the New York Times's real estate section
This program scrapes the listing price, number of beds, number of baths, latitude, longitude, neighborhood name, and the address of current properties listings - based upon your search criteria - and outputs data in csv format. Head to the [New York Times real estate section](https://www.nytimes.com/real-estate/homes-for-sale/) and enter in a neighborhood, city or state:

<br></br>

![Image1 of nytimes website](https://github.com/MDHRDY/A_NY_Times_Real_Estate_Web_Scraper/blob/master/ny_times_real_estate_home_page.png)

<br></br>

Note that after entering a location and clicking 'See Available Homes', there are some additional filtering tools, such as 'Open House', 'Reduced', and 'ADAVANCED FILTERS' (See next image).

### Run:
To run this program, run the following command at the command line:

<pre><code>python nytimes_v2.py</code></pre>

After the script begins, it will prompt you for a url. Copy and paste a url from the nytimes web page into the command prompt, and the scraper will pull listings off of the web, create an output file, and output data into your local directory. For the program to work, the last four characters of the url must end with '-asc' or 'desc'. Please see url in the following picture. 

![Image2 of nytimes website](https://github.com/MDHRDY/A_NY_Times_Real_Estate_Web_Scraper/blob/master/real_estate_search.png)

If your url does not currently end with '-asc' or '-desc', use the 'Sort By' function, as shown above. This will generate a new url with the correct tail. If 'p', '&p', or '&p=' (plus a number) follows the '-asc' or 'desc' tail, the script will also hande these tails.

### System Requirements
The program uses the 'requests' and 'beautifulsoup' packages, which are both available in the [Anaconda](https://www.continuum.io/downloads) distribution.  
Python 2.7.11 [Anaconda 2.3.0] or later will do
