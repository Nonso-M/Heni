import scrapy
from ..items import HeniscraperItem
from scrapy.loader import ItemLoader
import json


class BearspaceSpider(scrapy.Spider):
    """
    A basic template spider class created using the command:
    **scrapy genspider spidername domain**. This Spider crawls and
    scrapes links from African Development Bank, and scrapes data from
    links crawled.
    Outputs data as JSON files with 4 attributes: link, headline,
    body, date.
    This class inherits behaviour from scrapy.Spider class.
    """

    name = 'bearspace'

    # Domain allowed for managing redirects
    allowed_domains = ['www.bearspace.co.uk']

    # Url to begin scraping
    start_urls = ['http://www.bearspace.co.uk/purchase']

    button = None
    start_page = 1
    articles_no = 0
    custom_settings = {
        'FEEDS': {'./Heni/data/products.csv': {'format': 'csv', }}
    }

    def parse(self, response):
        """
        This method parsers all the links on website and extract the
        needed informations using callbacks
        :param response
        :return: request, request.meta['item']- list
        """
        # scrapes response on the current page
        yield from self.scrape(response)

        # Checks for the availability of the 'load more button'
        self.button = response.css("button.txtqbB").get()

        # If the button is still available, keep scraping
        if self.button is not None:
            self.articles_no += 20
            current_url = self.start_urls[0] + f'?page={self.start_page + 1}'
            self.start_page += 1
            yield scrapy.Request(current_url, callback=self.parse)

    def scrape(self, response):
        """
        A function which takes a response and returns the individual news article links
        present in the response.
        :param response
        :return: request, request.meta['item']- list
        """

        article_dom = response.css(
            "div.pNCdXj section[data-hook='product-list']"
        )

        # self.button = response.css("button.txtqbB").get()
        # Loop through the article DOM to retrieve links
        for product_url in article_dom.css(
                "li[data-hook=product-list-grid-item] a.oQUvqL::attr(href)").getall()[
                           self.articles_no:]:

            # make request to the news_reader function
            request = scrapy.Request(
                product_url, callback=self.product_parser,
                meta={"url": product_url}
            )
            yield request

    @staticmethod
    def product_parser(response):
        """
        A function that reads individual news articles collecting the headline,
        date and news body.
        :param response
        :returns: populated item loader- json/csv/jsonlines
        """

        # Instantiate an Item Loader to populate various fields and person data cleaning
        product_item_loader = ItemLoader(item=HeniscraperItem(),
                                         response=response)

        data = response.css(
            "meta[property='og:description']::attr(content)").get()

        media = response.css("div._1TImB pre._28cEs p::text").get()

        # In case the above query returns an empty list
        if not media:
            media = response.css("div._1TImB pre._28cEs p span::text").get()

        #
        # # height, width = [x.strip() for x in parse_list[1].split('x')]
        price = response.css(
            "span[data-hook='formatted-primary-price']::text").get()
        json_text = response.css("script#wix-warmup-data::text").get()

        # height, width, price = self.parse_price(json_text)

        # Populate the link, title, body and Date Fields
        product_item_loader.add_value("url", response.meta["url"])
        product_item_loader.add_css("title", "div._1TImB h1._2qrJF::text")
        product_item_loader.add_value("media", media)
        product_item_loader.add_value("height_cm", data)
        #
        product_item_loader.add_value("width_cm", data)
        product_item_loader.add_value('price_gbp', data)
        yield product_item_loader.load_item()

    # @staticmethod
    # def parse_price(text):
    #     """
    #     Parses the price from the json in the script tag and returns the actual price
    #     :return: Price of the art
    #     :rtype:
    #     """
    #     json_obj = json.loads(text)
    #     key1 = list(json_obj["appsWarmupData"].keys())[0]
    #     key2 = list(json_obj["appsWarmupData"][key1].keys())[0]
    #     products = json_obj["appsWarmupData"][key1][key2]["catalog"]["product"]
    #
    #     # parse the height and width and price
    #     height = products["media"][0]["width"]
    #     width = products["media"][0]["height"]
    #     price = str(int(products["price"] / 10))
    #
    #     yield height, width, price
