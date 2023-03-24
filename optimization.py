import re
from typing import List, Any

from variables import *


def find_packages_with_like_addresses():
    package_list = hash_table.package_list()
    set_dict = {}
    set_list = []
    for row in package_list:
        address = address_list.find_address_index(hash_table.search(row).address)
        for row in package_list:
            if address_list.find_address_index(hash_table.search(row).address) == address:
                set_list.append(row)
        set_dict[address] = set_list
        set_list = []
    return set_dict

    # does initial handling of package notes. ie "deliver with, can only be on truck 2, must be delivered with"


def package_note_handler():
    # variables package_list and package_list_total are declared. Package_list_total will be unaffected as for loop
    # removes id numbers from package_list
    package_list_total = hash_table.package_list()
    package_list = hash_table.package_list()
    holding = []
    group = []
    temp_list = []
    two = []
    for row in package_list_total:
        if "Can only be on truck 2" in hash_table.search(row).notes:
            two.append(row)
            package_list.remove(row)
            # print("truck2:", truck2.manifest)
        if "Delayed" in hash_table.search(row).notes:
            holding.append(row)
            package_list.remove(row)
            # print("holding:", holding)
        elif "Wrong address" in hash_table.search(row).notes:
            holding.append(row)
            package_list.remove(row)
            # print("holding:", holding)
        elif "Must be delivered with" in hash_table.search(row).notes:
            group.append(row)
            temp_list.append(row)

    for row in group:
        temp_list = temp_list + re.findall('\d+', hash_table.search(row).notes)

    for row in temp_list:
        row = int(row)
        if row not in group:
            group.append(row)
            # print(group)

    for row in package_list:
        if row in group:
            package_list.remove(row)
    return package_list, holding, group, two


def load_optimize():
    stops = find_packages_with_like_addresses()

    groups = package_note_handler()[2]  # packages that have to go out with others
    holding = package_note_handler()[1]  # packages that we are not ready for delivery

    # one, two, three represent loads to go onto trucks
    two = package_note_handler()[3]  # items that go on truck 2 only

    # print("stops before removing holding: ", stops)
    stop_list_one = {}
    stop_list_two = {}
    stop_list_three = {}

    # removes packages that need to wait to be delivered for whatever reason
    for row in holding:
        stop_list_three[address_list.find_address_index(hash_table.search(row).address)] = stops.pop(
            address_list.find_address_index(hash_table.search(row).address))

    # removes packages that need to be delivered on truck2 from stops
    for row in two:
        stop_list_two[address_list.find_address_index(hash_table.search(row).address)] = stops.pop(
            address_list.find_address_index(hash_table.search(row).address))

    for row in groups:
        if address_list.find_address_index(hash_table.search(row).address) in stops.keys():
            stop_list_one[address_list.find_address_index(hash_table.search(row).address)] = stops.pop(
                address_list.find_address_index(hash_table.search(row).address))

    # section determines the closest packages for load for truck 2
    # determines number of items in stop list 2 Dict
    sl2 = []
    for row in stop_list_two:
        sl2 = sl2 + stop_list_two[row]
    # print(stops.keys())
    # print(stop_list_two.keys())
    while len(sl2) < 16:
        closest = -1.0
        closest_address_index = -1
        for row in stop_list_two:
            current_row = row
            for row in stops:
                if find_distance(current_row, row) < closest or closest == -1:
                    closest = find_distance(current_row, row)
                    closest_address_index = row

        stop_list_two[closest_address_index] = stops.pop(closest_address_index)
        sl2 = sl2 + stop_list_two[closest_address_index]

    # print(stop_list_two.values())
    # print("stops after removing notes", stops)
    # # print("two: ", two)
    # # print("groups: ", groups)
    # # print("holding: ", holding)
    stop_list_one.update(stops)
    # print(stops)
    # print("stop_list_one: ", stop_list_one)
    # print("stop_list_two: ", stop_list_two)
    # print("stop_list_three: ", stop_list_three)

    return stop_list_one, stop_list_two, stop_list_three


def delivery_sequence_optimize():
    truck1_stops = list(truck1.manifest.keys())
    truck2_stops = list(truck2.manifest.keys())
    truck3_stops = list(truck3.manifest.keys())

    truck_stop_list = [truck1_stops, truck2_stops, truck3_stops]

    for i in range(len(truck_stop_list)):
        temp = truck_stop_list[i][:]
        truck_stop_list[i].append(0)
        truck_stop_list[i].append(0)
        truck_stop_list[i].insert(0, truck_stop_list[i].pop(truck_stop_list[i].index(0)))

        for j in range(len(truck_stop_list[i]) - 2):
            closest = -1
            item_swapped = 0
            for row in temp:
                mileage = find_distance(truck_stop_list[i][j], row)
                if mileage < closest or closest == -1:
                    closest = mileage
                    truck_stop_list[i].insert(j + 1, truck_stop_list[i].pop(truck_stop_list[i].index(row)))
                    item_swapped = truck_stop_list[i][j + 1]

            temp.remove(item_swapped)

    truck1.stop_sequence = truck1_stops
    truck2.stop_sequence = truck2_stops
    truck3.stop_sequence = truck3_stops


def get_status_update(id, time):
    truck_list = [list(truck1.manifest.values()), list(truck2.manifest.values()), list(truck3.manifest.values())]
    truck = truck1
    id = int(id)
    for i in range(len(truck_list)):
        temp = []
        for row in truck_list[i]:
            temp = temp + row
        for row in temp:
            if id == row and i == 0:
                truck = truck1
                break
            if id == row and i == 1:
                truck = truck2
                break
            if id == row and i == 2:
                truck = truck3
                break

    stop_number = 0
    for row in truck.manifest:
        if id in truck.manifest[row]:
            stop_number = row

    total_mileage = determine_total_mileage_per_truck(truck.stop_sequence)

    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)

    dt = time_from_hub_to_delivery(mileage_to_stop)
    start_time = datetime.timedelta(0, 0, 0, 0, 0, 8)

    if time > datetime.timedelta(0, 0, 0, 0, 20, 10) and id == 9:
        # 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St."
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"

    if truck == truck3:
        start_time = datetime.timedelta(0, 0, 0, 0, 20, 10)
        # TODO: add line to reoptimize truck 3 route. DOUBLE CHECK ADDRESS CHANGE ON PACKAGE #9 TAKES EFFECT

    dt = start_time + dt

    if time > dt:
        hash_table.search(id).status = "Delivered at:" + str(dt)

    package = hash_table.search(id)
    return package, dt, truck.id

    # TODO rework hashtable with update method


def get_delivery_time(id):
    truck_list = [list(truck1.manifest.values()), list(truck2.manifest.values()), list(truck3.manifest.values())]
    truck = truck1
    id = int(id)
    for i in range(len(truck_list)):
        temp = []
        for row in truck_list[i]:
            temp = temp + row
        for row in temp:
            if id == row and i == 0:
                truck = truck1
                break
            if id == row and i == 1:
                truck = truck2
                break
            if id == row and i == 2:
                truck = truck3
                break

    stop_number = 0
    for row in truck.manifest:
        if id in truck.manifest[row]:
            stop_number = row

    total_mileage = determine_total_mileage_per_truck(truck.stop_sequence)

    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)

    dt = time_from_hub_to_delivery(mileage_to_stop)
    start_time = datetime.timedelta(0, 0, 0, 0, 0, 8)

    if id == 9:
        # 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St."
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        # TODO need to rework truck route

    if truck == truck3:
        start_time = datetime.timedelta(0, 0, 0, 0, 20, 10)
        # TODO: add line to reoptimize truck 3 route. DOUBLE CHECK ADDRESS CHANGE ON PACKAGE #9 TAKES EFFECT

    dt = start_time + dt

    hash_table.search(id).status = "Delivered at:" + str(dt)

    package = hash_table.search(id)
    return package, dt, truck.id
