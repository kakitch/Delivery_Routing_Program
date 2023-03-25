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
        if "Delayed" in hash_table.search(row).notes:
            holding.append(row)
            package_list.remove(row)
        elif "Wrong address" in hash_table.search(row).notes:
            holding.append(row)
            package_list.remove(row)
        elif "Must be delivered with" in hash_table.search(row).notes:
            group.append(row)
            temp_list.append(row)

    for row in group:
        temp_list = temp_list + re.findall('\d+', hash_table.search(row).notes)

    for row in temp_list:
        row = int(row)
        if row not in group:
            group.append(row)

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

    stop_list_one.update(stops)

    truck1.manifest = stop_list_one
    truck2.manifest = stop_list_two
    truck3.manifest = stop_list_three


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

    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)

    dt = time_from_hub_to_delivery(mileage_to_stop)
    st = datetime.timedelta(0, 0, 0, 0, 0, 8)

    if truck == truck3:
        st = datetime.timedelta(0, 0, 0, 0, 20, 10)

    dt = st + dt

    if st < time < dt:
        hash_table.search(id).status = "en route"

    if time > dt:
        dt = str(dt)
        dt = ':'.join(str(dt).split(':')[:2])
        if dt[1] != ":":
            if int(dt[0] + dt[1]) >= 13:
                dt = dt + "PM"
            else:
                dt = dt + "AM"
        else:
            dt = dt + "AM"
        hash_table.search(id).status = "Delivered at: " + dt

    package = hash_table.search(id)
    return package, dt, truck.id


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

    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)

    dt = time_from_hub_to_delivery(mileage_to_stop)
    st = datetime.timedelta(0, 0, 0, 0, 0, 8)

    if truck == truck3:
        st = datetime.timedelta(0, 0, 0, 0, 20, 10)

    dt = st + dt
    dt = str(dt)
    dt = ':'.join(str(dt).split(':')[:2])

    if dt[1] != ":":
        if int(dt[0] + dt[1]) >= 13:
            dt = dt + "PM"
        else:
            dt = dt + "AM"
    else:
        dt = dt + "AM"

    hash_table.search(id).status = "Delivered at: " + dt

    package = hash_table.search(id)
    return package, dt, truck.id


def truck_reorganize_stops(truck):
    p = list(truck.manifest.values())
    pn = []
    for row in p:
        pn = pn + row
    set_dict = {}
    set_list = []
    for row in pn:
        address = address_list.find_address_index(hash_table.search(row).address)
        for row in pn:
            if address_list.find_address_index(hash_table.search(row).address) == address:
                set_list.append(row)
        set_dict[address] = set_list
        set_list = []

    truck.manifest.clear()
    truck.manifest = set_dict

    truck_stops = list(truck.manifest.keys())

    temp = truck_stops[:]
    truck_stops.append(0)
    truck_stops.append(0)
    truck_stops.insert(0, truck_stops.pop(truck_stops.index(0)))

    for j in range(len(truck_stops) - 2):
        closest = -1
        item_swapped = 0
        for row in temp:
            mileage = find_distance(truck_stops[j], row)
            if mileage < closest or closest == -1:
                closest = mileage
                truck_stops.insert(j + 1, truck_stops.pop(truck_stops.index(row)))
                item_swapped = truck_stops[j + 1]

        temp.remove(item_swapped)

    truck.stop_sequence = truck_stops
