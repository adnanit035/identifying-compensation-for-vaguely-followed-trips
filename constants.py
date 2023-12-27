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

# number of standard routes to generate
NUM_STD_ROUTES = 50

# number of actual routes to generate
NUM_ACT_ROUTES = 300

# minimum number of trips in a standard route
MIN_TRIPS = 4

# maximum number of trips in a standard route
MAX_TRIPS = 8

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

# CITIES_TO_ADD = [
#     "Benevento", "Civitavecchia", "Fiumicino", "Lecce", "Lucca", "Matera", "Molfetta", "Pisa", "Pomezia", "Potenza",
#     "Ragusa", "Rovigo", "Savona", "Siracusa", "Tivoli", "Trani", "Varese", "Viterbo"
# ]

# Merchandise types
MERCHANDISE_TYPES = ['milk', 'honey', 'butter', 'tomatoes', 'pens', 'bread', 'coca-cola']

# Number of drivers and their IDs
NUM_DRIVERS = 20
DRIVERS = [f'D{i}' for i in range(1, NUM_DRIVERS + 1)]

# Minimum and maximum number of actual routes variations for each standard route (against the same driver)
MIN_ACT_ROUTE_VARIATIONS = 1
MAX_ACT_ROUTE_VARIATIONS = 3

# maximum number of city variations in a route
MAX_CITY_VARIATIONS = 2

# maximum number of merchandise variations in a trip
MAX_MERCH_VARIATIONS = 2

