class Truck:

    def __init__(self, id):
        self.id = id
        self.manifest = {}
        self.stop_sequence = []

    def print_truck(self):
        print(self.id, self.manifest)

    def load_truck(self, load):
        self.manifest.update(load)


class Driver:

    def __init__(self, id_number):
        self.id = id_number
        self.current_truck = None

    def assign_truck(self, truck):
        self.current_truck = truck
