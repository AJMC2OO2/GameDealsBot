import requests
from bs4 import BeautifulSoup


def ogimage(url, html):
    og_image = html.find_all(property="og:image")
    for image in og_image:
        return image.get('content')


def imagesrc(url, html):
    image_src = html.find_all(rel="image_src")
    for image in image_src:
        return image.get('href')


def preview_image(url):
    session = requests.Session()
    cookies = session.cookies.get_dict()
    source = session.get(url, cookies=cookies)
    html = BeautifulSoup(source.text, "html.parser")
    if ogimage(url, html) == None and imagesrc(url, html) == None:
        return None
    elif ogimage(url, html) == None:
        return imagesrc(url, html)
    else:
        return ogimage(url, html)
