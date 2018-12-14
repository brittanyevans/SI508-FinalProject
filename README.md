# SI508-FinalProject - Brittany Ann Evans

This project analyzes the political bias in English language state-funded media around the world. It currently uses three state-funded media websites for the scope of this project. It scrapes the top articles from each website for the day, gets the respective bias measurement from the API (see note below), and caches that data. The data is stored in MongoDB. The user interfaces with the command prompt to view current countries in the database and plot values via Plot.ly.

## Data Sources
[**Top Bottom Center API**](https://topbottomcenter.com/api_info/) takes in an article title and article text and returns a measurement of political bias on a scale of -1 to 1  in a json response. 

***PLEASE NOTE THAT THIS API IS CURRENTLY DOWN. THE PROGRAM CURRENTLY RETURNS RANDOM VALUES  BUT IS EQUIPPED TO HANDLE THE REQUESTS AUTOMATICALLY WHEN THE API IS BACK UP. PLEASE SEE LINES 21-25 FROM 'scraping.py' IF INTERESTED. I WAS TOLD BY INSTRUCTORS I AM FINE SINCE I CANNOT CONTROL THAT IT WAS TAKEN DOWN AFTER I HAD ALREADY IMPLEMENTED IT. [Here](https://github.com/brittanyevans/SI508-FinalProject/blob/master/University%20of%20Michigan%20Mail%20-%20404%20on%20API%20Request.pdf) is a copy of my communications with the developer***

* Endpoint: https://topbottomcenter.com/api/ 
* Required Parameters: article title, article text
* Returns: measurement of bias in a json response


Note: The bias measurement is one company's representation of political bias from an American perspective. These measurements are not a standard or universal indicator of bias, but can show what may constitute bias from an American perspective. 

**State-affiliated media sources**

I have chosen this list tentatively because these sites are popular and known to people outside of each respective country. I have a list of other state-affiliated media sources that may work and would be easy to scrape, and in the future I may want to focus on a particular geographical region to help draw further meaning. 

* RT - [Russia](https://www.rt.com/)
* CCTV – [China](http://english.cctv.com/)
* Deutsche Welle – [Germany](https://www.dw.com/en/top-stories/s-9097)

## Getting Started
### You will need the following:
 * [Python3](https://www.python.org/downloads/)
#### For scraping:
 * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) `pip install BeautifulSoup4`
 * [requests](http://docs.python-requests.org/en/v2.7.0/user/install/) `pip install requests`
 * [requests-cache](https://requests-cache.readthedocs.io/en/latest/user_guide.html) (this program uses the default `sql-lite` backend)`pip install requests-cache`
 * [numpy](http://www.numpy.org/) (for random number generation) `pip install numpy`
#### For the database:
 * [mongoengine](http://docs.mongoengine.org/tutorial.html) `pip install mongoengine`
 If you want to use a different database, you will need to change the database fields in the `secrets.py` file
#### For plotting:
 * [Plotly](https://plot.ly/python/) `pip install plotly`
 * Get an API key for [Plotly](https://plot.ly/python/) for Python users

## Running the program
* Clone the project `git clone https://github.com/brittanyevans/SI508-FinalProject.git`
* Create a file called `secrets.py` to store:
  * Plotly credentials as `plotly_credentials`
  * Information about a MongoDB database to connect to as `db_vals`. I've already set up a database in a cloud environment using [mLab](https://mlab.com/home) that will be easy to get you started. I've kept some sample credentials in the `secrets.py.example` file that will work with the database that I've set up for you to use. 
  * See `secrets.py.example` for an example of this file
* In the terminal, navigate to your directory and call `python3 interface.py`. You will be prompted with instructions to begin:

![alt-text](https://github.com/brittanyevans/SI508-FinalProject/blob/master/welcome_mesage.png "Welcome Message")

Go ahead and use it. The program will tell you if it does not understand commands that you enter into the command prompt.

### Examples

If I wanted to see all of the articles from Russia, I would use the command `plot country russia` as indicated above. Here is an example of a possible output:

![alt-text](https://github.com/brittanyevans/SI508-FinalProject/blob/master/all_russia.png "Example image")

## Testing
The test suite ensures that article scraping, api calls, the database, and plotting is done as intended. Test this project by running `python3 test_media_proj.py`

## Project Requirements Met in this Project
 * Base Requirements
    * Data sources:
        * 3 Websites
        * 1 API
    * Caching:
        * `requests-cache` is used for development
        * When running the `interface.py` file, caching is not utilized because the program must update the database with new data; however, when running the `scraping.py` file directly (for development purposes) caching is fully implemented with the `requests-cache` library
    * Processing data from the scraped pages to extract an article's title, text, and link information. This information is added to an Article database object, which is a child of the Country class. The program then generates a date and makes a request to the API for the bias score and ads them to the article before saving it in the database. 
    * Imports libraries such as mongoengine, BeautifulSoup4, sys, and os
    * A test suite that contains 7 subclasses (1 for Plotly, 1 for each of the 2 classes, 1 for bias values, and 1 for each of the 3 scraping methods) and 16 non-trivial tests within those subclasses
    * Running project produces interactive interface that results in visualizations of queryed data from the database
    * 2 classes that represent a Country and an Article. In this case, a country ***has*** an article
 * Second-Level Requirements
    * Scraping data that comes in HTML from BeautifulSoup4
    * Uses a few libraries that we did not study in class (mongoengine, requests-cache, etc.) 
    * Uses object inheritance (All classes inherit from the mongoengine Document class)
    * Accesses a REST API that we did not cover in class (Currently returning errors, but will work when back up. See above)
    * Interacts with a NoSQL database
* Third-Level Requirements
    * A clear visualization of data using Plot.ly
    * Project is interactive in the command line. 
## Future Plans
* Continue to ~annoy~ email conner@connerpro.com because I am very sad that his API is down. It will be fun to investigate trends when possible. 
* Implement automation using a CronJob

## Thanks for reading! 
