
# Note: This Queue class is sub-optimal. Why?


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Graph:

    """Represent a graph as a dictionary of rooms mapping labels to doors."""

    def __init__(self):
        self.rooms = {}

    def add_room(self, room_id, exits):
        """
        Add a room to the graph.
        """
        if not room_id in self.rooms:
            self.rooms[room_id] = {x: '?' for x in exits}

    def connect_rooms(self, room1_id, room2_id, direction):
        """
        Add a directed edge to the graph.
        """
        reverse_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}[direction]

        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room1_id][direction] = room2_id
            self.rooms[room2_id][reverse_dir] = room1_id
        else:
            raise IndexError("That room does not exist.")

    def get_connected_rooms(self, room_id, visited=False):
        """
        Get exits from a room.
        """
        if visited == True:  # return only previously visited neighboring rooms
            return [exit for exit in self.rooms[room_id] if self.rooms[room_id][exit] != '?']
        # return unvisited neighboring rooms
        return [exit for exit in self.rooms[room_id] if self.rooms[room_id][exit] == '?']

    def path_to_directions(self, path):
        traversal = []
        current_room = path.pop(0)
        while len(path) > 0:
            next_room = path.pop(0)
            reverse_keys = {value: key for key,
                            value in self.rooms[current_room].items()}
            traversal.append(reverse_keys[next_room])
            current_room = next_room
        return traversal

    def bfs(self, starting_room):
        """
        Return a list containing the shortest path from
        starting_room to destination_room in
        breadth-first order.
        """

        # Create an empty queue and enqueue the starting room ID
        q = Queue()
        q.enqueue([starting_room])

        # Create an empty Set to store visited rooms
        visited = set()

        # While the queue is not empty...
        while q.size():
            # Dequeue the first path
            path = q.dequeue()
            # Look at the last room in the path...
            current_room = path[-1]
            # And if we've found a room with an unopened door, return our path to that room
            if '?' in self.rooms[current_room].values():
                # Return path as directions
                return [path, self.path_to_directions(path)]

            # If the room has not been visited
            if current_room not in visited:
                # Mark it as visited
                visited.add(current_room)
                # Add a path to each room to the queue
                for room in self.get_connected_rooms(current_room, visited=True):
                    new_path = path.copy()
                    new_path.append(self.rooms[current_room][room])
                    q.enqueue(new_path)

        return None
