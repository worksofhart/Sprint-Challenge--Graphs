
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

    def add_room(self, room_id):
        """
        Add a room to the graph.
        """
        if not room_id in self.rooms:
            self.rooms[room_id] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}

    def add_door(self, room1_id, room2_id, direction):
        """
        Add a directed edge to the graph.
        """
        reverse_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}[direction]

        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room1_id][direction] = room2_id
            self.rooms[room2_id][reverse_dir] = room1_id
        else:
            raise IndexError("That room does not exist.")

    def get_neighbors(self, room_id):
        """
        Get all neighbors (doors) of a room.
        """
        return self.rooms[room_id]

    def bfs(self, starting_room, destination_room):
        """
        Return a list containing the shortest path from
        starting_room to destination_room in
        breath-first order.
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
            # And if it is the current room, we're done searching
            if current_room == destination_room:
                return path

            # If the room has not been visited
            if current_room not in visited:
                # Mark it as visited
                visited.add(current_room)
                # Add a path to each neighbor to the queue
                for neighbor in self.get_neighbors(current_room):
                    new_path = path.copy()
                    new_path.append(neighbor)
                    q.enqueue(new_path)

        return None
