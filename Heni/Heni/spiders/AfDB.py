# import scrapy
# from ..items import HealthnewsscraperItem
# from scrapy.loader import ItemLoader
#
#
# class AfdbSpider(scrapy.Spider):
#     """
#     A basic template spider class created using the command:
#     **scrapy genspider spidername domain**. This Spider crawls and
#     scrapes links from African Development Bank, and scrapes data from
#     links crawled.
#     Outputs data as JSON files with 4 attributes: link, headline,
#     body, date.
#
#     This class inherits behaviour from scrapy.Spider class.
#     """
#
#     name = "AfDB"
#
#     # Domain allowed for managing redirects
#     allowed_domains = ["afdb.org"]
#
#     # Url to begin scraping
#     start_urls = ["https://www.afdb.org/en/search/content/Nigeria?title=&type_1=news"]
#
#     # spider specific settings
#     custom_settings = {
#         "FEEDS": {"./HealthNewsScraper/scrapes/afdb.jl": {"format": "jsonlines"}},
#     }
#
#     def parse(self, response):
#         """
#         Parses the response gotten from the start URL.
#         It retrieves the next page's link and stores it as a response.
#         Outputs a request object.
#         @url https://www.afdb.org/en/search/content/Nigeria?title=&type_1=news
#         @returns requests 1
#         @scrapes link title body date_published
#         :param response:
#         :return: generator
#         """
#
#         # Retrieve pagination DOM
#         pagination_dom = response.css("div.text-center ul.pagination")
#
#         # use item to verify next page link
#         verify_next_page = pagination_dom.css("li.next")
#
#         # retrieve next page link
#         next_page_link = verify_next_page.css("a::attr(href)").get()
#
#         # make full link
#         full_next_page_link = response.urljoin(next_page_link)
#
#         yield from self.scrape(response)
#
#         # check if next page is available
#         if verify_next_page:
#
#             # yield scrapy request
#             yield scrapy.Request(full_next_page_link, callback=self.parse)
#
#     def scrape(self, response):
#         """
#         A function which takes a response and returns the individual news article links
#         present in the response.
#         :param response
#         :return: request, request.meta['item']- list
#         """
#
#         # article DOM
#         article_dom = response.css(
#             "div.view-content div.views-row div.views-field span.field-content"
#         )
#
#         # Loop through the article DOM to retrieve links
#         for individual_news_link in article_dom.css("a::attr(href)").getall():
#
#             # make full link
#             full_individual_news_link = response.urljoin(individual_news_link)
#
#             # make request to the news_reader function
#             request = scrapy.Request(
#                 full_individual_news_link, callback=self.news_reader
#             )
#             request.meta["item"] = full_individual_news_link
#             yield request
#
#     @staticmethod
#     def news_reader(response):
#         """
#         A function that reads individual news articles collecting the headline,
#         date and news body.
#         :param response
#         :returns: populated item loader- json/csv/jsonlines
#         """
#
#         # Instantiate an Item Loader to populate various fields and person data cleaning
#         news_item_loader = ItemLoader(item=HealthnewsscraperItem(), response=response)
#
#         # Populate the link, title, body and Date Fields
#         news_item_loader.add_value("link", response.meta["item"])
#         news_item_loader.add_css(
#             "title", "div.page-main-content section h1.page-header ::text"
#         )
#         news_item_loader.add_css("body", "div.field-item.even p *::text")
#         news_item_loader.add_css("date_published", "div.field-item.even span ::text")
#
#         yield news_item_loader.load_item()
