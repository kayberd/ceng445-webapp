class RoomList:
    def __init__(self):
        self.room_list = list()

    def __str__(self):
        room_list_string = ""
        for room in self.room_list:
            room_list_string += str(room) + " "
        return room_list_string

    def addRoom(self, roomid):
        self.room_list.append(roomid)

    def removeRoom(self, roomid):
        self.room_list.remove(roomid)
