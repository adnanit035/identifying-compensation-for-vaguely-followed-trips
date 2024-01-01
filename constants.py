import os


# home directory
HOME = os.path.dirname(os.path.abspath(__file__))

# data directory
DATA_DIR = os.path.join(HOME, "Dataset")

# Italian cities database CSV file
ITALIAN_CITIES_DB_CSV_FILE = os.path.join(DATA_DIR, "it-cities.csv")

# Selected Cities Distance Matrix CSV file
CITIES_DISTANCE_MATRIX_CSV_FILE = os.path.join(DATA_DIR, "distance-matrix.csv")

# standard routes file
STD_ROUTES_FILE = os.path.join(DATA_DIR, "standard_routes.json")

# actual routes file
ACT_ROUTES_FILE = os.path.join(DATA_DIR, "actual_routes.json")

# List of top 50 cities in Italy (from Wikipedia)
CITIES = [
    "Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence",
    "Bari", "Catania", "Verona", "Venice", "Messina", "Padova", "Prato", "Trieste",
    "Brescia", "Parma", "Taranto", "Modena", "Reggio di Calabria", "Reggio Emilia",
    "Perugia", "Ravenna", "Livorno", "Rimini", "Cagliari", "Foggia", "Ferrara",
    "Salerno", "Latina", "Giugliano in Campania", "Monza", "Sassari", "Bergamo",
    "Pescara", "Trento", "Forlì", "Siracusa", "Vicenza", "Terni", "Bolzano",
    "Piacenza", "Novara", "Ancona", "Udine"
]

# Merchandise types
MERCHANDISE_TYPES = ['milk', 'honey', 'butter', 'tomatoes', 'pens', 'bread', 'coca-cola']

# number of standard routes to generate
NUM_STD_ROUTES = 50

# number of actual routes to generate
NUM_ACT_ROUTES = 500

# minimum number of trips in a standard route
MIN_TRIPS = 4

# maximum number of trips in a standard route
MAX_TRIPS = 7

# Number of drivers and their IDs
NUM_DRIVERS = 50
DRIVERS = [f'D{i}' for i in range(1, NUM_DRIVERS + 1)]

# Minimum and maximum number of actual routes variations for each standard route (against the same driver)
MIN_ACT_ROUTE_VARIATIONS_PER_DRIVER = 5
MAX_ACT_ROUTE_VARIATIONS_PER_DRIVER = 20

# Same varied route(s) probability (i.e. probability of having the same route(s) for a driver). Here same route(s) means
# varied actual route(s) that are different from the standard route but belongs to same actual route(s) variations.
SAME_VARIED_ROUTE_PROB = 0.60
SAME_STD_ROUTE_PROB = 0.10

# maximum number of city variations in a route
MIN_CITY_VARIATIONS_PER_ROUTE = 2
MAX_CITY_VARIATIONS_PER_ROUTE = 4

# maximum number of merchandise variations in a trip
MIN_MERCH_VARIATIONS_PER_ROUTE = 2
MAX_MERCH_VARIATIONS_PER_ROUTE = 4
