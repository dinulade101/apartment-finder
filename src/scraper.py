from bs4 import BeautifulSoup
import


class Listing():
    def __init__(self, id, title, lon, lat, url, desc, price):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.url = url
        self.desc = desc
        self.price = price
        self.title = title


class Scraper():
    def __init__(self):
        url = "https://www.kijiji.ca/b-apartments-condos/edmonton/c37l1700203"
        self.soup = self.get_soup(url)
        self.listings = []

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def get_listings(self):
        for listing in self.soup.find_all(attrs={"data-ad-id": not None}):
            new_listing = Listing()
            new_listing.id = listing["data-ad-id"]
            new_listing.url = "https://www.kijiji.ca" + listing["data-vip-url"]

            soup = self.get_soup(listing_url)
            new_listing.price = soup.find('span', content=(not None)).get_text()
            new_listing.title = soup.head.title.get_text()
            new_listing.desc = soup.find("meta", property="og:description")["content"]
            new_listing.lat = soup.find("meta", property="og:latitude")["content"]
            new_listing.lon = soup.find("meta", property="og:longitude")["content"]

            # listing_dict = {
            #     id: listing_id,
            #     lon: listing_lon,
            #     lat: listing_lat,
            #     url: listing_url,
            #     price: listing_price
            # }


if __name__ == '__main__':
    pass
