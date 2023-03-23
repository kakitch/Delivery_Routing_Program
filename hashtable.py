import csv
from package import Package


class HashTable:

    def __init__(self, initial_capacity=10):

        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
        self.load_hash()

    def load_hash(self):
        with open("CSV/package.csv") as csvFile:
            read_csv = list(csv.reader(csvFile, delimiter=','))

            for row in read_csv:
                # instantiates packages with attributes from row package parameters: (row[0] = id, row[1] = address,
                # row[2] = city, row[3] = state, row[4] = zip_code, row[5] = deadline, row[6] = weight, row[7] = notes
                if len(row) == 7:
                    package = Package(int(row[0]), row[1], row[2], row[3], int(row[4]), row[5], row[6], None)
                else:
                    package = Package(int(row[0]), row[1], row[2], row[3], int(row[4]), row[5], row[6], row[7])
                # loads package into hash
                self.insert(package)

    def insert(self, package):
        # get the bucket list where this item will go.
        id = package.id
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        key_value = [id, package]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:

            if kv[0] == key:
                return kv[1]  # value
        return None


    def print_table(self):
        for row in self.table:
            row_list = row
            for row in row_list:
                print(row[0], row[1].address, row[1].city, row[1].state, row[1].zip, row[1].deadline, row[1].notes,
                      row[1].status)

    def package_list(self):
        package_list = []
        for row in self.table:
            row_list = row
            for row in row_list:
                package_list.append(row[0])

        return package_list
