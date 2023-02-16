# 
# %%

# load packages
import math
import json
import numpy as np
import requests
import random

# Define 10 miles boundary for current location
def get_bounding_box(lat, lon, radius=10):

    """
    This function uses the Haversine formula to calculate the distance between two points on the Earth's surface, 
    and then, 
    calculates the latitude and longitude boundaries for a square bounding box around the given location 
    with sides of length equal to the radius. 
    The function returns a tuple representing the minimum and maximum latitude and longitude values for the bounding box.


    Arguments:

    Input: 
        lat: latitude for current location

        lon: longitude for current location

        radius: radius for current location
                unit: miles

    
    Output:
        lat_min: min latitude for current location
        
        lon_min: mix longitude for current location
        
        lat_max: max latitude for current location 
        
        lon_max: max longitude for current location



    
    Example
    -------
    lat = 39.7589
    lon = -84.1916
    radius = 10
    bounding_box = get_bounding_box(lat, lon, radius)
    print(bounding_box)


    (39.68082270984139, -84.30565642600785, 39.83797729015862, -84.07754357399214)
    """


    # Earth's radius in miles
    R = 3963.1676

    # Convert radius from miles to radians
    r_lat = math.radians(radius / R)
    r_lon = math.radians(radius / (R * math.cos(math.pi * lat / 180)))

    # Calculate the bounding box
    lat_min = lat - math.degrees(r_lat)
    lat_max = lat + math.degrees(r_lat)
    lon_min = lon - math.degrees(r_lon)
    lon_max = lon + math.degrees(r_lon)

    return (lat_min, lon_min, lat_max, lon_max)


def miles_to_meters(miles):
    """
    Description:
    -----------

    Convert miles into meters

    Arguments:
    ----------

        Input:
        -------
        miles: number of miles


        Output:
        --------
        meters: miles in meters 
                dtype: int32
    
    Note: 
        The output has to be int otherwise the search_restaurants() won't work
    """
    meters = np.int32(miles * 1609.34)
    return meters

def search_restaurants(latitude, longitude, api_key, limit, radius):
    
    """
    Description
    -----------
    This is the skeleton code for a function that searches for restaurants near a 
    given latitude and longitude using the Yelp Fusion API, 
    and returns a list of restaurant information sorted by rating.
    

    Arguments:
    ----------

        Input: 
        ------
        latitude: the latitude information of your current location

        longitude: the longitude information of your current location

        api_key: the personal api_key for access Yelp dataset

        limit: number of results return

        radius: the boundary for searching
                unit: meters

        Output:
        -------
        restaurants: restaurants with detail information 
                    dtype: np array
    """

    # Set the endpoint and parameters for the Yelp Fusion API search
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius, # miles in meters
        'categories': 'restaurants',
        'sort_by': 'rating',
        'open_now': True,
        'price': '1,2',
        'limit': limit # maximum number of results to return
    }
    
    # Make the HTTP request to the Yelp Fusion API
    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()
    
    # Extract the restaurant information from the API response
    restaurants = []
    for business in data["businesses"]:
        restaurant = {
            'name': business['name'],
            'rating': business['rating'],
            'address': ', '.join(business['location']['display_address']),
            'phone': business['phone']
        }
        restaurants.append(restaurant)
    
    return restaurants


# generate the final restaurant decision
def get_restaurant_decision(restaurants):
    """
    Description:
    ------------
    The get_restaurant_decision function takes a list of restaurants as input and
    returns a random restaurant from the list
    

    Arguments:
    ----------
        Inputs:
        --------
            restaurants : restaurants pool for final restaurant decision
                            dtype: numpy array

        Outputs:
            restaurant_decision: final restaurant decision
    
    
    """
    # Generate a random number between 0 and the number of restaurants
    random_value = random.randint(0,len(restaurants)-1) # here use -1 in case the boundary error
    # Select the restaurant at the random index
    restaurant_decision = restaurants[random_value]

    return restaurant_decision


# %% Pipline
"""
Here is work pipeline for "What should I eat today?"
"""


# Dayton
latitude = 39.758948
longitude = -84.191607

# Cincinnati 
# latitude = 39.103119
# longitude = -84.512016

api_key = "kUHCKejIt3HOsQwtd-NuLcOHtaBaWQtKXXB5O4ESkDd3w2up0XuuM6OOfN-7ATM3EG9zWdelJ7akz46wnCjxfaG7vpOc_39mFP4GVRhjHha02xmV_cU0LmB3KZrtY3Yx"
miles = 20
limit = 30 # Note: the max limit could set upto 50, otherwise will return error.

# convert miles into meters
radius = miles_to_meters(miles= miles)
# generate the restaurant pool
restaurants = search_restaurants(latitude = latitude, 
                                 longitude = longitude, 
                                 api_key = api_key,
                                radius = radius, 
                                limit = limit)

final_decision = get_restaurant_decision(restaurants= restaurants)

print("Tonight you should go: ", final_decision["name"])
print("The rating for this restaurant is :", final_decision["rating"])
print("The address is :", final_decision["address"] )
print("The Phone number is :", final_decision["phone"], "if you want to order through phone")
# %%
