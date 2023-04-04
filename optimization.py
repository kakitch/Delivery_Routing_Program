from variables import *


# load_trucks manually associates package id's addresses and then with trucks
# load trucks is called, time complexity is  O^n2 and is dependent on hashtable.search.py which is O^n and
# address_table.search which is also O^n this function is independent.
# total time complexity: O(n^4)
def load_trucks():
    # lists of packages are initialized, there one list for every truck
    sl1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]  # holding all deadlines except late arrivals
    sl2 = [3, 18, 36, 38, 23, 39, 8, 9, 5, 11, 35, 12, 10, 2, 4, 7]  # 3,18,36,38 have to be on truck 2
    sl3 = [32, 28, 25, 6, 17, 21, 22, 24, 26, 27, 33]  # holds late arrivals, must leave at 9:05

    # list of list is created for use in a for loop
    sl = [sl1, sl2, sl3]

    #  dictionaries are created, one for every truck
    sd1 = {}
    sd2 = {}
    sd3 = {}

    # list of dictionaries is created for a for loop.
    sd = [sd1, sd2, sd3]

    # this block determines the address of packages and inserts them into a corresponding dictionary where
    #  the key is the address index according to the address list and a list of packages is the value.
    for i in range(len(sl)):
        for row in sl[i]:
            key = address_list.find_address_index(hash_table.search(row).address)
            v = sd[i].get(key)
            if v is not None:
                sd[i][key] = v + [row]
            else:
                sd[i][key] = [row]

    # truck manifest attributes assigned with dictionaries
    truck1.manifest = sd1
    truck2.manifest = sd2
    truck3.manifest = sd3

    # truck stops lis is initialized as a list of stops for each truck and assigned to truck stop sequence
    # attribute.
    truck1_stops = list(truck1.manifest.keys())
    truck2_stops = list(truck2.manifest.keys())
    truck3_stops = list(truck3.manifest.keys())
    truck1.stop_sequence = truck1_stops
    truck2.stop_sequence = truck2_stops
    truck3.stop_sequence = truck3_stops


# get_status_update gets a packages status based on a time value passed into the function.
# worst case is O(n^2 + 2n)
def get_status_update(id, time):
    truck_list = [list(truck1.manifest.values()), list(truck2.manifest.values()), list(truck3.manifest.values())]
    truck = truck1
    id = int(id)
    # this block of  determines what truck a package is on and sets the truck variable accordingly
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

    # determines the stop number in the stop sequence
    stop_number = 0
    for row in truck.manifest:  # O(n)
        if id in truck.manifest[row]:
            stop_number = row
    # passes in the stop number and the stop sequence and returns the mileage
    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)
    # determines delivery time based on miles to the stop
    dt = time_from_hub_to_delivery(mileage_to_stop)
    st = datetime.timedelta(hours=8)

    # truck 3 leaves at 9:05
    if truck == truck3:
        st = datetime.timedelta(hours=9, minutes=5)
    #  truck 2 will not leave until another truck returns, this block determines which truck returns first
    if truck == truck2:
        t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
        t2 = determine_total_mileage_per_truck(truck2.stop_sequence)
        if t1 < t2:
            st = st + time_from_hub_to_delivery(t1)
        else:
            st = st + time_from_hub_to_delivery(t2)
    # adds the start time to the delivery time to obtain the time a package id was delivered.
    dt = st + dt
    # determines if the package is en route or delivered. all package objects are initialized with a status of
    #  "at the hub". if the time variable is greater than the delivery time a time string is formated
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

    # package object, delivery time, and truck id are returned.
    package = hash_table.search(id)
    return package, dt, truck.id


# get_delivery_time calculates the current status of a package given its ID. Called by Option 1 of main menu.
# worst case is O(n^2 + 2n)
def get_delivery_time(id):
    # the packages from every truck are put into a list separated by trucks
    truck_list = [list(truck1.manifest.values()), list(truck2.manifest.values()), list(truck3.manifest.values())]
    # truck variable is initialized as truck1
    truck = truck1
    id = int(id)

    # this block of  determines what truck a package is on and sets the truck variable accordingly
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

    # determines the stop number in the stop sequence
    stop_number = 0
    for row in truck.manifest:
        if id in truck.manifest[row]:
            stop_number = row

    # passes in the stop number and the stop sequence and returns the mileage
    mileage_to_stop = determine_mileage_to_stop(stop_number, truck.stop_sequence)
    # determines delivery time based on miles to the stop
    dt = time_from_hub_to_delivery(mileage_to_stop)

    st = datetime.timedelta(hours=8)
    # truck 3 leaves at 9:05
    if truck == truck3:
        st = datetime.timedelta(hours=9, minutes=5)

    #  truck 2 will not leave until another truck returns, this block determines which truck returns first
    if truck == truck2:
        t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
        t2 = determine_total_mileage_per_truck(truck2.stop_sequence)

        if t1 < t2:
            st = st + time_from_hub_to_delivery(t1)
        else:
            st = st + time_from_hub_to_delivery(t2)

    # adds the start time to the delivery time to obtain the time a package id was delivered.
    dt = st + dt
    # this block formats the output status string that is saved to the package object. since this only used
    # option 1, the only option is to input a delivered status with a corresponding time.
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
    # package, delivery time, and the truck id is returned
    package = hash_table.search(id)
    return package, dt, truck.id


# truck_reorganize_stops takes package data and sorts by the address to find packages with the same address
# on the same truck and groups then. It then it takes the index of those addresses according to the
# distance table and calculates the closest address according to its current address index as it iterates
# through the list of stops.
# O(n^4 + n^2 + n)
def truck_reorganize_stops(truck):
    # a list of packages "p" on the truck is initialized, but they are a still a list of lists
    p = list(truck.manifest.values())
    # all the lists are combined into a single level list
    pn = []
    for row in p:
        pn = pn + row

    # like addresses are combined into a dictionary  with the key as address index and package as the list of values
    # this is done to account for changes in address
    set_dict = {}
    set_list = []
    for row in pn:
        address = address_list.find_address_index(hash_table.search(row).address)
        for row in pn:
            if address_list.find_address_index(hash_table.search(row).address) == address:
                set_list.append(row)
        set_dict[address] = set_list
        set_list = []
    # the truck manifest is cleared and reset with the new values
    truck.manifest.clear()
    truck.manifest = set_dict

    # list of all the stops for this truck
    truck_stops = list(truck.manifest.keys())

    temp = truck_stops[:]   # a copy is made
    truck_stops.append(0)
    truck_stops.append(0)
    truck_stops.insert(0, truck_stops.pop(truck_stops.index(0)))  # 0's put in first and last position

    # nearest neighbor algorithm
    for j in range(len(truck_stops) - 2): # for loop with the length of temp
        closest = -1                      # closest initialized
        item_swapped = 0                  # item swapped initialized
        for row in temp:
            mileage = find_distance(truck_stops[j], row)  # determines mileage to every stop listed in temp
            if mileage < closest or closest == -1:        # if the mileage is less than closest or closest is the
                closest = mileage                         # initialized value, then closest is assigned a new mileage and items
                truck_stops.insert(j + 1, truck_stops.pop(truck_stops.index(row)))   #are swapped
                item_swapped = truck_stops[j + 1]
        temp.remove(item_swapped)                         # the item that was swapped is removed from the temp list

    truck.stop_sequence = truck_stops  # the list of stops is assigned to the truck stop sequence attribute.
