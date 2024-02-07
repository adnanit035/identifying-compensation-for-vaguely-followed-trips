import json
from constants import *
from scripts.gen_routes import generate_standard_routes, generate_actual_routes


# # Generate a set of standard routes
standard_routes = generate_standard_routes(
    num_routes=NUM_STD_ROUTES, min_trips_=MIN_TRIPS, max_trips_=MAX_TRIPS
)

# Write the generated standard routes to a JSON file
with open(STD_ROUTES_FILE, "w") as f:
    json.dump(standard_routes, f, indent=4)

print("Generated standard routes and written to {}".format(STD_ROUTES_FILE))

# read standard routes from json file
with open(STD_ROUTES_FILE, "r") as f:
    standard_routes = json.load(f)

# Generate a set of actual routes
actual_routes = generate_actual_routes(
    standard_routes_=standard_routes, drivers_=DRIVERS,
    min_variations_per_driver=MIN_ACT_ROUTE_VARIATIONS_PER_DRIVER,
    max_variations_per_driver=MAX_ACT_ROUTE_VARIATIONS_PER_DRIVER,

)

# Write the generated actual routes to a JSON file
with open(ACT_ROUTES_FILE, "w") as f:
    json.dump(actual_routes, f, indent=4)

print("Generated actual routes and written to {}".format(ACT_ROUTES_FILE))
