from bs4 import BeautifulSoup
import requests
from routeFinder import RouteFinder
from slackHelper import SlackHelper
import settings
import sheets
from naturalLanguageProcessing import keyWordFinder


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
        self.bathrooms = None
        self.furnished = None
        self.pets = None
        self.pathToUni = None
        self.dist = None
        self.minStation = None
        self.distToMinStation = None


class Scraper():
    '''
    Class that contains an array of Listing objects.
    Scrapes Kijiji and finds apartments from the first 3 pages, then goes to
    each listing and finds all required information. Stores each listing as a
    "Listing" object, then appends it to the array.
    '''
    def __init__(self):
        self.newRouter = RouteFinder("edmonton.txt")
        self.sp = SlackHelper()
        self.sp.initializeSlackHelper()
        self.sheet = sheets.GoogleSheets()

        self.index = 1
        self.keyWords = ["pet", "patio", "dog", "cat"]

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
        for listing in self.soup.find_all(attrs={"data-ad-id": not None}):
            new_listing = Listing()

            new_listing.id = listing["data-ad-id"]
            new_listing.url = "https://www.kijiji.ca" + listing["data-vip-url"]

            soup = self.get_soup(new_listing.url)  # create a soup for each ad
            try:
                # get required details for the ad
                price = soup.find('span', content=(not None)).get_text()
                title = soup.head.title.get_text()
                desc = soup.find("meta", property="og:description")["content"]
                lat = soup.find("meta", property="og:latitude")["content"]
                lon = soup.find("meta", property="og:longitude")["content"]
                features = soup.find_all("dd")
                bathrooms = features[0].get_text()
                furnished = features[1].get_text()
                pet_friendly = features[2].get_text()

            except:
                continue

            # update data for new_listing
            new_listing.price = price
            new_listing.title = title
            new_listing.desc = desc
            new_listing.lon = lon
            new_listing.lat = lat
            new_listing.bathrooms = bathrooms
            new_listing.furnished = furnished
            new_listing.pets = pet_friendly

            # add to array
            self.listings.append(new_listing)

            print(title)

            if int(new_listing.price[1:].replace(',', '')[:-3]) < settings.MIN_PRICE:
                continue
            if int(new_listing.price[1:].replace(',', '')[:-3]) > settings.MAX_PRICE:
                continue
            if (float(lon) > settings.LON_MAX or float(lon) < settings.LON_MIN):
                continue
            if (float(lat)> settings.LAT_MAX or float(lat) < settings.LAT_MIN):
                continue

            try:
                new_listing.pathToUni, new_listing.dist, new_listing.minStation, new_listing.distToMinStation = self.newRouter.computePathToUni((
                                (float(lat)*100000), (float(lon)*100000)))
            except:
                continue

            message = '{0} {1} \n *Distance to UNI:* {2:.2f}  \n *Closest LRT:* {3} {4:.2f} km away \n *Number of Bathrooms:* {5} \n *Furnished:* {6} \n *Pet Friendly:* {7} \n'.format(title,
             price, new_listing.dist, new_listing.minStation, new_listing.distToMinStation, new_listing.bathrooms, new_listing.furnished, new_listing.pets)


            try:
                kw = keyWordFinder(new_listing.url)
                foundWords = kw.findKeyWords(settings.KEYWORDS)

                if foundWords:
                    message += "*We found the following sentence snippets:* \n"
                    for word in foundWords:
                        message += str(word) + "\n"
            except:
                continue


            if int(new_listing.distToMinStation) > settings.MAX_DIST_TO_LRT:
                continue
            if int(new_listing.dist) > settings.MAX_DIST_TO_UNI:
                continue

            messageArrayForSheets = [str(title),str(price),str(new_listing.dist), str(new_listing.minStation), str(new_listing.distToMinStation), str(new_listing.bathrooms), str(new_listing.furnished), str(new_listing.pets)]
            self.sheet.add_apartment(messageArrayForSheets, self.index)
            self.index += 1
            self.sp.postMessage(message)


if __name__ == '__main__':
    kijiji = Scraper()
