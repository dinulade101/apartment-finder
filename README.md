# Apartment Finder

## About:
Apartment Finder is a Python bot that scrapes Kijiji and finds apartments tailored for the user, according to their preferences.

---
## How does it work?
### Web Scraping
Web scraping was done using BeautifulSoup4. It scrapes the first 3 pages of Kijiji using the listings’ advertisement ID. The overall idea is that every time the program finds an advertisement ID, it finds that ad listing’s URL and then scrapes the listing itself, in order to find essential information about the listing, such as: Ad description, location, price, how many bathrooms, pet friendliness, if it's furnished, etc. 

### Sanitization
After the program is done scraping, it uses this data and checks it against the user’s specifications. The user can tailor this for their own preferences, by specifying several factors such as rent, distance to University, distance to LRT, number of bathrooms, and other general things people look for in apartments. 

### Graph Theory, because why not?
After the scraping running and getting all the required data, data such as the ad’s location is used to then calculate the distance using the ‘Route Finding’ program, which utilizes A* algorithm to provide a quick way of finding the distances. After everything is calculated and all the data is checked and is up to the required specifications, all the eligible listings are then used to compose a message. This message is then used by a Slackbot to promptly notify the user on a Slack Channel that a new listing exists. The message is also used by a Google Sheets API in order to store the listing on Google Sheets as means of having a backend database to store all the listings that we liked.<br/><br/>
Route Finding:<br/>
The route finder allows for the calculation of the shortest route from a house or apartment to a selected University, as well as closest LRT station. The route finder class can be initialized with a text file containing the vertices and edges in a city. Although currently the program is tested only for Edmonton, the necessary functions are ready so that other cities can be added as well. After the object of the Route Finder class is created, several functions are available for calculating the shortest route. Currently, the function called computePathToUni calculate the shortest distance to the University, as well as finds the closest LRT station.
To determine the shortest distance to the University, the A* algorithm is utilized. For this algorithm, we load up the heap with the start location, and then keep on adding to the heap after checking a point’s neighbors. Moreover, as a heuristic for the A* algorithm, we use euclidean distance to direct the graph search towards the end point, and help make the search run faster. The LRT route finding is done using a similar technique. However, for the LRT’s, all the locations of LRTs are added to the heap at the start, and a search tree builds out from each of the station locations to the home under consideration. The first LRT station to be reached is then the closest, and the path can be traced back to calculate the distance from the LRT station to the house. 
The route finder class contains several important helper functions as well. For instance, convertLatLonDistToMetres converts the distance between two coordinates given in latitudes and longitudes to km. Moreover, the load city graph can parse through a text file containing the vertices and edges of a particular city, and build a graph out of them.<br/>  
Slack Helper:<br/>
The slack helper class utilizes the Python Slack API to connect with the correct Slack channel and login, and then post text messages. This is used in order to promptly notify the user of any listings, so that the user can only check the listings that the Slack Bot spits out into the channel. <br/><br/>
Google Sheets<br/>
We use the Google Sheets API as means of a “backend database” in order to store all the listings that the user might like. This is just for storing the listings, and not notify the user. The user can go any time onto the Google Sheets in order to look at the past listings.<br/><br/>
To setup Google Sheets: 1) create a google sheet and named it however you like 2) Go to Google API manager and create a project 3) Add Google Drive API to the project 4) Create credentials to access this API, use webserver option and give access to application data 5) Create a service account and assign the role project editor 6) Download the JSON file and save it as cmput.json in same directory as program 7) go to your sheet and choose to share the sheet to the email in the cmput.json file. <br/><br/>
Natural Language Processing: <br/>
This class is used to match keywords in the ad to those provided by the user. This will allow the user to instantly see important features they are a looking for in a home. For example, consider the following screenshot: <br/><br/>

In this example, the user provided keywords like “discount” and “school,” and the natural language processing was able to find a phrases in the ad that matched these keywords, and return them. <br/><br/>
This class is initialized with the URL whose text needs to be analyzed (in this case, the URL of the Kijiji ad). Then BeautifulSoup is utilized to extract the ad’s description, and clean the HTML tags. Moreover, unnecessary stop words and symbols are removed as well. Then, a collection of several synonyms of the extracted words are generated as well using Wordnet. This will allow for the best matching with the key words provided to the program. If a match is found, the found word, as well several surrounding words for context are returned as well. <br/><br/>

## Install Instructions:
+ Clone this repo
+ Pip3 already comes with Python3, however if its not available, download and install it also well . <br/>
+ Install Slack Developer Kit 
``` pip install slackclient ```
+ Install the Natural Language Processing Library
``` sudo pip install -U nltk ```
+ Download nltk (first time only): 

```python3 
import nltk
nltk.download() 
```
+ Run using 

```SLACK_BOT_TOKEN="yourslackbottoken" python3 scraper.py``` 

## Future Tasks
Deploy this script on a server online such as Heroku or AWS. 
Replace Google Sheets with MongoDB or Postgresql
