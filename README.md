# Apartment Finder

## What is this?
Apartment Finder is a python bot that scrapes Kijiji.com in order to find apartments within a certain price range. 

---
Apartment Finder
What is this?
Apartment Finder is a python bot that scrapes Kijiji.com in order to find apartments within a certain price range.
Install Instructions:
Download the provided .zip file containing the main program directory
Pip3 already comes with Python3, however if its not available, download and install it also well . 
Run pip install slackclient in terminal to install Slack Developer Kit for python 
Run sudo pip install -U nltk to install the natural language processing library 
Now enter python3 into terminal
Type in import nltk and press enter
Enter nltk.download() and download click Download with “All” selected 
Ahmed, talk about BeutifulSoup and url.lib stuff 
Finally to run program, change terminal directory to directory containing “scraper.py”. 
For ex. cd /Users/dinula/repos/apartment-finder/src
Run 
SLACK_BOT_TOKEN="####" python3 scraper.py
This command is crucial to run program because without it, the Slack API will not have the necessary token to connect with Slack servers. Now the program should be running and scraping apartments. These will be posted on both Slack and Google Sheets. 
To join the Slack and see the posted apartments, please use this link:
https://join.slack.com/t/cmput275project/shared_invite/enQtMzQ3NzQ4MTYwNDAzLWI1OGVhYmU4ZjAwNzI5YzBkNWI5MmFiMjU3OTNmYWJiYmM2YmFmNGNlZmY2MDY0OTk1ZWVhNDdjYmQyZGY0OWI
 
 
Web Scraping:
Web scraping was done entirely using the Python BeautifulSoup4 library. It was programmed in such a way that it scrapes the first 3 pages of Kijiji using the listings’ advertisement ID. How BeautifulSoup works is by requesting the page using the python requests library, and then fetching the html data and parsing it as html data. The generic Kijiji URL is built into the program, and then it formats every iteration in order to calculate the URL for the next page. After the URL for the next page is made, we use the requests library and the “get” function in order to get the html data. After parsing this data, we create a BeautifulSoup object. The overall idea is that Every time it finds an advertisement ID, it finds that ad listing’s URL and then scrapes the listing itself, in order to find a few required information about the listing, which are: the ad title, description, location, price, how many bathrooms, pet friendly, furnished or not, etc. After the program is done scraping the first 3 pages, it then uses this data and checks it against the user’s specifications. This allows the user to give their own specifications, such as the maximum rent they want to pay, the maximum distance from the University, maximum distance from LRT, etc. After the scraping running and getting all the required data, data such as the ad’s location is used to then calculate the distance using the ‘Route Finding’ program, which utilizes A* algorithm to provide a quick way of finding the distances. After everything is calculated and all the data is checked and is up to the required specifications, all the eligible listings are then used to compose a message. This message is then used by a Slackbot to promptly notify the user on a Slack Channel that a new listing exists. The message is also used by a Google Sheets API in order to store the listing on Google Sheets as means of having a backend database to store all the listings that we liked.
Route Finding:
The route finder allows for the calculation of the shortest route from a house or apartment to a selected University, as well as closest LRT station. The route finder class can be initialized with a text file containing the vertices and edges in a city. Although currently the program is tested only for Edmonton, the necessary functions are ready so that other cities can be added as well. After the object of the Route Finder class is created, several functions are available for calculating the shortest route. Currently, the function called computePathToUni calculate the shortest distance to the University, as well as finds the closest LRT station.
To determine the shortest distance to the University, the A* algorithm is utilized. For this algorithm, we load up the heap with the start location, and then keep on adding to the heap after checking a point’s neighbors. Moreover, as a heuristic for the A* algorithm, we use euclidean distance to direct the graph search towards the end point, and help make the search run faster. The LRT route finding is done using a similar technique. However, for the LRT’s, all the locations of LRTs are added to the heap at the start, and a search tree builds out from each of the station locations to the home under consideration. The first LRT station to be reached is then the closest, and the path can be traced back to calculate the distance from the LRT station to the house. 
The route finder class contains several important helper functions as well. For instance, convertLatLonDistToMetres converts the distance between two coordinates given in latitudes and longitudes to km. Moreover, the load city graph can parse through a text file containing the vertices and edges of a particular city, and build a graph out of them.  
Slack Helper:
The slack helper class utilizes the Python Slack API to connect with the correct Slack channel and login, and then post text messages. This is used in order to promptly notify the user of any listings, so that the user can only check the listings that the Slack Bot spits out into the channel. 
Google Sheets
We use the Google Sheets API as means of a “backend database” in order to store all the listings that the user might like. This is just for storing the listings, and not notify the user. The user can go any time onto the Google Sheets in order to look at the past listings.
To setup Google Sheets: 1) create a google sheet and named it however you like 2) Go to Google API manager and create a project 3) Add Google Drive API to the project 4) Create credentials to access this API, use webserver option and give access to application data 5) Create a service account and assign the role project editor 6) Download the JSON file and save it as cmput.json in same directory as program 7) go to your sheet and choose to share the sheet to the email in the cmput.json file. 
Natural Language Processing:
This class is used to match keywords in the ad to those provided by the user. This will allow the user to instantly see important features they are a looking for in a home. For example, consider the following screenshot: 

In this example, the user provided keywords like “discount” and “school,” and the natural language processing was able to find a phrases in the ad that matched these keywords, and return them. 
This class is initialized with the URL whose text needs to be analyzed (in this case, the URL of the Kijiji ad). Then BeautifulSoup is utilized to extract the ad’s description, and clean the HTML tags. Moreover, unnecessary stop words and symbols are removed as well. Then, a collection of several synonyms of the extracted words are generated as well using Wordnet. This will allow for the best matching with the key words provided to the program. If a match is found, the found word, as well several surrounding words for context are returned as well. 
Future Improvements:

In the future, we want to deploy this script on a server online such as Heroku or AWS in order to have it run in the background with 0 user input. This is our true vision for this application, where the user can just have this script run in the background and it would output all the nice listings while the busy user can freely do anything else and not have to spend time looking for listings. 
We would also want to use a database such as Postgresql or MySQL in order to store the listings, and to see if we could utilize the database better than Google Sheets.
