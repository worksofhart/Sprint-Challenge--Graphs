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

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

graph = Graph()
graph.add_room(player.current_room.id, player.current_room.get_exits())
print(graph.rooms)
# exit()

random.seed(1)
while len(visited_rooms) != len(room_graph):
    exits = graph.get_connected_rooms(player.current_room.id, visited=False)
    print(player.current_room.id, "Exits: ", exits)
    if exits:
        print("Exits found")
        prev_room = player.current_room
        direction = random.choice(exits)
        print(player.current_room, "Going:", direction)
        player.travel(direction)
        print("Went", direction)
        traversal_path.append(direction)
        visited_rooms.add(player.current_room)
        graph.add_room(player.current_room.id, player.current_room.get_exits())
        graph.connect_rooms(prev_room.id, player.current_room.id, direction)
        print(prev_room.id, player.current_room.id)
    else:
        print("dead end")
        # exits = graph.get_connected_rooms(player.current_room.id, visited=True)
        # direction = random.choice(exits)
        # player.travel(direction)
        # traversal_path.append(direction)
        path, route = graph.bfs(player.current_room.id)
        print(path, route)
        for direction in route:
            print(direction, end=" ", flush=True)
            player.travel(direction)
            traversal_path.append(direction)
        print(f"\n{player.current_room.id}")
        # exit()

print(graph.rooms, len(visited_rooms), len(room_graph))
print(traversal_path)
# print(visited_rooms)
# ['n', 'n', 'w', 'w', 'n', 'e', 'e', 'n', 'e',
# 'e', 's', 's', 'w', 'w', 'n', 'n', 'e']

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
