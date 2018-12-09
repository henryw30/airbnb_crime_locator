from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.parse import CoreNLPParser
from sodapy import Socrata
import datetime
import neighborhoods as nb
import argparse

#reads url listings from listings.txt
def read_url_listings(path_to_listings):
    #read file with airbnb listings to compare
    text_file = open(path_to_listings, "r")
    urls = [x.strip(' ') for x in text_file.read().split(',')]
    text_file.close()
    return urls

#writes ordered list to file
def write_listings_ordered(ordered_listings):
    with open('ordered.txt', 'w') as f:
        f.write('\n'.join('%s    %s' % x for x in ordered_listings))

#find specific borough given a list of cities/locations
def find_borough(list_of_locations):
    borough_dict = {"manhattan": 0, "queens":0, "bronx":0, "brooklyn":0, "staten":0}

    #go through all locations and add to count
    for loc in list_of_locations:
        if(loc.lower() in nb.manhattan_neighborhoods or loc.lower() == "manhattan"):
            #since manhattan is very common in any airbnb listing near nyc
            if(loc.lower() == "manhattan"):
                borough_dict["manhattan"] += .5
            else:
                borough_dict["manhattan"] += 1
        if(loc.lower() in nb.queens_neighborhoods or loc.lower() == "queens"):
            borough_dict["queens"] += 1
        if(loc.lower() in nb.bronx_neighborhoods or loc.lower() == "bronx"):
            borough_dict["bronx"] += 1
        if(loc.lower() in nb.brooklyn_neighborhoods or loc.lower() == "brooklyn"):
            borough_dict["brooklyn"] += 1
        if(loc.lower() in nb.staten_island_neighborhoods or loc.lower() == "staten"):
            borough_dict["staten"] += 1

    #return the borough that is most referenced
    return max(borough_dict, key=borough_dict.get)

#connect to NYC Crime Database and find crime listings in given name of borough
def get_crime_data(name_of_borough):
    #connect to NYC Crime Database
    client = Socrata("data.cityofnewyork.us", None)
    #get past days
    last_date = (datetime.datetime.now() + datetime.timedelta(days=-250)).isoformat()

    if(name_of_borough == 'staten'):
        upper_borough = 'STATEN ISLAND'
    else:
        upper_borough = name_of_borough.upper()

    #get all felonies without being throttled
    num_crimes = 0
    for i in range(15):
        offset = 1000 * i
        #build query to get crimes that are within x days and happened in name_of_borough 
        q = "SELECT * WHERE cmplnt_fr_dt > '%s' and boro_nm = '%s' and law_cat_cd = '%s' OFFSET %d" % (last_date, upper_borough, "FELONY", offset)

        #run query
        num_crimes += len(client.get("7x9x-zpz6", query=q))
        
    print(num_crimes)
    client.close()
    return num_crimes


#SCRIPT_START
#----------------------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Get info about local server, chrome driver, headless option')
parser.add_argument('-L', '--local_server_link', required=True, metavar="", help='NLP local server address')
parser.add_argument('-C', '--chrome_driver_path', required=True, metavar="", help="absolute path to chrome driver")
parser.add_argument('-H', '--headless', type=int, metavar="", help="chrome to pop on screen")
args = parser.parse_args()


local_server_link = args.local_server_link #http://localhost:9000
chrome_driver_path = args.chrome_driver_path #/Users/henrywu/Downloads/chromedriver
headless_flag = args.headless


#connect to local NLP server
ner_tagger = CoreNLPParser(url=local_server_link, tagtype='ner')


#opens chrome and goes to airbnb link and expands all elements
options = webdriver.ChromeOptions()
if(headless_flag == None):
    options.add_argument('headless')
driver = webdriver.Chrome(chrome_driver_path, options=options)

urls = read_url_listings("listings.txt")
#dictionary to keep track of listing and crime
links_to_crime = {key: 0 for key in urls}

for url in urls:
    print("\n\n\nGetting webpage...")
    print(url)
    #open webpage
    driver.get(url)
    
    #get extra description details
    button = driver.find_element_by_id('details')
    driver.execute_script("arguments[0].click();", button.find_elements_by_class_name('_ni9axhe')[1])

    #get neighborhood details
    button2 = driver.find_element_by_id('neighborhood')
    driver.execute_script("arguments[0].click();", button2.find_elements_by_class_name('_ni9axhe')[1])
    
    all_text = ""
    #add description details
    for paragraph in button.find_elements_by_class_name('_6z3til'):
        all_text = all_text + " " + paragraph.text

    #add neighborhood info
    for paragraph in button2.find_elements_by_class_name('_6z3til'):
        all_text = all_text + " " + paragraph.text

    print("Tagging text...")
    #get all locations/cities from text on website
    the_list = [x[0] for x in ner_tagger.tag(all_text.split()) if x[1] == 'LOCATION' or x[1] == 'CITY']

    #find the borough
    borough = find_borough(the_list)
    print("\n%s is in %s" % (url, borough.upper()))

    #get crime data for borough
    links_to_crime[url] = get_crime_data(borough)

#sort the listings by crimes that have occurred 
ordered_listings = sorted(links_to_crime.items(), key=lambda x: x[1])
print("\n\nFINAL ORDER IS (also found in ordered.txt): ", ordered_listings)
write_listings_ordered(ordered_listings)

driver.quit()




