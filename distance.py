import csv


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


def determine_total_mileage_per_truck(stop_order):
    distance = 0.0
    for i in range(len(stop_order) - 1):
        new = find_distance(stop_order[i], stop_order[i + 1])
        distance = distance + new
    return distance


class AddressList:
    def __init__(self):
        self.table = []
        with open("CSV/addresses.csv") as csvFile:
            self.table = list(csv.reader(csvFile, delimiter=','))

    def find_address_index(self, address: str) -> int:
        for row in self.table:
            if address in row[2]:
                return int(row[0])

    def find_distance_between(self, current_index: int, new_index: int):
        return find_distance(current_index, new_index)

    def update(self, name, address, index):
        for row in self.table:
            if row[1] != name or row[2] != address and row[0] == index:
                row[1] = name
                row[2] = address

    def find_closest_address(self, current_index) -> int:
        address_distances = list(distance_table[current_index])
        address_distances[current_index] = max(address_distances)
        closest_distance = min(address_distances)
        index = address_distances.index(closest_distance)
        return current_index, index, closest_distance

    #
    #     # horizontal_list = []
    #     # vertical_list = []
    #     #
    #     # for row in Distance().table[current_index]:
    #     #     index = Distance().table[current_index].index(row)
    #     #     if index < current_index:
    #     #         horizontal_list.append(row)
    #     #
    #     # for row in Distance().table:
    #     #     index = Distance().table.index(row)
    #     #     if index > current_index:
    #     #         vertical_list.append(row[current_index])
    #
    #     mileage_list = horizontal_list + vertical_list
    #     nearest = mileage_list[0]
    #     nearest_index = 0
    #     for row in mileage_list:
    #         i = mileage_list.index(row)
    #         if row < nearest:
    #             nearest = row
    #             nearest_index = mileage_list.index(nearest)
    #
    #     return_list = [nearest_index + 1, nearest]
    #     return return_list


distance_table = distance_table()
