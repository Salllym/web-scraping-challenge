#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

#Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests
import pprint 
from IPython.display import Markdown, display
import pymongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
	executable_path = {"executable_path":"webdriver/chromedriver"}
	return Browser("chrome", **executable_path, headless = False)

def mars_news(): 
    # connect to NASA Mars news Site
    url = 'https://redplanetscience.com/'

    # Retrieve page with the requests module
    browser.visit(url)

    response = requests.get(url)

    html=browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Examine the results, determine elements that contains sought info.
    #print(soup.prettify())

    article = soup.find("div", class_ = "list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

#     print(f'------------------------------------------------')
#     print(f'TITLE: {news_title}')
#     print(f'------------------------------------------------')
#     print(f'PARAGRAPH: {news_p}')
     
    return news_title, news_p


# JPL Mars Space Images 
def featured_image():
    # Visit the url for JPL Featured Space Image
    # Set URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html=browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    browser.find_by_css("a.showimg").first.click()
    time.sleep(2)

    #parse html page with BeautifulSoup
    html=browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Need more info to find image url
    image_url = browser.find_by_css("img.fancybox-image")["src"]
    return image_url


def mars_facts():
    # Visit the Mars Facts webpage
    # Set URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    #print(mars_facts_df)

    # Clean up DataFrame, set index
    mars_facts_df.columns=["Planet Profile", "Value"]
    mars_facts_df.set_index("Planet Profile", inplace=True)
    mars_facts_html_table = mars_facts_df.to_html()
    mars_facts_html_table = mars_facts_html_table.replace('\n','')
    return mars_facts_html_table


# Mars Hemispheres
def hemisphere_image_urls():
    # Visit the Astrogeology site
    # Set URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    mars_weather_soup = BeautifulSoup(html, "html.parser")


    # Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name
    soup1 = BeautifulSoup(html, "html.parser")
    items = soup1.find_all("div", class_="item")

    hemisphere_img_urls = []

    for item in items:

        title = item.find("h3").text
        link = item.find("a", class_="itemLink")["href"]
        hemispherelink = url + link
        browser.visit(hemispherelink)
        hemispherehtml = browser.html

        soup2 = BeautifulSoup(hemispherehtml, "lxml")
        image = soup2.find("img", class_="wide-image")["src"]
        imageurl = url + image
        hemisphere = {}

        hemisphere_img_urls.append({"title":title,"img_url":imageurl})

        browser.back()


    # Use a Python dictionary to store the data using the keys `img_url` and `title`
    return hemisphere_img_urls


# Scrape All
def scrape_all():
    # Initiate headless driver for deployment
#     executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news()
#     image_url = featured_image()
#     mars_facts_df = mars_facts()
#     hemisphere_img_urls = hemisphere_img_urls()

     # Run all scraping functions and store results in a dictionary
    mars_data = {
        "news_title": news_title,
         "news_p": news_p,
        "featured_image": featured_image(),
        "mars_facts": mars_facts(),
        "hemispheres": hemisphere_image_urls()}
    
    browser.quit()
    return mars_data


