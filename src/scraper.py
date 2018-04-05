from bs4 import BeautifulSoup
import requests
from routeFinder import RouteFinder
from slackHelper import SlackHelper
import settings
import sheets

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
            except:
                continue
            # update data for new_listing
            new_listing.price = price
            new_listing.title = title
            new_listing.desc = desc
            new_listing.lon = lon
            new_listing.lat = lat

            # add to array
            self.listings.append(new_listing)


if __name__ == '__main__':
    newRouter = RouteFinder("edmonton.txt")
    sp = SlackHelper()
    sp.initializeSlackHelper()
    index = 0
    print("here")
    kijiji = Scraper()
    sheet = sheets.GoogleSheets()

    for i in kijiji.listings:
        print(i.title)
        pathToUni, dist, minStation = newRouter.computePathToUni((
                        (float(i.lat)*100000), (float(i.lon)*100000)))

        message = '{} {} "Distance to UNI" {} Closest LRT and distance {} {}'.format(i.title, i.price, dist, minStation[0], minStation[1])

        if int(i.price[1:].replace(',', '')) < settings.MIN_PRICE:
            continue
        if int(i.price[1:].replace(',', '')) > settings.MAX_PRICE:
            continue
        if int(minStation[1]) > settings.MAX_DIST_TO_LRT:
            continue
        if int(dist) > settings.MAX_DIST_TO_UNI:
            continue

        sheet.add_apartment(message.split(), index)
        index += 1
        sp.postMessage(message)

    # except Exception as e:
    #     print("error2 {}".format(e))
