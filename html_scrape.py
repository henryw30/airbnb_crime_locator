from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.parse import CoreNLPParser
from sodapy import Socrata
import datetime
import neighborhoods as nb

#reads url listings from listings.txt
def read_url_listings(path_to_listings):
    #read file with airbnb listings to compare
    text_file = open(path_to_listings, "r")
    urls = [x.strip(' ') for x in text_file.read().split(',')]
    text_file.close()
    return urls

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
    last_date = (datetime.datetime.now() + datetime.timedelta(days=-160)).isoformat()

    if(name_of_borough == 'staten'):
        upper_borough = 'STATEN ISLAND'
    else:
        upper_borough = name_of_borough.upper()

    #build query to get crimes that are within x days and happened in name_of_borough 
    q = "SELECT * WHERE cmplnt_fr_dt > '%s' and boro_nm = '%s'" % (last_date, upper_borough)

    #run query
    num_crimes = len(client.get("7x9x-zpz6", query=q))
    client.close()
    return num_crimes


#connect to local NLP server
ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')


#opens chrome and goes to airbnb link and expands all elements
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome("/Users/henrywu/Downloads/chromedriver", options=options)

urls = read_url_listings("listings.txt")
#dictionary to keep track of listing and crime
links_to_crime = {key: 0 for key in urls}

for url in urls:
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

    #get all locations/cities from text on website
    the_list = [x[0] for x in ner_tagger.tag(all_text.split()) if x[1] == 'LOCATION' or x[1] == 'CITY']
    print('\n\n\n')
    print(the_list)
    print('\n')
    borough = find_borough(the_list)
    print(borough)

    links_to_crime[url] = get_crime_data(borough)

write_listings_ordered(sorted(links_to_crime.items(), key=lambda x: x[1]))

driver.quit()




