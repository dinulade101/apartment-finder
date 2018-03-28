from bs4 import BeautifulSoup
import requests
# maybe add googlemaps


class Listing():
    def __init__(self):
        self.id = None
        self.lon = None
        self.lat = None
        self.url = None
        self.desc = None
        self.price = None
        self.title = None


class Scraper():
    def __init__(self):
        self.listings = []
        self.start()

    def start(self):
        for i in range(1, 4):
            url = self.get_url(i)
            self.soup = self.get_soup(url)
            self.get_listings()

    def get_url(self, page):
        url = ("https://www.kijiji.ca/b-apartments-condos/page-{}".format(page)
                + "/edmonton/c37l1700203")
        return url

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def get_listings(self):
        for listing in self.soup.find_all(attrs={"data-ad-id": not None}):
            new_listing = Listing()

            new_listing.id = listing["data-ad-id"]
            new_listing.url = "https://www.kijiji.ca" + listing["data-vip-url"]

            soup = self.get_soup(new_listing.url)

            price = soup.find('span', content=(not None)).get_text()
            title = soup.head.title.get_text()
            desc = soup.find("meta", property="og:description")["content"]
            lat = soup.find("meta", property="og:latitude")["content"]
            lon = soup.find("meta", property="og:longitude")["content"]

            new_listing.price = price
            new_listing.title = title
            new_listing.desc = desc
            new_listing.lon = lon
            new_listing.lat = lat

            self.listings.append(new_listing)


if __name__ == '__main__':
    kijiji = Scraper()
    # try:
    #     kijiji = Scraper()
    # except:
    #     raise Exception("Failed to scrape Kijiji!")
