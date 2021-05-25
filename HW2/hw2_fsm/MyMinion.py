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

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from moba import *

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.states += [Move, Attack]
		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###

		world = self.agent.world
		enemyTowers = world.getEnemyTowers(self.agent.team)
		# minionRange = self.agent.bulletclass.range # THIS DOESN'T WORK?

		# sort enemyTowers based on distance
		enemyTowers.sort(key=lambda x: distance(self.agent.position, x.position))

		if len(enemyTowers) > 0:
			tower = enemyTowers[0]
			if distance(self.agent.position, tower.position) <= SMALLBULLETRANGE:
				self.agent.changeState(Attack, tower)
			else:
				self.agent.changeState(Move, tower)
		else:
			bases = world.getEnemyBases(self.agent.team)
			if len(bases) > 0:
				if distance(self.agent.position, bases[0].position) <= SMALLBULLETRANGE:
					self.agent.changeState(Attack, bases[0])
				else:
					self.agent.changeState(Move, bases[0])

		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print("Hey " + str(self.victim) + ", I don't like you!")
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:
class Move(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if self.target is not None:
			self.agent.navigateTo(self.target.position)

	def execute(self, delta = 0):
		State.execute(self, delta)
		if self.target is not None:
			minions = []
			visibleMinions = self.agent.getVisibleType(Minion)
			for minion in visibleMinions:
				if minion.team != self.agent.team:
					minions.append(minion)
			if distance(self.agent.position, self.target.position) < SMALLBULLETRANGE:
				self.agent.changeState(Attack, self.target)
			elif len(minions) > 0:
				for minion in minions:
					if distance(self.agent.position, minion.position) < SMALLBULLETRANGE:
						self.agent.turnToFace(minion.position)
						self.agent.shoot()
						break

	def exit(self):
		State.exit(self)
		self.agent.stopMoving()

class Attack(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)

	def execute(self, delta = 0):
		State.execute(self, delta)
		if self.target is not None and self.target.isAlive():
			self.agent.turnToFace(self.target.position)
			self.agent.shoot()
		else:
			self.agent.changeState(Idle)

	def exit(self):
		State.exit(self)