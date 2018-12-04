# airbnb_crime_locator
Given NYC airbnb listings, finds recent crimes that have occurred in the area

make sure to download these repositories first:

-java 8

-pip install sodapy
  
-pip install selenium
  
-download chrome driver (place in same directory as this repository)
		  -https://chromedriver.storage.googleapis.com/index.html?path=2.44/
      
-download Stanford NER server (place in same directory as this repository)
		  
  Command to run Stanford NER server:
  
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 &
	
 -pip install nltk
