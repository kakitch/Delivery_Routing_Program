# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import sys
import datetime
import package
from optimization import *
from variables import *
import datetime

def load_trucks():
    loads = load_optimize()


    truck1.load_truck(loads[0])
    truck2.load_truck(loads[1])
    truck3.load_truck(loads[2])

    delivery_sequence_optimize()





#G.  Provide an interface for the user to view the status and info (as listed in part F) of any package at any time,
# and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route,
# or delivered. Delivery status must include the time.)
#   1.  Provide screenshots to show the status of all packages at a time between 8:35 a.m. and 9:25 a.m.
#   2.  Provide screenshots to show the status of all packages at a time between 9:35 a.m. and 10:25 a.m.
#   3.  Provide screenshots to show the status of all packages at a time between 12:03 p.m. and 1:12 p.m.
#   H.  Provide a screenshot or screenshots showing successful completion of the code, free from runtime errors or warnings,
#       that includes the total mileage traveled by all trucks.

def launch_main_menu():
    valid = False
    while valid == False:

        print("************************************************************************")
        print("1. Display status for package deliveries and total mileage")
        print("2. Display status for any package at a given Time")
        print("3. Display status for all pagages at a given time")
        print("4. Exit")
        command =  input("Choose an option:")

        if command == "1":
            option_1()
            valid = True
        elif command == "2":
            id = input("Input Package ID:")
            time = input("Input Time in HH:MM Format:")
            option_2(id, time)
            valid = True
        elif command == "3":
            time = input("Input Time in HH:MM Format:")
            option_3(time)
            valid = True
        elif command == "4":
            sys.exit()
        else:
            print("choose a valid option")

def option_1():
    for i in range(len(hash_table.package_list())):
        result = get_delivery_time(i+1)
        package = result[0]
        dt = result[1]
        tr = result[2]
        print("Package ID:", package.id,
              # "Address:", package.address,
              # package.city,
              # package.state,
              # package.zip,
              # "Weight:", package.weight,
              #"Deadline:", package.deadline,
              "Status:", package.status,
              # "notes", package.notes,
              # "Delivery time:", dt,
              #"Truck ID:", tr
              )


def option_2(id, time):
    t = conv_string_to_timedelta(time)
    package = get_status_update(id,t)
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
    for i in range(len(hash_table.package_list())):
        result = get_status_update(i+1, t)
        package = result[0]
        dt = result[1]
        tr = result[2]
        print("Package ID:", package.id,
              # "Address:", package.address,
              # package.city, package.state,
              # package.zip,
              # "Weight:", package.weight,
              # "Deadline:", package.deadline,
              "Status:", package.status,
              # "notes", package.notes,
              # "Delivery time:", dt,
              "Truck ID:", tr
              )

load_trucks()
launch_main_menu()

t1 = determine_total_mileage_per_truck(truck1.stop_sequence)
t2 = determine_total_mileage_per_truck(truck2.stop_sequence)
t3 = determine_total_mileage_per_truck(truck3.stop_sequence)


#print(t1,t2,t3)





