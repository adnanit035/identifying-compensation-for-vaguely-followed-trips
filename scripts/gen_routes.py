import random
from .utils import *

if not os.path.exists(CITIES_DISTANCE_MATRIX_CSV_FILE):
    print("The distance matrix CSV file does not exist. Generating a new one...")
    distance_matrix = gen_cities_distance_matrix()
else:
    distance_matrix = pd.read_csv(CITIES_DISTANCE_MATRIX_CSV_FILE, index_col=0)


def get_closest_cities(city, num_cities=5):
    """
    Get the closest cities to the given city based on the distance matrix.

    :param city: The city to find the closest cities to.
    :param num_cities: Number of closest cities to return.
    :return: A list of the closest cities.
    """
    closest = distance_matrix[city].nsmallest(num_cities + 1).index.tolist()
    try:
        closest.remove(city)  # Remove the city itself from the list
    except ValueError:
        pass
    return closest


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
        decision = random.choice(['increase', 'decrease', 'keep'])  # Randomly decide what to do
        if decision == 'increase':
            adjusted[item] = min(quantity + random.randint(1, 5), 50)  # Capacity at 50 for max quantity
        elif decision == 'decrease' and quantity > 1:
            adjusted[item] = max(quantity - random.randint(1, quantity - 1), 1)  # Ensure at least 1
        elif decision == 'keep':
            adjusted[item] = quantity

    return adjusted


def generate_connected_standard_route(min_trips, max_trips):
    """
    Generate a connected route based on the distance matrix, ensuring no city is revisited.

    :param min_trips: Minimum number of trips in the route.
    :param max_trips: Maximum number of trips in the route.
    :return: A connected route.
    """
    route_length = random.randint(min_trips, max_trips)
    route = []

    # Select random departure and destination cities
    departure_city = random.choice(CITIES)
    destination_city = random.choice([city for city in CITIES if city != departure_city])

    current_city = departure_city
    visited_cities = [current_city]  # Initialize list of visited cities

    for _ in range(route_length):
        # Get the closest cities excluding visited ones and select the next city
        closest_cities = [city for city in get_closest_cities(current_city) if city not in visited_cities]

        # If no unvisited closest cities are available, break the loop
        if not closest_cities:
            break

        next_city = random.choice(closest_cities)
        visited_cities.append(next_city)  # Update visited cities list

        # Add trip to the route
        route.append({"from": current_city, "to": next_city, "merchandise": generate_merchandise()})

        # Update current city
        current_city = next_city

        # If the next city is the destination, break the loop
        if current_city == destination_city:
            break

    return route


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
        "id": f"a{random.randint(1, 100000)}",  # Unique ID for the actual route
        "driver": driver_id,
        "sroute": standard_route_["id"],
        "route": []
    }

    # get all the cities from the current standard route
    current_route_cities = []
    for trip in standard_route_["route"]:
        current_route_cities.append(trip["from"])
        current_route_cities.append(trip["to"])

    current_route_cities = list(set(current_route_cities))

    # Iterate over the trips in the standard route to create variations
    trip_count = 0
    num_of_city_variations = 0
    num_of_merch_variations = 0

    actions_list = ["omission", "addition"]

    # randomly choose an action
    action = random.choice(actions_list)

    if action == "omission":
        # randomly choose a city to remove
        selected_city_to_remove = random.choice(current_route_cities[:len(current_route_cities) - 1])

        # to replace the removed city with a new close city, select top 3 closest cities
        closest_cities = get_closest_cities(selected_city_to_remove, 5)

        closest_cities_ = [
            city for city in closest_cities
            if city != selected_city_to_remove and city not in current_route_cities
        ]

        if len(closest_cities_) == 0:
            num_of_closest_increment = 5
            while len(closest_cities_) == 0:
                # to replace the removed city with a new close city, select top 3 closest cities
                closest_cities = get_closest_cities(selected_city_to_remove, num_of_closest_increment + 3)

                closest_cities_ = [
                    city for city in closest_cities
                    if city != selected_city_to_remove and city not in current_route_cities
                ]

                num_of_closest_increment += 3

            # randomly choose a new city to replace the removed city
            selected_new_city_to_replace = random.choice(closest_cities_)
        else:
            # randomly choose a new city to replace the removed city
            selected_new_city_to_replace = random.choice(closest_cities_)

        # get all the trips with selected_city_to_remove
        trips_with_selected_city_to_remove = []
        for trip_ in standard_route_["route"]:
            if trip_["from"] == selected_city_to_remove or trip_["to"] == selected_city_to_remove:
                trips_with_selected_city_to_remove.append(trip_)

        # replace all the trips with selected_city_to_remove with trips with selected_new_city_to_replace
        for trip_ in standard_route_["route"]:
            if trip_["from"] == selected_city_to_remove:
                actual_route["route"].append({
                    "from": selected_new_city_to_replace, "to": trip_["to"],
                    "merchandise": adjust_merchandise(trip_["merchandise"])
                })
            elif trip_["to"] == selected_city_to_remove:
                actual_route["route"].append({
                    "from": trip_["from"], "to": selected_new_city_to_replace,
                    "merchandise": adjust_merchandise(trip_["merchandise"])
                })
            else:
                # add the original trip
                actual_route["route"].append(trip_)
    elif action == "addition":
        for trip in standard_route_["route"]:
            trip_count += 1

            # closest cities to the current trip "from" city
            closest_cities = get_closest_cities(trip["from"], 5)

            # closest cities to the current trip "to" city
            closest_cities.extend(get_closest_cities(trip["to"], 5))

            # duplicate cities are removed
            closest_cities = list(set(closest_cities))

            # remove the current trip "from" and "to" cities from the closest cities list
            closest_cities = [
                city for city in closest_cities
                if city != trip["from"] and city != trip["to"] and city not in current_route_cities
            ]

            # if there are no close cities to the current trip "from" and "to" cities, keep the original trip
            if not closest_cities:
                actual_route["route"].append(trip)
                continue

            # Choose a random nearby city for a detour
            detour_city = random.choice(closest_cities)

            # if this is the first trip
            if trip_count == 1:
                # add a detour city in from of the original trip or after the original trip
                if random.choice([True, False]):
                    # Add a detour trip (from the detour city to the original city)
                    actual_route["route"].append({
                        "from": detour_city, "to": trip["from"],
                        "merchandise": adjust_merchandise(trip["merchandise"])
                    })

                    # Add the original trip (from the original city to the detour city)
                    actual_route["route"].append({
                        "from": trip["from"], "to": trip["to"],
                        "merchandise": adjust_merchandise(trip["merchandise"])
                    })

                    # update the current route cities list with the new detour city
                    current_route_cities.append(detour_city)

                    # increase the number of city variations
                    num_of_city_variations += 1
                else:  # if the detour city is added after the original trip
                    if random.choice([True, False]):
                        # Add a detour trip (from the original city to the detour city)
                        actual_route["route"].append({
                            "from": trip["from"], "to": detour_city,
                            "merchandise": adjust_merchandise(trip["merchandise"])
                        })

                        # Add the original trip (from the detour city to the original destination)
                        actual_route["route"].append({
                            "from": detour_city, "to": trip["to"],
                            "merchandise": adjust_merchandise(trip["merchandise"])
                        })

                        # update the current route cities list with the new detour city
                        current_route_cities.append(detour_city)

                        # increase the number of city variations
                        num_of_city_variations += 1
                    else:
                        # Keep the original trip
                        actual_route["route"].append(trip)
                        continue

            # if not the first trip
            else:
                # if variation limit is reached, keep the original trip
                if num_of_city_variations >= MAX_CITY_VARIATIONS:
                    # keep the original trip
                    actual_route["route"].append(trip)
                    continue

                # Randomly decide to make a minor detour
                if random.choice([True, False]):
                    # Add a detour trip (from the original city to the detour city)
                    actual_route["route"].append({
                        "from": trip["from"], "to": detour_city,
                        "merchandise": adjust_merchandise(trip["merchandise"])
                    })

                    # Add the original trip (from the detour city to the original destination)
                    actual_route["route"].append({
                        "from": detour_city, "to": trip["to"],
                        "merchandise": adjust_merchandise(trip["merchandise"])
                    })

                    # update the current route cities list with the new detour city
                    current_route_cities.append(detour_city)

                    # increase the number of city variations
                    num_of_city_variations += 1
                else:  # merchandise variation
                    if num_of_merch_variations >= MAX_MERCH_VARIATIONS:
                        # keep the original trip
                        actual_route["route"].append(trip)
                        continue

                    # Keep the original trip but adjust the merchandise
                    actual_route["route"].append({
                        "from": trip["from"], "to": trip["to"],
                        "merchandise": adjust_merchandise(trip["merchandise"])
                    })

                    # increase the number of merchandise variations
                    num_of_merch_variations += 1

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
