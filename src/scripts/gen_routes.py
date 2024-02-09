import copy
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
    # print('city:', city)
    # print('distance_matrix:', distance_matrix)
    # print('distance_matrix[city]:', distance_matrix[city])
    # print('num_cities:', num_cities)
    closest = distance_matrix[city].nsmallest(num_cities + 1).index.tolist()
    try:
        closest.remove(city)  # Remove the city itself from the list
    except ValueError:
        pass
    return closest


def generate_merchandise():
    selected_merchandise = random.sample(
        MERCHANDISE_TYPES, random.randint(2, min(MERCHANDISE_SIZE, len(MERCHANDISE_TYPES)))
    )

    return {item: random.randint(1, 50) for item in selected_merchandise}


# def generate_merchandise():
#     """Generate a random set of merchandise with quantities."""
#     return {
#         # merchandise_type: random_quantity for _ in range(random_number_of_items)
#         random.choice(MERCHANDISE_TYPES): random.randint(1, 50) for _ in range(random.randint(1, 4))
#     }


# def adjust_merchandise(merchandise):
#     """
#     Adjust the merchandise by increasing, decreasing, omitting, or keeping the quantity of each item.
#
#     :param merchandise: The merchandise to adjust.
#
#     :return: The adjusted merchandise.
#     """
#     # if merchandise is empty, then create a new merchandise
#     if not merchandise:
#         return generate_merchandise()
#
#     adjusted = {}
#     for item, quantity in merchandise.items():
#         decision = random.choice(['increase', 'decrease', 'keep'])  # Randomly decide what to do
#         if decision == 'increase':
#             adjusted[item] = min(quantity + random.randint(1, 5), 50)  # Capacity at 50 for max quantity
#         elif decision == 'decrease' and quantity > 1:
#             adjusted[item] = max(quantity - random.randint(1, quantity - 1), 1)  # Ensure at least 1
#         elif decision == 'keep':
#             adjusted[item] = quantity
#
#     # if adjusted merchandise is empty, then do a recursive call to adjust the merchandise
#     if not adjusted:
#         return adjust_merchandise(merchandise)
#
#     return adjusted


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


def route_merchandise_variations(route):
    """
    Adjust the merchandise of a random trip either by removing an item or changing the quantity of an item.
    :param route: A route containing trips with merchandise.
    :return: The route with adjusted merchandise in a random trip.
    """
    try:
        index = random.randint(0, len(route) - 1)  # select a random trip
        merchandise = route[index]['merchandise']  # get the merchandise in the trip
        length = len(merchandise)
    except Exception:
        print('route:', route)
        raise Exception

    if random.randint(0, 1):  # 50% chance of losing an item or changing the quantity of an item
        # if losing an item
        for _ in range(random.randint(0, length)):
            if length > 5:
                key = list(merchandise.keys())[random.randint(0, length - 1)]
                del merchandise[key]
                length -= 1
    else:
        # if changing the quantity of an item
        for _ in range(random.randint(0, length)):
            key = list(merchandise.keys())[random.randint(1, length - 1)]
            merchandise[key] = random.randint(1, 50)

    route[index]['merchandise'].update(merchandise)

    return route


def trip_merchandise_variations(trip):
    """
    Adjust the merchandise of a trip either by removing an item or changing the quantity of an item.
    :param trip: A trip with merchandise.
    :return: The trip with adjusted merchandise.
    """
    merchandise = trip['merchandise']
    length = len(merchandise)  # get the length of the merchandise in the trip

    if random.randint(0, 1):
        # if losing an item
        for _ in range(random.randint(0, length)):
            if length > 5:  # if the length of the merchandise is greater than 5
                # randomly choose an item to remove
                key = list(merchandise.keys())[random.randint(0, length - 1)]
                del merchandise[key]
                length -= 1
    else:
        # if changing the quantity of an item
        for _ in range(random.randint(0, length)):
            key = list(merchandise.keys())[random.randint(1, length - 1)]
            merchandise[key] = random.randint(1, 50)

    trip['merchandise'].update(merchandise)

    return trip['merchandise']


def add_item_or_change_quantity_of_items_in_merchandise(route):
    """
    Add new items to the merchandise if there is space or change the quantity of the existing items.
    :param route: A route containing trips with merchandise.
    :return: The route with adjusted merchandise.
    """
    # Iterate over the trips in the route to add new items or change the quantity of the existing items
    for index in range(0, len(route)):
        current_merchandise = [m for m in route[index]['merchandise'].keys()]
        available_merchandise = [m for m in MERCHANDISE_TYPES if m not in current_merchandise]

        new_items = {}
        if available_merchandise:  # if there is space for new items
            selected_merchandise = random.sample(
                available_merchandise, random.randint(1, min(MERCHANDISE_SIZE, len(available_merchandise)))
            )
            for item in selected_merchandise:  # add new items to the merchandise
                new_items[item] = random.randint(1, 50)
        else:
            # if there is no space for new items, then change the quantity of the existing items
            new_items = trip_merchandise_variations(copy.deepcopy(route[index]))

        route[index]['merchandise'].update(new_items)

    return route


def adjust_merchandise(route):
    """
    Adjust the merchandise of the trips in the route by adding new items or changing the quantity of the existing items.
    :param route: A route containing trips with merchandise.
    :return: The route with adjusted merchandise.
    """
    merchandise_variations_ops = ['Addition', 'Variation', 'Keep']
    # randomly choose a merchandise variation operation
    merchandise_variation_op = random.choice(merchandise_variations_ops)

    if merchandise_variation_op == 'Addition':
        return add_item_or_change_quantity_of_items_in_merchandise(route)
    elif merchandise_variation_op == 'Variation':
        return route_merchandise_variations(route)
    else:
        return route


def create_actual_routes_with_variations_for_std_route(standard_route_, variations=10):
    """
    Create a variation of the standard route to form an actual route.
    Variations include minor changes in the route and merchandise.

    :param standard_route_: The original standard route.
    # :param driver_id: The ID of the driver for the actual route.
    :param variations: The number of variations to create for the standard route.

    :return: A varied actual route.
    """
    # get all the cities from the current standard route
    current_route_cities = []
    for trip in standard_route_["route"]:
        current_route_cities.append(trip["from"])
        current_route_cities.append(trip["to"])

    current_route_cities = list(set(current_route_cities))

    actions_list = ["omission", "addition", "merchandise_variation"]

    num_of_city_variations = 0  # number of city variations in the route
    actual_route_variations_of_current_std_route = []

    while len(actual_route_variations_of_current_std_route) < variations:
        # Create a new actual route variation of the standard route
        actual_route = {
            "id": f"a{random.randint(1, 100000)}",  # Unique ID for the actual route
            # "driver": driver_id,
            "route": []
        }

        try:
            actual_route["sroute"] = standard_route_["sroute"]  # in case of keeping the same variation
        except KeyError:
            actual_route["sroute"] = standard_route_["id"]  # keeping the standard route or creating a new variation

        keep_std_route = random.random() < SAME_STD_ROUTE_PROB
        keep_same_variation = random.random() < SAME_VARIED_ROUTE_PROB

        if keep_same_variation:
            # then randomly choose a variation of the standard route from the actual_routes list for the same
            # driver and same standard route
            if len(actual_route_variations_of_current_std_route) > 0:
                already_created_variation = random.choice(actual_route_variations_of_current_std_route)
                already_created_variation["route"] = adjust_merchandise(
                    copy.deepcopy(already_created_variation["route"])
                )
                actual_route_variations_of_current_std_route.append(already_created_variation)
                continue

        if keep_std_route:
            # keep the original standard route
            actual_route["route"] = adjust_merchandise(copy.deepcopy(standard_route_["route"]))
            actual_route_variations_of_current_std_route.append(actual_route)
            continue

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
                    varied_trip = {
                        "from": selected_new_city_to_replace, "to": trip_["to"],
                        "merchandise": trip_["merchandise"]
                    }
                    # trip's merchandise variation
                    varied_trip["merchandise"] = trip_merchandise_variations(varied_trip)
                    actual_route["route"].append(varied_trip)
                elif trip_["to"] == selected_city_to_remove:
                    varied_trip = {
                        "from": trip_["from"], "to": selected_new_city_to_replace,
                        "merchandise": trip_["merchandise"]
                    }
                    # trip's merchandise variation
                    varied_trip["merchandise"] = trip_merchandise_variations(varied_trip)
                    actual_route["route"].append(varied_trip)
                else:
                    # add the original trip
                    actual_route["route"].append(trip_)
        elif action == "addition":  # addition of a new city in the route
            while num_of_city_variations < MAX_CITY_VARIATIONS_PER_ROUTE:
                # randomly choose a trip for the new city addition
                selected_trip_index = random.randint(0, len(standard_route_["route"]) - 1)
                selected_trip = standard_route_["route"][selected_trip_index]

                # closest cities to the current trip "from" city
                closest_cities = get_closest_cities(selected_trip["from"], 5)

                # closest cities to the current trip "to" city
                closest_cities.extend(get_closest_cities(selected_trip["to"], 5))

                # duplicate cities are removed
                closest_cities = list(set(closest_cities))

                # remove the current trip "from" and "to" cities from the closest cities list
                closest_cities = [
                    city for city in closest_cities
                    if city != selected_trip["from"] and city != selected_trip["to"] and city not in current_route_cities
                ]
                # if there are no close cities to the current trip "from" and "to" cities, keep the original trip
                if not closest_cities:
                    actual_route["route"].append(selected_trip)
                    num_of_city_variations += 1
                    continue

                # Choose a random nearby city for a detour trip
                detour_city = random.choice(closest_cities)

                # if this is the first trip
                if selected_trip_index == 0:
                    # add a detour city in from of the original trip or after the original trip
                    if random.choice([True, False]):
                        # Add a detour trip (from the detour city to the original city)
                        trip_varied = {
                            "from": detour_city, "to": selected_trip["from"],
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # Add the original trip (from the original city to the detour city)
                        trip_varied = {
                            "from": selected_trip["from"], "to": selected_trip["to"],
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # update the current route cities list with the new detour city
                        current_route_cities.append(detour_city)

                        # increase the number of city variations
                        num_of_city_variations += 1
                    else:
                        # Add the original trip (from the original city to the detour city)
                        trip_varied = {
                            "from": selected_trip["from"], "to": detour_city,
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # Add a detour trip (from the detour city to the original city)
                        trip_varied = {
                            "from": detour_city, "to": selected_trip["to"],
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # update the current route cities list with the new detour city
                        current_route_cities.append(detour_city)

                        # increase the number of city variations
                        num_of_city_variations += 1
                else:
                    # Randomly decide to make a minor detour in middle of the route
                    if random.choice([True, False]):
                        # Add a detour trip (from the original city to the detour city)
                        trip_varied = {
                            "from": selected_trip["from"], "to": detour_city,
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # Add the original trip (from the detour city to the original destination)
                        trip_varied = {
                            "from": detour_city, "to": selected_trip["to"],
                            "merchandise": selected_trip["merchandise"]
                        }
                        # trip's merchandise variation
                        trip_varied["merchandise"] = trip_merchandise_variations(trip_varied)
                        actual_route["route"].append(trip_varied)

                        # update the current route cities list with the new detour city
                        current_route_cities.append(detour_city)

                        # increase the number of city variations
                        num_of_city_variations += 1
                    else:
                        # Keep the original trip
                        actual_route["route"].append(selected_trip)
                        continue
            num_of_city_variations = 0
        elif action == "merchandise_variation":
            # add variations in the merchandise
            actual_route["route"] = adjust_merchandise(copy.deepcopy(standard_route_["route"]))

        # add actual route variation to the list
        actual_route_variations_of_current_std_route.append(actual_route)

    return actual_route_variations_of_current_std_route


def generate_actual_routes(standard_routes_, drivers_, min_variations_per_driver=1, max_variations_per_driver=3):
    """
    Generate a set of actual routes with variations from the given standard routes and drivers.

    :param standard_routes_: The standard routes to use.
    :param drivers_: The drivers to use.
    :param min_variations_per_driver: The minimum number of variations for each standard route for each driver.
    :param max_variations_per_driver: The maximum number of variations for each standard route for each driver.

    :return: A set of actual routes with variations from the given standard routes and drivers.
    """
    actual_routes = []

    for std_route in standard_routes_:
        print(f"Generating actual routes for standard route {std_route['id']}")
        # Generate a random number of variations for each standard route
        num_variations = random.randint(min_variations_per_driver, max_variations_per_driver)
        current_actual_routes_variations = create_actual_routes_with_variations_for_std_route(std_route, num_variations)
        print(f"Generated {len(current_actual_routes_variations)} actual route variations.")
        # assign the driver to the actual route
        for actual_route in current_actual_routes_variations:
            actual_route["driver"] = random.choice(drivers_)
            # add the actual route to the list of actual routes
            actual_routes.append(actual_route)

    print(f"Generated {len(actual_routes)} actual routes with variations")
    return actual_routes
