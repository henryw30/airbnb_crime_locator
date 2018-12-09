# airbnb_crime_locator
Given a list of Airbnb listings in NYC, this script finds recent felonies that have occurred in the area by figuring out which borough the listing is in and connects to NYC's Crime Database to find crime data.

This python script uses Selenium and the Chrome web driver to connect to Airbnb.com since Airbnb does not provide an API. It then scrapes the text from the listings and uses Stanford's Named Entity Recognizer to identify which borough the Airbnb listing is located in. The script then connects to NYC's Crime Database to find the number of felonies that have recently occurred in the area and ranks the Airbnb listings from the least number of felonies to most.


Link to NYC's Crime Database
- https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243

Overview of functions (script will handle all function calls):
- read_url_listings: reads url listings from listings.txt
- write_listings_ordered: writes ordered listings to ordered.txt
- find_borough: identifies borough of listing
- get_crime_data: connects to NYC's Crime Database and finds number of felonies in borough


# Installation
Clone this repository and make sure to download these repositories first:

Stanford CoreNLP (unzip and know the absolute path to this directory): https://stanfordnlp.github.io/CoreNLP/download.html

Google Chrome Driver (unzip and know the absolute path where this driver was downloaded): https://chromedriver.storage.googleapis.com/index.html?path=2.44/

Java 8 (to use Stanford CoreNLP): https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

Selenium: https://pypi.org/project/selenium/
```
pip install selenium
```
Sodapy: https://pypi.org/project/sodapy/0.1.4/
```
pip install sodapy
``` 
      
NLTK: https://pypi.org/project/nltk/
```
pip install nltk
```

# Before Running the Script
Follow these directions to set up the Stanford NER Server in a terminal window:
- cd into the unzipped Stanford CoreNLP project directory and run the following command:
 ```
 java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 150000
```
- the server will be ready once this is shown in the terminal
```
[main] INFO CoreNLP - StanfordCoreNLPServer listening at /0:0:0:0:0:0:0:0:9000
```
- open a new terminal and give executable privileges to html_scrape.py with the following command
```
chmod +x html_scrape.py
```
- add your airbnb listings in listings.txt separated by a comma (an example is found in listings.txt)
# Running the Script
- cd into the this project directory and run the following command:
```
#example of absolute-path-to-chrome-driver: /Users/bob/Downloads/chromedriver
python html_scrape.py -C <absolute-path-to-chrome-driver> -L http://localhost:9000
```
- once done, results can be found in ordered.txt found in this directory
## Options When Running the Script
-use -h flag for help:
```
python html_scrape.py -h
```
- running script in non-headless mode (can see actual chrome window):
```
python html_scrape.py -C <absolute-path-to-chrome-driver> -L http://localhost:9000 -H 1
```
# Closing the Server
- close the server with ctrl+c in the terminal with server info
