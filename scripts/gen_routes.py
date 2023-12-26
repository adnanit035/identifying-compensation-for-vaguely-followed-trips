from constants import *
import random


def generate_merchandise():
    """Generate a random set of merchandise with quantities."""
    return {
        # merchandise_type: random_quantity for _ in range(random_number_of_items)
        random.choice(MERCHANDISE_TYPES): random.randint(1, 50) for _ in range(random.randint(1, 4))
    }


def adjust_merchandise(merchandise):
    """
    Adjust the merchandise by increasing, decreasing, omitting, or keeping the quantity of each item.

    :param merchandise: The merchandise to adjust.

    :return: The adjusted merchandise.
    """
    adjusted = {}
    for item, quantity in merchandise.items():
        decision = random.choice(['increase', 'decrease', 'omit', 'keep'])  # Randomly decide what to do
        if decision == 'increase':
            adjusted[item] = min(quantity + random.randint(1, 5), 50)  # Capacity at 50 for max quantity
        elif decision == 'decrease' and quantity > 1:
            adjusted[item] = max(quantity - random.randint(1, quantity - 1), 1)  # Ensure at least 1
        elif decision == 'keep':
            adjusted[item] = quantity

    return adjusted


def generate_connected_standard_route(min_trips_, max_trips_):
    """
    Generate a connected route with a random number of trips within the specified constraint.

    @param min_trips_: minimum number of trips in the route
    @param max_trips_: maximum number of trips in the route

    @return: a connected route with a random number of trips within the specified constraint
    """
    route_length = random.randint(min_trips_, max_trips_)  # Number of trips in the route

    # random.sample() returns a list of unique elements, so the route is guaranteed to be connected
    selected_cities = random.sample(CITIES, route_length + 1)  # One more city for the final destination

    # randomize the order of the CITIES
    random.shuffle(selected_cities)

    route_ = []
    for i in range(route_length):  # Generate a trip for each pair of CITIES
        from_city = selected_cities[i]
        to_city = selected_cities[i + 1]
        route_.append({"from": from_city, "to": to_city, "merchandise": generate_merchandise()})

    return route_


def generate_standard_routes(num_routes, min_trips_, max_trips_):
    """
    Generate a set of standard routes with connected trips and trip number constraints.

    @param num_routes: number of routes to generate
    @param min_trips_: minimum number of trips in the route
    @param max_trips_: maximum number of trips in the route

    @return: a set of standard routes with connected trips and trip number constraints
    """
    standard_routes = []
    for i in range(num_routes):  # Generate a standard route for each route id
        # Generate a connected route with the specified trip constraints
        route_ = generate_connected_standard_route(min_trips_, max_trips_)

        # Add the route to the list of standard routes
        standard_routes.append({"id": f"s{i + 1}", "route": route_})

    return standard_routes


def create_an_actual_route_with_variation(standard_route_, driver_id):
    """
    Create a variation of the standard route to form an actual route.
    Variations include minor changes in the route and merchandise.

    :param standard_route_: The original standard route.
    :param driver_id: The ID of the driver for the actual route.
    :return: A varied actual route.
    """
    actual_route = {
        "id": f"a{random.randint(1, 10000)}",  # Unique ID for the actual route
        "driver": driver_id,
        "sroute": standard_route_["id"],
        "route": []
    }

    # Iterate over the trips in the standard route to create variations
    for trip in standard_route_["route"]:
        # Randomly decide to make a minor detour
        if random.choice([True, False]):
            # Choose a random nearby city for a detour
            detour_city = random.choice(
                [city for city in CITIES if city != trip["from"] and city != trip["to"]]
            )

            # add a detour city in from of the original trip or after the original trip
            if random.choice([True, False]):
                # Add a detour trip (from the detour city to the original city)
                actual_route["route"].append({
                    "from": detour_city, "to": trip["from"],
                    "merchandise": generate_merchandise()
                })

                # Add the original trip (from the original city to the detour city)
                actual_route["route"].append({
                    "from": trip["from"], "to": detour_city,
                    "merchandise": adjust_merchandise(trip["merchandise"])
                })
            else:
                # Add a detour trip (from the original city to the detour city)
                actual_route["route"].append({
                    "from": trip["from"], "to": detour_city,
                    "merchandise": adjust_merchandise(trip["merchandise"])
                })

                # Add the original trip (from the detour city to the original destination)
                actual_route["route"].append({
                    "from": detour_city, "to": trip["to"],
                    "merchandise": generate_merchandise()
                })
        else:
            # Keep the original trip but adjust the merchandise
            actual_route["route"].append({
                "from": trip["from"], "to": trip["to"],
                "merchandise": adjust_merchandise(trip["merchandise"])
            })

    return actual_route


def generate_actual_routes(standard_routes_, drivers_, min_variations_=1, max_variations_=3):
    """
    Generate a set of actual routes with variations from the given standard routes and drivers.

    :param standard_routes_: The standard routes to use.
    :param drivers_: The drivers to use.
    :param min_variations_: The minimum number of variations for each standard route for each driver.
    :param max_variations_: The maximum number of variations for each standard route for each driver.

    :return: A set of actual routes with variations from the given standard routes and drivers.
    """
    actual_routes = []
    for driver_ in drivers_:
        for standard_route_ in standard_routes_:
            # Generate multiple variations for each standard route for each driver
            for _ in range(random.randint(min_variations_, max_variations_)):
                varied_route_ = create_an_actual_route_with_variation(standard_route_, driver_)
                actual_routes.append(varied_route_)

    return actual_routes
