# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import Join, TakeFirst, MapCompose


def extract_price(text: str) -> str:
    """
    Extract price from the texted passed in using aa regex expression
    :param text: Item to be parsed
    :type text: Parsed price
    :return:
    :rtype:
    """
    parameter = re.compile(r"£(\d+)")
    try:
        price = parameter.search(text).group(1)

    except:
        price = "N/A"

    return price


def format_price(text: str) -> str:
    """
    A helper function that format the price parsed from the
    price string.

    :param text
    :return: text:string
    """
    # write the search string
    parameter = re.compile(r"£\d+")
    search = parameter.search(text)

    return search.group()


def extract_width(text: str) -> str:
    """
    Extracts with from the text passed in
    :param text:  Scraped text from the meta tag
    :type text: 
    :return: 
    :rtype: 
    """
    sequence = re.compile(r"(\d+)\s*.*[xX]\s*(\d+)")

    try:
     dimension = sequence.search(text).group(1)

    except:
        dimension = 'N/A'

    return dimension

def extract_height(text: str) -> str:
    """                       
    Extracts the height from a text passed in
    :param text:  Scraped text from the scraped respponse
    :type text:               
    :return:                  
    :rtype:                   
    """
    sequence = re.compile(r"(\d+)\s*.*[xX]\s*(\d+)")
    try:
        dimension = sequence.search(text).group(2)

    except:
        dimension = "N/A"

    return dimension


class HeniscraperItem(scrapy.Item):
    """
    An item that inherits from **scrapy.Item** class for performing
    cleaning and storage of scraped data.
    :return item-json/jsonlines/csv file
    """
    url = scrapy.Field()

    title = scrapy.Field()

    media = scrapy.Field()
    #
    height_cm = scrapy.Field(input_processor=MapCompose(extract_height),
                             output_processor=TakeFirst())

    width_cm = scrapy.Field(
        input_processor=MapCompose(extract_height),
        output_processor=TakeFirst())

    # # parse the price using the function defined
    price_gbp = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst())
