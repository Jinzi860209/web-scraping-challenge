# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"C:/Users/pahou/.wdm/drivers/chromedriver/win32/87.0.4280.20/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    # Create a dictionary that can hold evertyhing then imported into Mongo
scraped_data = {}

# NASA MARS NEWS
def scrape():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        scraped_data['news_title'] = news_title
        scraped_data['news_paragraph'] = news_p
        # Close the browser after scraping
        browser.quit()

#Featured Iamge
    #Get the featured image and description
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
    # HTML Object 
        html = browser.html

# Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

# use beautifulsoup to navigate to the image
        image_url = soup.find("li", class_="slide").a["data-fancybox-href"]
# Website Url 
        main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
        featured_image_url = main_url + image_url

#Store the image in the dictionary
        scraped_data['featured_image_url'] = featured_image_url

#Mars Facts
#         