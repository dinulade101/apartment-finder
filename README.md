# Apartment Finder

<img src="/screenshots/apartmentfinder.png" width=300>

## About:
Apartment Finder is a **Python bot** created for **busy students** to help them save the _time_ and _effort_ required to find an apartment to rent during school. This bot works with **0 user input**, scraping **Kijiji** to find apartments **tailored** to the student, and notifies them in **real-time** on **Slack**.

This is currently tailored for University of Alberta students, but could be modified to work _anywhere_.


--- 

## Installation:
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

--- 

## Usage:
In ```Settings.py```, you can set up:
+ _MAX_ and _MIN_ price you are willing to pay for rent
+ _MAX_ distance of commute to _university_ and _transit stations_
+ _Location_ of the neighbourhoods you're looking for apartments
+ _Keywords_ you are looking for in the ad, that will be used by our **Natural Language Processing** algorithm to find matches in the ad

In ```listOfLRTStations.txt```, add your local transit stations.

Replace ```edmonton.txt``` with your own city's data, downloaded from [**OpenStreetMap**](http://openstreetmap.org)

---

## How does it work?

### Web Scraping
Web scraping is done using [**BeautifulSoup**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). It scrapes the first 3 pages of Kijiji using the listings’ advertisement ID. The overall idea is that every time the program finds an advertisement ID, it finds that ad listing’s URL and scrapes the listing itself, finding essential information about the listing, such as: Ad description, location, price, how many bathrooms, pet friendliness, if it's furnished, etc. 


### Sanitization
After the program is done scraping, it uses this data and checks it against the user’s specifications. The user can tailor this for their own preferences, by specifying several factors such as rent, distance to University, distance to LRT, number of bathrooms, and other general things people look for in apartments. 


### Graph Theory, because why not?
Even though we could have used Google Maps API to calculate distance between 2 different locations, we wanted to put our **Graph Theory** knowledge to test.

We used [**OpenStreetMap**](http://openstreetmap.org) to create a Graph instance of Edmonton, Alberta by converting the map data to a list of vertices and edges of the city. We extract each listing's postal code while scraping, and pass that into the [**Google Maps API**](https://cloud.google.com/maps-platform/) in order to get a pair of latitude and longitude which is converted to a vertex on the Graph. 

We use **path-finding algorithms** such as **A* algorithm** to find the distance of the **shortest path** to University and the nearest transit station. This algorithm works by loading up the **Binary Heap** with the vertex for the ad's location, and then checking the point's neighbouring vertices and adding them to the heap. We use **Manhattan distance** as our **heuristic** to direct the graph search towards the end point, and **optimize** the search to run as **efficiently** as possible. On the other hand, for transit stations, all the vertices for the transit stations are added to the heap at the start, and a **search tree** builds out from each of the stations to the  vertex corresponding to the ad listing. The first station to be reached is then the **closest**, the search tree stops, and that path is **backtracked** to calculate the required distance. This ensures the most efficient search possible. 

### Natural Language Processing: 
NLP is used to match keywords in the ad to those provided by the user. This will allow the user to instantly see important features they are a looking for in a home.

User can provide keywords such as _discount_ or _school_, and our algorithm will be able to find if these phrases are in the ad and return them to the user.

Before passing the data to the algorithm, unnecessary stop words and symbols are removed and a collection of several synonyms of the extracted words are generated using Wordnet. This allows for optimized results. If a match is found, the algorithm returns the phrase where it's mentioned.

### Slack Helper:
[**Slack API**](https://api.slack.com/) is used to notify the user in real time about any good ad postings that it finds. 

Eligible listings are used to compose a message which is used by the Slackbot to send a message on the Slack Channel. The message is also used by the Google Sheets API to store the listing on Google Sheets.

## The Bot in Action

Below is a screenshot of the Settings.py file and one of several Slack posts created by the bot

Settings.py
```
# set the minimum and maximum prices for the apartments
MIN_PRICE = 0
MAX_PRICE = 1299

#DELAY = 10

# maximum distance away from university
MAX_DIST_TO_UNI = 100

# maximum distance away closest LRT station
MAX_DIST_TO_LRT = 100


# define lat and lon ranges for houses you want to find 
LAT_MIN = 53.395655
LAT_MAX = 53.7160999

LON_MIN = -113.7147381
LON_MAX = -113.2731591


# define keywords to match with Kijij advertisement 
KEYWORDS = ["pets", "smoking", "school", "river", "free", "discount", "animals", "rooms", "internet"]

```
<img src="/screenshots/screenshot4.png" width=500>

As you can see, the bot found a suitable apartment with the distance to the Univeristy of Alberta, as well as a distance to the closest LRT. Moreover, the bot was able to match the KEYWORDS defined in the settings.py file to the description of the advertisement. This finding of keywords is extremely useful as it saves the user from having to check the ad their selves and rather quickly look at a Slack post.

### Google Sheets
For this small project, Google Sheets was used as our "database” in order to store the listings that match up to the user's preferences. 

To set up the API
+ Create a Google sheet
+ Create a project on [Google API manager](https://console.cloud.google.com/apis/dashboard)
+ Add **Google Drive API** to the project 
+ Create your credentials, and use WebServer option and allow application data access
+ Create a service account and assign the role project editor 
+ Download the JSON file and save it as cmput.json in the same directory as the program 
+ Share the sheet with the email in the cmput.json file 


## Future Tasks
Deploy this script on a server online such as Heroku or AWS. 

Replace Google Sheets with MongoDB or Postgresql.

## Creators: 
[Ahmed Elgohary](github.com/ahmedelgohary)

[Dinula De Silva](https://github.com/dinulade101)

## Screenshots: 
<img style="float:left" src="/screenshots/screenshot3.png" width=600>
