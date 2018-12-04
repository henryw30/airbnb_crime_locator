from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.parse import CoreNLPParser
from sodapy import Socrata
import datetime


#read file with airbnb listings to compare
text_file = open("listings.txt", "r")
urls = [x.strip(' ') for x in text_file.read().split(',')]
print(urls)
text_file.close()


manhattan_neighborhoods = {"midtown", "harlem",}



#url = 'https://www.airbnb.com/rooms/14389040?location=New%20York%2C%20NY%2C%20United%20States&s=8y-928Tu'
#url2 = 'https://www.airbnb.com/rooms/891117?adults=0&children=0&infants=0&toddlers=0&s=aEURFR7F'

#connect to local NLP server
ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')


#opens chrome and goes to airbnb link and expands all elements
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome("/Users/henrywu/Downloads/chromedriver", options=options)

for url in urls:
    driver.get(url)
    
    #get extra description details
    button = driver.find_element_by_id('details')
    driver.execute_script("arguments[0].click();", button.find_elements_by_class_name('_ni9axhe')[1])

    #get neighborhood details
    button2 = driver.find_element_by_id('neighborhood')
    driver.execute_script("arguments[0].click();", button2.find_elements_by_class_name('_ni9axhe')[1])
    
    all_text = ""
    #print description details
    for paragraph in button.find_elements_by_class_name('_6z3til'):
        all_text = all_text + " " + paragraph.text
        #print(paragraph.text)
    

    #print neighborhood info
    for paragraph in button2.find_elements_by_class_name('_6z3til'):
        all_text = all_text + " " + paragraph.text
        #print(paragraph.text)

    #the_list = [x for x in ner_tagger.tag(all_text.split())]
    the_list = [x[0] for x in ner_tagger.tag(all_text.split()) if x[1] == 'LOCATION' or x[1] == 'CITY']
    print('\n\n\n\n\n\n')
    print(the_list)
    
driver.quit()
