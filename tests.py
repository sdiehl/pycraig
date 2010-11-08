from pycraig import *

# Get 3 page of listings for "cars & trucks" for sale "by owner"
# in the "San Franciso Bay" area
listings = get_listings(url='sfbay.craigslist.org',
                        cat='cars & trucks - by owner',
                        pages=1)

cars = Table()

# Populate the table with our car listings
extract_rows(listings, cars)

for car in cars:
    if car.price < 15000 and 'honda' in car.desc:
        print car.link, car.desc

# Save the results for later
cars.to_file('hondas')

# ... some time later
cars = Table.from_file('hondas')

from itertools import *

sorted_by_price = sorted(cars, key=lambda car: car.price)
group_by_location = groupby(cars, key=lambda car: car.location)

# Show all cars in a common location
for location, cars in group_by_location:
    print location, [car.price for car in cars]

# Get 1 page of listings for "cell phones" in the 
# "San Fernando Valley" area
listings = get_listings(url='losangeles.craigslist.org/sfv',
                        cat='cell phones',
                        pages=1)

cells = Table()
extract_rows(listings, cells)

for cell in cells:
    print cell.price
