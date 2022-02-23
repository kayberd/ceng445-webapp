class Room:

    def __init__(self, room_id, capacity, description):
        self.id = room_id
        self.capacity = capacity
        self.description = description

    def __str__(self):
        return f"Room: {self.id}"

    def update(self, capacity, description):
        self.capacity = capacity
        self.description = description
