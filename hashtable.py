import csv
from package import Package

class HashTable:

    # instantiates a HashTable object with 10 empty buckets. called once in Variables.py
    # O(n)
    def __init__(self, initial_capacity=10):

        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
        self.load_hash()

    # loads CSV input and instantiates package objects while also inserting them into the hashtable.
    # The Hashtable structure is that the key is the package ID, and the value is the package object.
    # O(n)
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

    # inserts a package into the hashtable
    # O(1)
    def insert(self, package):
        # get the bucket list where this item will go.
        id = package.id
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        key_value = [id, package]
        bucket_list.append(key_value)
        return True

    # Package search method via hash table
    # passes key to method and returns package object
    # O(n)
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:

            if kv[0] == key:
                return kv[1]  # value
        return None

    # returns the quantity of all packages.
    # O(n^2)
    def total_packages(self):
        l = []
        for row in self.table:
            rowlist = row
            for row in rowlist:
                l.append(row[0])
        return len(l)