from variables import *


def load_optimize():
    sl1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]  # holding all deadlines except late arrivals
    sl2 = [3, 18, 36, 38, 23, 39, 8, 9, 5, 11, 35, 12, 10, 2, 4, 7]  # 3,18,36,38 have to be on truck 2
    sl3 = [32, 28, 25, 6, 17, 21, 22, 24, 26, 27, 33]  # holds late arrivals, must leave at 9:05

    sl = [sl1, sl2, sl3]

    sd1 = {}
    sd2 = {}
    sd3 = {}

    sd = [sd1, sd2, sd3]

    for i in range(len(sl)):
        for row in sl[i]:
            key = address_list.find_address_index(hash_table.search(row).address)
            v = sd[i].get(key)
            if v is not None:
                sd[i][key] = v + [row]
            else:
                sd[i][key] = [row]

    truck1.manifest = sd1
    truck2.manifest = sd2
    truck3.manifest = sd3

    truck1_stops = list(truck1.manifest.keys())
    truck2_stops = list(truck2.manifest.keys())
    truck3_stops = list(truck3.manifest.keys())

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
    st = datetime.timedelta(hours=8)

    if truck == truck3:
        st = datetime.timedelta(hours=9, minutes=5)
    if truck == truck2:
        t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
        t2 = determine_total_mileage_per_truck(truck2.stop_sequence)
        if t1 < t2:
            st = st + time_from_hub_to_delivery(t1)
        else:
            st = st + time_from_hub_to_delivery(t2)

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

    st = datetime.timedelta(hours=8)

    if truck == truck3:
        st = datetime.timedelta(hours=9, minutes=5)
    if truck == truck2:
        t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
        t2 = determine_total_mileage_per_truck(truck2.stop_sequence)

        if t1 < t2:
            st = st + time_from_hub_to_delivery(t1)
        else:
            st = st + time_from_hub_to_delivery(t2)

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
