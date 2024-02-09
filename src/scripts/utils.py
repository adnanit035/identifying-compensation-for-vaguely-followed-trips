import pandas as pd
from geopy import distance
from src.constants import *


IT_CITIES_DF = pd.read_csv(ITALIAN_CITIES_DB_CSV_FILE)

# rename so that the column names are shorter and comply with PEP-8
IT_CITIES_DF.rename(
    columns={"CountryName": "Country", "CapitalName": "capital", "CapitalLatitude": "lat",
             "CapitalLongitude": "lon", "CountryCode": "code", "ContinentName": "continent"},
    inplace=True
)


# Function to calculate the distance between two cities
def calculate_distance(city1_, city2_):
    """
    Calculate the distance between two cities in km using the geopy library. Note that first the coordinates of the two
    cities are retrieved from the IT_CITIES_DF dataframe, then the distance is calculated. If the two cities are the
    same, the distance is set to NaN. If one of the two cities is not in the IT_CITIES_DF dataframe, then there will be
    a KeyError exception. So it is important to make sure that the selected cities are in the IT_CITIES_DF dataframe.

    @param city1_: the first city
    @param city2_: the second city

    @return: the distance between the two cities
    """
    global IT_CITIES_DF

    # Get the coordinates of the two cities
    city1_coords = IT_CITIES_DF[IT_CITIES_DF["city"] == city1_].reset_index()
    city2_coords = IT_CITIES_DF[IT_CITIES_DF["city"] == city2_].reset_index()

    # Calculate the distance between the two cities
    d_ = distance.distance(
        (city1_coords.loc[0, "lat"], city1_coords.loc[0, "lng"]),
        (city2_coords.loc[0, "lat"], city2_coords.loc[0, "lng"])
    )

    return d_.km


def gen_cities_distance_matrix():
    """
    Generate a distance matrix for the cities in the CITIES list. The distance matrix is a pandas dataframe with the
    cities in the CITIES list as both row and column indexes. The distance between two cities is calculated using the
    calculate_distance() function. The distance matrix is saved to a CSV file.
    :return: the distance matrix as a pandas dataframe
    """
    # Create a distance matrix for the cities
    distance_matrix = pd.DataFrame(index=CITIES, columns=CITIES)
    for city1 in CITIES:
        print(f"Calculating distances from {city1}...")
        for city2 in CITIES:
            if city1 == city2:
                continue
            distance_matrix.loc[city1, city2] = calculate_distance(city1, city2)

    # Save the distance matrix to a CSV file
    distance_matrix.to_csv(CITIES_DISTANCE_MATRIX_CSV_FILE, index=False)
    print(f"Distance matrix saved to {CITIES_DISTANCE_MATRIX_CSV_FILE}")

    return distance_matrix
