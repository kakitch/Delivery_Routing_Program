import csv
import sys
import datetime
import package
from optimization import *
from variables import *
import datetime

def load_trucks():
    loads = load_optimize()
def launch_main_menu():
    while True == True:
        print("************************************************************************")
        print("1. Display status for package deliveries and total mileage")
        print("2. Display status for any package at a given Time")
        print("3. Display status for all pagages at a given time")
        print("4. Exit")
        command =  input("Choose an option:")

        if command == "1":
            option_1()

        elif command == "2":
            id = input("Input Package ID:")
            time = input("Input Time in HH:MM Format:")
            option_2(id, time)

        elif command == "3":
            time = input("Input Time in HH:MM Format:")
            option_3(time)

        elif command == "4":
            sys.exit()
        else:
            print("choose a valid option")
def option_1():
    hash_table.search(9).address = "410 S State St"
    hash_table.search(9).city = "Salt Lake City"
    hash_table.search(9).state = "UT"
    hash_table.search(9).state = "84111"
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    for i in range(40):
        result = get_delivery_time(i+1)
        package = result[0]
        dt = result[1]
        tr = result[2]
        print("Package ID:", package.id,
              "Address:", package.address,
              package.city,
              package.state,
              package.zip,
              "Weight:", package.weight,
              "Deadline:", package.deadline,
              "Status:", package.status,
              # "notes", package.notes,
              # "Delivery time:", dt,
              # "Truck ID:", tr
              )
    t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
    t2 = determine_total_mileage_per_truck(truck2.stop_sequence)
    t3 = determine_total_mileage_per_truck(truck3.stop_sequence)
    tt = t1+t2+t3
    tt = round(tt, 1)
    print("total Mileage:", tt)
def option_2(id, time):
    t = conv_string_to_timedelta(time)
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    if t > datetime.timedelta(0, 0, 0, 0, 20, 10):
        # update package # 9 to 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St"
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        truck_reorganize_stops(truck3)
    result = get_status_update(id,t)
    package = result[0]
    print("Package ID:", package.id,
          "Address:", package.address,
          package.city,
          package.state,
          package.zip, "Weight:",
          package.weight,
          "Deadline:",
          package.deadline,
          "Status:", package.status)

# Main Menu option 3: Get status for any package at a given time
def option_3(time):
    t = conv_string_to_timedelta(time)
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    if t > datetime.timedelta(0, 0, 0, 0, 20, 10):
        print("hi")
        # update package # 9 to 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St"
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        truck_reorganize_stops(truck3)
    for i in range(40):
        result = get_status_update(i+1, t)
        package = result[0]
        dt = result[1]
        tr = result[2]
        print("Package ID:", package.id,
              "Address:", package.address,
              package.city, package.state,
              package.zip,
              "Weight:", package.weight,
              "Deadline:", package.deadline,
              "Status:", package.status,
              # "notes", package.notes,
              # "Delivery time:", dt,
              "Truck ID:", tr
              )


load_trucks()
launch_main_menu()







