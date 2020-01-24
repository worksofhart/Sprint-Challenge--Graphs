from room import Room
from player import Player
from world import World
from util import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Seed for the pseudorandom number generator
# Best so far: 22902, number of moves 956
seed = 22902
shortest_traversal = 20000
# Lookup for finding direction player came from
reverse_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

# Find random traversals endlessly, incrementing seed and looking for better ones
while True:
    if not seed % 1000:  # Progress indicator
        print(f"{seed}", end="\r", flush=True)

    # Seed the random number generator for reproducible results
    random.seed(seed)

    # Start player in the first room
    player = Player(world.starting_room)

    # Will be filled with directions to walk
    traversal_path = []

    # Keep track of visited rooms so we know when we've visited them all
    visited_rooms = set()
    visited_rooms.add(player.current_room)

    # Initialize a graph to track rooms and connections between them
    graph = Graph()
    graph.add_room(player.current_room.id, player.current_room.get_exits())

    backtracked = False  # Track whether player has returned from a dead end

    # Loop until all rooms have been visited
    while len(visited_rooms) != len(room_graph):
        # Get a list of unvisited exits from the current location
        exits = graph.get_connected_rooms(
            player.current_room.id, visited=False)

        # If there are exits
        if exits:
            # Store current room for connecting to the next room
            current_room = player.current_room

            # If we didn't backtrack, bias toward making turns rather than going straight
            if not backtracked:
                # If there's more than one exit, remove the direction player came from
                # In order to force a turn
                if len(exits) > 1 and len(traversal_path) > 0:
                    prev_dir = reverse_dir[traversal_path[-1]]
                    if prev_dir in exits:
                        exits.remove(prev_dir)
                    direction = random.choice(exits)
                else:
                    direction = exits[0]
            else:
                # If we backtracked from a dead end, take next avail clockwise turn
                direction = exits[0]
                backtracked = False
            player.travel(direction)
            traversal_path.append(direction)
            visited_rooms.add(player.current_room)
            graph.add_room(player.current_room.id,
                           player.current_room.get_exits())
            graph.connect_rooms(
                current_room.id, player.current_room.id, direction)
        else:
            route = graph.bfs(player.current_room.id)
            for direction in route:
                player.travel(direction)
                traversal_path.append(direction)
            backtracked = True

    if len(traversal_path) < shortest_traversal:
        print(f"New shorter traversal found: {traversal_path}")
        print(f"Number of moves: {len(traversal_path)}")
        print(f"Seed: {seed}")
        shortest_traversal = len(traversal_path)

        # TRAVERSAL TEST
        visited_rooms = set()
        player.current_room = world.starting_room
        visited_rooms.add(player.current_room)

        for move in traversal_path:
            player.travel(move)
            visited_rooms.add(player.current_room)

        if len(visited_rooms) == len(room_graph):
            print(
                f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
        else:
            print("TESTS FAILED: INCOMPLETE TRAVERSAL")
            print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
        print(f"TOTAL MOVES: {len(traversal_path)}")

    seed += 1

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
print(f"TOTAL MOVES: {len(traversal_path)}")
