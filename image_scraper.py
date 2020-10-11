import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver


def ogimage(url, html):
    """Finds the property="og:image" in the html for the preview"""
    og_image = html.find_all(property="og:image")
    for image in og_image:
        return image.get('content')
    return


def imagesrc(url, html):
    """Finds the rel="image_src" in the html for the preview"""
    image_src = html.find_all(rel="image_src")
    for image in image_src:
        return image.get('href')


def preview_image(url):
    """Heroku configurations for Chrome webdriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get(
        "/app/.chromedriver/bin/chromedriver")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "/app/.apt/usr/bin/google-chrome"), chrome_options=chrome_options)

    """Returns the image in the website (og:image -> image_src -> Nothing)"""
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if ogimage(url, soup) != None:
        return ogimage(url, soup)
    elif imagesrc(url, soup) != None:
        return imagesrc(url, soup)
    else:
        return ""
