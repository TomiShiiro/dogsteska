# Contains methods used to make the dog walk

# Authors: Andy Wendler, Ondřej Všelko
# Created: 11. 3. 2025
# Last edited: 31. 3. 2025


# test at techtower
# https://github.com/unitreerobotics/unitree_sdk2_python

# the dog will walk straight for a distance
# params:
#   dist - distance to walk
def straightWalk(point):
    print("I'm walking to " + str(point))

def walkToCoordinates(x, y):
    straightWalk(x)
    straightWalk(y)
    print("I'm here")