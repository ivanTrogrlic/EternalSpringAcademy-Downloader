from cgitb import html
import re
import ssl
import time
import requests
from fileinput import filename
from urllib.request import urlopen

from file_utils import *
from link_finder import LinkFinder

OBJAVE = "Objave"

class Downloader:
    base_url = ''

    def __init__(self, base_url):
        create_project_dir(OBJAVE)
        Downloader.base_url = base_url
        self.crawl_page('First spider', base_url)
    
    @staticmethod
    def crawl_page(thread_name, page_url):
        print(thread_name + ' now crawling ' + page_url)
        Downloader.download_from_links(Downloader.gather_links(page_url))

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            gcontext = ssl._create_unverified_context()
            response = urlopen(page_url, context=gcontext)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("iso-8859-1")
            finder = LinkFinder(Downloader.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print('Error: cannot crawl page')
            print(e)
            return set()
        return finder.page_links()

    @staticmethod
    def download_from_links(links):
        for url in links:
            time.sleep(1) # Avoid DDOSing the page :)

            fileName = re.search("(?<=https:\/\/akademijavjecnogproljeca.org\/dudde_poruke\/poruke\/bd_)(.*)(?=\.html)", str(url))
            print("File name", OBJAVE + "/" + str(fileName.group()))

            html_string = ''
            try:
                response = requests.get(url)
                html_string = response.text
                objava = re.search("(?=<div class=\"okvir\">)([\S\s]*?)(?<=<\/div>)", html_string)
                write_file(OBJAVE + "/" + str(fileName.group()) + ".txt", str(objava.group()))
                print("File written")
            except Exception as e:
                print('Error: cannot read page')
                print(e)
