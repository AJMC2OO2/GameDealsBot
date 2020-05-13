import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver


class ImagePreview:
    def ogimage(url, code):
        og_image = html.find_all(property="og:image")
        for image in og_image:
            return image.get('content')
            break

    def imagesrc(url, code):
        image_src = html.find_all(rel="image_src")
        for image in image_src:
            return image.get('href')
            break

    def preview_image(url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        
        source = driver.get(url)
        html = driver.page_source
        code = BeautifulSoup(source.text, "html.parser")
        if ogimage(url, code) != None:
            return ogimage(url, code)
        elif imagesrc(url, code) != None:
            return imagesrc(url, code)
        else:
            return ""
