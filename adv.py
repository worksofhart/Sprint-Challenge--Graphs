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

seed = 0
shortest_traversal = 20000

while True:
    random.seed(seed)

    player = Player(world.starting_room)

    # Fill this out with directions to walk
    traversal_path = []

    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    graph = Graph()
    graph.add_room(player.current_room.id, player.current_room.get_exits())

    while len(visited_rooms) != len(room_graph):
        exits = graph.get_connected_rooms(
            player.current_room.id, visited=False)
        if exits:
            prev_room = player.current_room
            direction = random.choice(exits)
            player.travel(direction)
            traversal_path.append(direction)
            visited_rooms.add(player.current_room)
            graph.add_room(player.current_room.id,
                           player.current_room.get_exits())
            graph.connect_rooms(
                prev_room.id, player.current_room.id, direction)
        else:
            path, route = graph.bfs(player.current_room.id)
            for direction in route:
                player.travel(direction)
                traversal_path.append(direction)

    if len(traversal_path) < shortest_traversal:
        print(f"New shorter traversal found: {traversal_path}")
        print(f"Number of moves: {len(traversal_path)}")
        print(f"Seed: {seed}")
        shortest_traversal = len(traversal_path)

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


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
