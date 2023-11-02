
'''
import cyte.hygiene._node.architecture as hygiene_architecture
hygiene_architecture.create ()
'''

import cyte.hygiene.foods._db.architecture as foods_architecture
import cyte.hygiene.supplements._db.architecture as supplements_architecture

import cyte.hygiene.recipes._db.architecture as recipes_architecture


def create ():
	foods_architecture.create ()
	supplements_architecture.create ()
	recipes_architecture.create ()

