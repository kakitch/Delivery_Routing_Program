from distance import *
import hashtable
import truck

# Variables and functions for global use

hash_table = hashtable.HashTable()
address_list = AddressList()

truck1 = truck.Truck(1)
truck2 = truck.Truck(2)
truck3 = truck.Truck(3)


def conv_string_to_timedelta(string):
    dt = datetime.datetime.strptime(string, "%H:%M")
    dt = datetime.timedelta(0, 0, 0, 0, dt.minute, dt.hour)
    return dt


