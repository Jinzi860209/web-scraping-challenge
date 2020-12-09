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
    
    # Get the url for Mars's facts 
    facts_url = "https://space-facts.com/mars/"
    # Use panda's `read_html` to parse the url
    mars_df = pd.read_html(facts_url)[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    html_table = mars_df.to_html()
    # Store the table in the dictionnary
    scraped_data['table'] = html_table

# Mars Hemispheres   
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    hemisphere_image_urls = []

# Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    # Navigate Backwards
        browser.back()
 # Store the list of dictionnaries in the main dictionnary
    scraped_data['hemispheres'] = hemisphere_image_urls
  
    # Close the browser after scraping
    browser.quit()         
    return scraped_data 