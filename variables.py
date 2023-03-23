from distance import *
import hashtable
import truck

## Variables and functions for global use

hash_table = hashtable.HashTable()
address_list = AddressList()

truck1 = truck.Truck(1)
truck2 = truck.Truck(2)
truck3 = truck.Truck(3)

driver1 = truck.Driver(1)
driver2 = truck.Driver(2)


def conv_string_to_timedelta(string):
    dt = datetime.datetime.strptime(string, "%H:%M")
    dt = datetime.timedelta(0, 0, 0, 0, dt.minute, dt.hour)
    return dt


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

    if time > datetime.timedelta(0, 0, 0, 0, 20, 10):
        # 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St."
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        # TODO rework package item attributes directly into hash table and make update address method

    if truck == truck3:
        start_time = datetime.timedelta(0, 0, 0, 0, 20, 10)
        # TODO: add line to reoptimize truck 3 route. DOUBLE CHECK ADDRESS CHANGE ON PACKAGE #9 TAKES EFFECT

    dt = start_time + dt

    if time > dt:
        hash_table.search(id).status = "Delivered at:" + str(dt)

    package = hash_table.search(id)
    return package, dt, truck.id

    # TODO rework hashtable with update method
