class Truck:

    def __init__(self, id):
        self.id = id
        self.manifest = {}
        self.stop_sequence = []
        self.status

    def print_truck(self):
        print(self.id, self.manifest)

    def load_truck(self, load):
        self.manifest.update(load)





