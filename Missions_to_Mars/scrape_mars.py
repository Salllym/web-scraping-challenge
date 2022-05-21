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
  # @NOTE: Replace the path with your actual path to the chromedriver
  executable_path = {'executable_path': ChromeDriverManager().install()}
  return Browser("chrome", **executable_path, headless=False)


def scrape_all():

  browser = init_browser()

  mars_data = {}
  sleep_timer = 2


  # Mars News
  # connect to NASA Mars news Site
  url = "https://redplanetscience.com/"

  # Retrieve page with the requests module
  browser.visit(url)
  response = requests.get(url)

  # Create BeautifulSoup object; parse with 'html.parser'
  html=browser.html
  soup = BeautifulSoup(html, 'html.parser')

  # Examine the results, determine elements that contains sought info.
  article = soup.find("div", class_ = "list_text")
  news_title = article.find("div", class_="content_title").text
  news_p = article.find("div", class_="article_teaser_body").text
      
  # result to mongoDB dictionary
  mars_data['news_title'] = news_title
  mars_data['news_p'] = news_p



  # JPL Mars Space Images 
  # Visit and set url
  url = 'https://spaceimages-mars.com/'
  browser.visit(url)

  # Create BeautifulSoup object; parse with 'html.parser'
  html=browser.html
  soup = BeautifulSoup(html, 'html.parser')

  # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
  browser.find_by_css("a.showimg").first.click()
  time.sleep(2)

    # Create BeautifulSoup object; parse with 'html.parser'
  html=browser.html
  soup = BeautifulSoup(html, 'html.parser')

  # Need more info to find image url
  image_url = browser.find_by_css("img.fancybox-image")["src"]

  # result to mongoDB dictionary
  mars_data['featured_image'] = image_url



  #Mars Facts
  # Visit and set url
  url = 'https://galaxyfacts-mars.com/'
  browser.visit(url)

  # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
  mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]

  # Clean up DataFrame, set index
  mars_facts_df.columns=["Planet Profile", "Value"]
  mars_facts_df.set_index("Planet Profile", inplace=True)
  mars_facts_html_table = mars_facts_df.to_html()
  mars_facts_html_table = mars_facts_html_table.replace('\n','')

  # result to mongoDB dictionary
  mars_data['mars_facts'] = mars_facts_html_table



  # Mars Hemispheres
  # Visit and set url
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

  # result to mongoDB dictionary
  mars_data["hemispheres"] = hemisphere_img_urls

  browser.quit()

  return mars_data

mars_data = scrape_all()

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars
collection = db.mars

# Dictionary to be inserted as a MongoDB document
collection.update_one({}, {"$set": mars_data}, upsert=True)





