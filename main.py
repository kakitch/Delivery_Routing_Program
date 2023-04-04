# Kyle Kitchens
# Student ID: 001417219
import csv
import sys
import datetime
import package
from optimization import *
from variables import *
import datetime

# WGUPS Routing Program.
# overview of flow and time complexity.
# hash_table is instantiated and loaded - O(n^2)
# distance_table is instatiated and loaded - O(3n^2)
# address_table is instantiated and loaded - O(n)
# load trucks is called - O(n^4)
# option is selected - O(1)
# truck_reorganize route is called 3 times for each truck - O(3(n^4 + n^2 + n))
# either get_status_update is called or get delivery time is called for each package, both O(n^2 + 2n)
# for O(n^3 + 2n^2)
# total time complexity: O(4n^4 + n^3 + 9n^2 +2n)

# O(1)
def launch_main_menu():
    # launches main menu, put in while loop to reload for bad input or for completed command until option 4 is
    # called for sys.exit()
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

# returns all package information after and what time they were delivered along with total mileage.
# Also updates the address of package 9
# O(n)
def option_1():
    # since this option is for completed deliveries only, package 9 address info is updated
    hash_table.search(9).address = "410 S State St"
    hash_table.search(9).city = "Salt Lake City"
    hash_table.search(9).state = "UT"
    hash_table.search(9).state = "84111"
    # truck reorganized stops called for all trucks
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    # get delivery time is called for all packages and output is printed
    for i in range(hash_table.total_packages()):
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
    # total mileage is determined and output
    t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
    t2 = determine_total_mileage_per_truck(truck2.stop_sequence)
    t3 = determine_total_mileage_per_truck(truck3.stop_sequence)
    tt = t1+t2+t3
    tt = round(tt, 1)
    print("total Mileage:", tt)

# returns information about a single package at a certain time
# Also updates the address of package 9 if input time is after 10:20
# O(n)
def option_2(id, time):
    t = conv_string_to_timedelta(time)
    # truck reorganize stops is called
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    # if time is after 10:20, package 9 is updated and truck reorganize stops is run again for address update
    if t > datetime.timedelta(0, 0, 0, 0, 20, 10):
        # update package # 9 to 410 S State St., Salt Lake City, UT 84111
        hash_table.search(9).address = "410 S State St"
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        truck_reorganize_stops(truck3)
    # gets the package status for single package at a given time
    result = get_status_update(id,t)
    package = result[0]
    # prints package info
    print("Package ID:", package.id,
          "Address:", package.address,
          package.city,
          package.state,
          package.zip, "Weight:",
          package.weight,
          "Deadline:",
          package.deadline,
          "Status:", package.status)

# returns information about all packages at a certain time
# Also updates the address of package 9 if input time is after 10:20
# O(n)
def option_3(time):
    t = conv_string_to_timedelta(time)
    # truck reorganize stops is called for all trucks for optimization
    truck_reorganize_stops(truck1)
    truck_reorganize_stops(truck2)
    truck_reorganize_stops(truck3)
    if t > datetime.timedelta(0, 0, 0, 0, 20, 10):
        # update package # 9 to 410 S State St., Salt Lake City, UT 84111 and optimize stops again to account
        # address change
        hash_table.search(9).address = "410 S State St"
        hash_table.search(9).city = "Salt Lake City"
        hash_table.search(9).state = "UT"
        hash_table.search(9).state = "84111"
        truck_reorganize_stops(truck3)
    # gets status of all packages and prints package information
    for i in range(hash_table.total_packages()):
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
              #"Truck ID:", tr
              )


load_trucks()
launch_main_menu()







