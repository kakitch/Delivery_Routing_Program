import csv
import datetime


# instantiates the distance_table, called once in distance.py (line96). the structure of distance table is a dictionary
# of lists that can be easily accessed by passing in the key of the dictionary and index of the list.
# the lists are assembled by concatenating the vertical and horizontal portions of the CSV file according to
# each row.
# O(3n^2)
def distance_table():
    distance = {}
    temp_table = []
    with open("CSV/distance.csv") as csvFile:
        temp_table = list(csv.reader(csvFile, delimiter=','))
        for row in temp_table:
            r = temp_table.index(row)
            row_list = row
            for row in row_list:
                c = row_list.index(row)
                if row != '':
                    temp_table[r][c] = float(row)
    i = 0

    for row in temp_table:
        current_index = temp_table.index(row)
        horizontal_list = []
        vertical_list = []
        # gathers the horizontal elements in the temp table from the csv file
        for row in temp_table[current_index]:
            index = temp_table[current_index].index(row)
            if index <= current_index:
                horizontal_list.append(row)
        # gathers the vertical elements in the temp table from the csv file
        for row in temp_table:
            index = temp_table.index(row)
            if index > current_index:
                vertical_list.append(row[current_index])
        # concatenates the two lists for a list of all associated distance
        mileage_list = horizontal_list + vertical_list

        # creates a new entry in the distance table
        distance[current_index] = mileage_list
    # print(distance)
    return distance


# finds distance by cross-referencing the indexes in the distance table
# 0(2)
def find_distance(current_index, new_address_index):
    return distance_table[current_index][new_address_index]


# determines total mileage per truck including mileage returning to hub, based on truck.stop_sequence
# O(n)
def determine_total_mileage_per_truck(sequence):
    distance = 0.0
    for i in range(len(sequence) - 1):
        new = find_distance(sequence[i], sequence[i + 1])
        distance = distance + new
    return distance


# determines mileage from hub to the address index(id parameter). starts at first index of truck.stop_sequence
# and iterates until the index value is reached adding up the distance of each leg of the route.
# O(n)
def determine_mileage_to_stop(id, sequence):
    index = sequence.index(id)
    distance = 0.0
    for i in range(index):
        new = find_distance(sequence[i], sequence[i + 1])
        distance = distance + new
    return distance


# calculates the time based by passing in distance in miles. dividing by 18 for 18mph and creating a
# datetime.timedelta object based on the value of dt variable as hours.
# O(1)
def time_from_hub_to_delivery(distance):
    dt = distance / 18
    t = datetime.timedelta(0, 0, 0, 0, 0, dt)
    return t


class AddressList:
    # instantiates AddressList and creates a list of addresses, called once in variables.py
    # O(n)
    def __init__(self):
        self.table = []
        with open("CSV/addresses.csv") as csvFile:
            self.table = list(csv.reader(csvFile, delimiter=','))

    # finds the index of an address on address_list. The indexes correspond to the same index in the distance table.
    # O(n)
    def find_address_index(self, address: str) -> int:
        for row in self.table:
            if address in row[2]:
                return int(row[0])


# instantiates the distance table
distance_table = distance_table()
