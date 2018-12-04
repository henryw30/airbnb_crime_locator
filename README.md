# airbnb_crime_locator
Given NYC airbnb listings, finds recent crimes that have occurred in the area


# Installation
make sure to download these repositories first:

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
		  
Command to run Stanford NER server:
  
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 &
	
