import os
import time
import sys
import re
from time import sleep

from db import Row

# Craigslist RSS feeds are really unreadable, its actually
# much easier to scrape the html pages, so we use BeautifulSoup
from BeautifulSoup import BeautifulSoup

try:
    from jellyfish import jellyfish
except:
    print 'Could not find jellyfish, make sure you run make or setup.py in pycraig/jellyfish.'

money = re.compile('|'.join([
  r'^\$?(\d*\.\d{1,2})$',
  r'^\$?(\d+)$',
  r'^\$(\d+\.?)$',
]))

categories = {
    'antiques'                       :"atq",
    'appliances'                     :"app",
    'arts & crafts'                  :"art",
    'auto parts'                     :"pts",
    'baby & kid stuff'               :"bab",
    'barter'                         :"bar",
    'bicycles'                       :"bik",
    'boats'                          :"boa",
    'books'                          :"bks",
    'business'                       :"bfs",
    'cars & trucks - by dealer'      :"ctd",
    'cars & trucks - by owner'       :"cto",
    'elected> cars+trucks'           :"cta",
    'cds / dvds / vhs'               :"emd",
    'cell phones'                    :"mob",
    'clothing'                       :"clo",
    'collectibles'                   :"clt",
    'computers & tech'               :"sys",
    'electronics'                    :"ele",
    'farm &amp; garden'              :"grd",
    'free stuff'                     :"zip",
    'furniture'                      :"fua",
    'furniture - by dealer'          :"fud",
    'furniture - by owner'           :"fuo",
    'garage sales'                   :"gms",
    'general'                        :"for",
    'health and beauty'              :"hab",
    'household'                      :"hsh",
    'items wanted'                   :"wan",
    'jewelry'                        :"jwl",
    'materials'                      :"mat",
    'motorcycles/scooters'           :"mcy",
    'musical instruments'            :"msg",
    'photo/video'                    :"pho",
    'recreational vehicles'          :"rvs",
    'sporting goods'                 :"spo",
    'tickets'                        :"tix",
    'tools'                          :"tls",
    'toys & games'                   :"tag",
    'video gaming'                   :"vgm",
}

def get_listings(url, cat, pages=1, use_cached=False, wait=1):
    '''Use GNU curl to grab listings from Craigslist and return
    the resulting parsable HTML'''

    # Note that if you curl too much from Craigsist you will 
    # get your ip address *banned*, this script is designed 
    # for PERSONAL USE

    soups = ''

    for page in range(0,pages):

        path = '%s/%s/index%s.html' % (url, categories[cat],page*100)
        if use_cached:
            print 'Using cached copy'
        else:
            os.popen('curl -silent %s > index%s.html' % (path,page))

        try:
            soups += open('index%s.html' % (page*100)).read()
        except IOError:
            print 'Could not html file from', path

        # Wait before grabbing the next page
        sleep(wait)
    return BeautifulSoup(soups)

# Extract a row-style listing. Example:
# http://sfbay.craigslist.org/cta/
def extract_rows(soup, table):
    '''Extract row-style from the soup given and insert into the
    Table object given'''
    for row in soup.findAll('h4'):
        try:
            for x in row.nextGenerator():
                if hasattr(x,'name'):
                    date = row.string

                    # Match <p class="row"></p>
                    if x.name == 'p' and x.get('class') == 'row':
                        image = x.contents[1].get('id')

                        link = x.contents[3].get('href')

                        desc = x.contents[3].string.lower()

                        # Look for something that looks like a
                        # currency and return its numeric value
                        price_str = str(x.contents[4]).split('-')[1].strip()
                        matches = money.match(price_str)
                        price = matches and matches.group(0) or None
                        if price:
                            nprice = float(price[1:])
                            price = nprice

                        location = x.contents[5].string

                        new_row = Row(date=str(date),
                                      price=price, #Chop off the $
                                      desc=str(desc),
                                      image=str(image),
                                      link=str(image),
                                      location=str(location))

                        table.insert(new_row)
                    if x.name == 'h4':
                        raise StopIteration
        except StopIteration:
            pass
