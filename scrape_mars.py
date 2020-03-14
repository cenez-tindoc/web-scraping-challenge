#import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import time
import re

def scrape():
    mars_dict = {}

    executable_path = {"executable_path":"chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless = False)

#scrape the NASA Mars News SIte, collect news title, paragraph text, assign
#to variables for later reference
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

#scrape the title and accompanying paragraph
    ListTitle= soup.find("ul", class_="item_list")
    title=ListTitle.find('div', class_="content_title").get_text()
    paragraph = ListTitle.find("div", class_="article_teaser_body").get_text()

    mars_dict["title"] = title
    mars_dict["paragraph"] = paragraph


# JPL Mars Space Images - Featured Image¶
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)

    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    time.sleep(10)

    #Design an xpath selector to grab the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    #get image url using BeautifulSoup
    time.sleep(5)
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url

    mars_dict["full_img_url"] = full_img_url

    # Mars Weather

    import GetOldTweets3 as got
    tweetCriteria = got.manager.TweetCriteria().setUsername("MarsWxReport").setMaxTweets(5)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)[3]

    mars_dict["tweet"] = tweet

    # Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table

    mars_dict["mars_html_table"] = mars_html_table

    # Mars Hemispheres

    hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere)
    time.sleep(15)

    #Getting the base url
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hemisphere))
    time.sleep(15)


    cerberus_image = browser.find_by_tag('h3')[0]
    schiaparelli_image =  browser.find_by_tag('h3')[1]
    syrtis_image = browser.find_by_tag('h3')[2]
    marineris_image = browser.find_by_tag('h3')[3]

    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']

    mars_hemispheres_images = [
        {'title': cerberus_image, 'img_url': first_img},
        {'title': schiaparelli_image, 'img_url': second_img},
        {'title': syrtis_image, 'img_url': third_img},
        {'title': marineris_image, 'img_url': fourth_img}
    ]
    time.sleep(10)

    mars_dict["mars_hemispheres_images"] = mars_hemispheres_images

    return mars_dict