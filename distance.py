import csv
import datetime


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

        for row in temp_table[current_index]:
            index = temp_table[current_index].index(row)
            if index <= current_index:
                horizontal_list.append(row)

        for row in temp_table:
            index = temp_table.index(row)
            if index > current_index:
                vertical_list.append(row[current_index])

        mileage_list = horizontal_list + vertical_list
        distance[current_index] = mileage_list
    # print(distance)
    return distance


def find_distance(current_index, new_address_index):
    return distance_table[current_index][new_address_index]


def determine_total_mileage_per_truck(sequence):
    distance = 0.0
    for i in range(len(sequence) - 1):
        new = find_distance(sequence[i], sequence[i + 1])
        distance = distance + new
    return distance


def determine_mileage_to_stop(id, sequence):
    index = sequence.index(id)
    distance = 0.0
    for i in range(index):
        new = find_distance(sequence[i], sequence[i + 1])
        distance = distance + new
    return distance


def time_from_hub_to_delivery(distance):
    dt = distance / 18
    t = datetime.timedelta(0, 0, 0, 0, 0, dt)
    return t


class AddressList:
    def __init__(self):
        self.table = []
        with open("CSV/addresses.csv") as csvFile:
            self.table = list(csv.reader(csvFile, delimiter=','))

    def find_address_index(self, address: str) -> int:
        for row in self.table:
            if address in row[2]:
                return int(row[0])


distance_table = distance_table()
