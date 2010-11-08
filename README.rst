=========
PyCraig
=========

PyCraig is a python library for scraping small amounts of data
off of Craigslist.

All code is released under a BSD-style license, see LICENSE for details.

Written by Stephen Diehl <sdiehl@clarku.edu>.

Dependencies
============

PyCraig depends on *BeautifulSoup*, you can install it with

>   pip install BeautifulSoup

It also uses GNU Curl for grabbing web pages. If you are running
Linux, BSD, or OS X you probably have this installed.

*jellyfish* ( https://github.com/sunlightlabs/jellyfish ) is
optinally included for doing approximate string matching. It 
is written in C and is very fast. 

To use it run from the pycraig directory use the included 
Makefile

>    cd pycraig/jellyfish
>    make

Or install globally with:

>   python pycraig/jellyfish/setup.py install


Example
=======

>>> from pycraig import *

# Get 3 page of listings for "cars & trucks" for sale "by owner"
# in the "San Franciso Bay" area
>>> listings = get_listings(url='sfbay.craigslist.org',
...                         cat='cars & trucks - by owner',
...                         pages=3)


# Create table with our car listings
>>> cars = Table()
>> extract_rows(listings, cars)

# Show all hondas under $15,000
>>> for car in cars:
...    if car.price < 15000 and 'honda' in car.desc:
...        print car.link, car.desc
