from bs4 import BeautifulSoup
import requests
from routeFinder import RouteFinder
from slackHelper import SlackHelper
# maybe add googlemaps


class Listing():
    '''
    Class used to define a Listing, and stores all of the listings properties such as:
    Title, Advertisement ID, Longitude, Latitude, URL, Description, Price.
    '''
    def __init__(self):
        self.id = None
        self.lon = None
        self.lat = None
        self.url = None
        self.desc = None
        self.price = None
        self.title = None


class Scraper():
    '''
    Class that contains an array of Listing objects.
    Scrapes Kijiji and finds apartments from the first 3 pages, then goes to
    each listing and finds all required information. Stores each listing as a
    "Listing" object, then appends it to the array.
    '''
    def __init__(self):
        self.listings = []  # an array that will contain all the Listings
        self.start_scraping()

    def start_scraping(self):
        for i in range(1, 4):
            url = self.get_url(i)  # get the url of 3 different pages
            self.soup = self.get_soup(url)  # soupify
            self.get_listings()  # use the soup to get listings on that page

    def get_url(self, page):
        url = ("https://www.kijiji.ca/b-apartments-condos/page-{}".format(page)
               + "/edmonton/c37l1700203")
        return url

    def get_soup(self, url):
        # function that gets the soup for that url
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def get_listings(self):
        # scrapes through kijiji page to find all the listings
        counter = 5
        for listing in self.soup.find_all(attrs={"data-ad-id": not None}):
            counter -= 1
            if counter == 0:
                break
            new_listing = Listing()

            new_listing.id = listing["data-ad-id"]
            new_listing.url = "https://www.kijiji.ca" + listing["data-vip-url"]

            soup = self.get_soup(new_listing.url)  # create a soup for each ad

            # get required details for the ad
            price = soup.find('span', content=(not None)).get_text()
            title = soup.head.title.get_text()
            desc = soup.find("meta", property="og:description")["content"]
            lat = soup.find("meta", property="og:latitude")["content"]
            lon = soup.find("meta", property="og:longitude")["content"]

            # update data for new_listing
            new_listing.price = price
            new_listing.title = title
            new_listing.desc = desc
            new_listing.lon = lon
            new_listing.lat = lat

            # add to array
            '''
            print(float(new_listing.lon)*100000, float(new_listing.lat)*100000)
            newRouter = RouteFinder("edmonton.txt")
            sp = SlackHelper()
            sp.initializeSlackHelper()
            try:
                print(((float(new_listing.lon)*100000), (float(new_listing.lat)*100000)))
                pathToUni, dist = newRouter.computePathToUni(((float(new_listing.lon)*100000), (float(new_listing.lat)*100000)))
                message = '{} {} {} {}'.format(new_listing.title, new_listing.price,"Distance to UNI", dist)
                sp.postMessage(message)
                print("number of waypoints:", len(pathToUni), "distance (in iterms in lat lot)", dist)
                #pathToUni = newRouter.computePathToUni((,(-11350793.73),(5348479.89)))
            except:
                print("error")
            '''
            self.listings.append(new_listing)


if __name__ == '__main__':
    newRouter = RouteFinder("edmonton.txt")
    sp = SlackHelper()
    sp.initializeSlackHelper()
    
    try:
        kijiji = Scraper()
        #print(kijiji.listings)
        for i in kijiji.listings:
            try:
                print(((float(i.lat)*100000), (float(i.lon)*100000)))
                pathToUni, dist, minStation = newRouter.computePathToUni(((float(i.lat)*100000), (float(i.lon)*100000)))
                message = '{} {} "Distance to UNI" {} Closest LRT and distance {} {}'.format(i.title, i.price, dist, minStation[0], minStation[1])
                sp.postMessage(message)
                print("number of waypoints:", len(pathToUni), "distance (in iterms in lat lot)", dist)
                #pathToUni = newRouter.computePathToUni((,(-11350793.73),(5348479.89)))
            except:
                print("error")
    except:
        pass # who gives a shit
