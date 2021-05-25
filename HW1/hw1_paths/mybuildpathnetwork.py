'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the path network as a list of lines between all path nodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = []

	### YOUR CODE GOES BELOW HERE ###

	worldLines = world.getLines()
	r = agent.getMaxRadius()
	collision = False

	for node in pathnodes:
		node1 = (node[0] + r, node[1] + r)
		node2 = (node[0] + r, node[1] - r)
		node3 = (node[0] - r, node[1] + r)
		node4 = (node[0] - r, node[1] - r)
		for target in pathnodes:
			targ1 = (target[0] + r, target[1] + r)
			targ2 = (target[0] + r, target[1] - r)
			targ3 = (target[0] - r, target[1] + r)
			targ4 = (target[0] - r, target[1] - r)

			for line in worldLines:
				if rayTrace(node1, targ1, line) is not None \
						or rayTrace(node2, targ2, line) is not None \
						or rayTrace(node3, targ3, line) is not None \
						or rayTrace(node4, targ4, line) is not None:
					collision = True
					break

			if not collision:
				lines.append((node, target))

			collision = False

	# obstacles = world.getObstacles()
	# toRemove = []
	# for line in lines:
	# 	for i in range(line[0][0], line[1][0]):
	# 		for j in range(line[1][0], line[1][1]):
	# 			for obstacle in obstacles:
	# 				if obstacle.pointInside((i,j)):
	# 					if line not in toRemove:
	# 						toRemove.append(line)

	# res = [i for i in lines if i not in toRemove]
	# lines = res


	### YOUR CODE GOES ABOVE HERE ###

	return lines
