# Scrape data from the New York Times's real estate section
Currently, this program will scrape the listing price of current properties (more features coming soon!) - based upon your search criteria - and output the data in csv format. Head to the [New York Times real estate section] (http://www.nytimes.com/pages/realestate/index.html?action=click&pgtype=Homepage&region=TopBar&module=HPMiniNav&contentCollection=Real%20Estate&WT.nav=page) and enter in a neighbord, city or state:

<br></br>

![Image1 of nytimes website](https://cloud.githubusercontent.com/assets/16641405/12249197/01292e80-b873-11e5-8920-a90f975c5adb.png)

<br></br>

Note that after entering a location and clicking 'See Available Homes', there are some additional filtering tools, such as 'Open House', 'Reduced', and 'ADAVANCED FILTERS' (See next image).

###Run:###
To run this program, copy and paste the url into the python code and type the following into the command line:

<pre><code>python nytimes_listings.py</code></pre>

For the program to work, the last three characters in the url must be 'p=1', as shown in the image below: 

![Image2 of nytimes website](https://cloud.githubusercontent.com/assets/16641405/12249211/13997f7a-b873-11e5-9c27-99ae1ed09a04.png)

If your url does not currently end with 'p=1', use the 'Sort By' function, as shown above. This will generate a new url that ends with 'p=1'.

### System Requirements###
The program uses the 'requests' and 'beautifulsoup' packages, which are both available in the [Anaconda] (https://www.continuum.io/downloads) distribution.  
Python 2.7.11 [Anaconda 2.3.0]
